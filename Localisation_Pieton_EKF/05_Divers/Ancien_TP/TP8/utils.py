from pathlib import Path
import numpy as np
import plotly.graph_objects as go


class Calibration:
    """Conteneur pour les paramètres de calibration KITTI."""

    def __init__(self):
        self.calib_time = None
        self.corner_dist = None

        self.S = {}
        self.K = {}
        self.D = {}
        self.R = {}
        self.T = {}
        self.S_rect = {}
        self.R_rect = {}
        self.P_rect = {}

        self.Tr_velo_to_cam = None
        self.Tr_imu_to_velo = None

    def load_cam_to_cam_file(self, filepath):
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(filepath)

        with filepath.open("r") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue

                key, raw_value = line.split(":", 1)
                key = key.strip()
                raw_value = raw_value.strip()

                if key == "calib_time":
                    self.calib_time = raw_value
                    continue

                if key == "corner_dist":
                    self.corner_dist = float(raw_value)
                    continue

                try:
                    values = np.array([float(x) for x in raw_value.split()])
                except ValueError:
                    continue

                if key.startswith("S_rect_"):
                    cam_id = int(key.split("_")[-1])
                    self.S_rect[cam_id] = values.astype(int)

                elif key.startswith("R_rect_"):
                    cam_id = int(key.split("_")[-1])
                    self.R_rect[cam_id] = values.reshape(3, 3)

                elif key.startswith("P_rect_"):
                    cam_id = int(key.split("_")[-1])
                    self.P_rect[cam_id] = values.reshape(3, 4)

                elif key.startswith("S_"):
                    cam_id = int(key.split("_")[-1])
                    self.S[cam_id] = values.astype(int)

                elif key.startswith("K_"):
                    cam_id = int(key.split("_")[-1])
                    self.K[cam_id] = values.reshape(3, 3)

                elif key.startswith("D_"):
                    cam_id = int(key.split("_")[-1])
                    self.D[cam_id] = values

                elif key.startswith("R_"):
                    cam_id = int(key.split("_")[-1])
                    self.R[cam_id] = values.reshape(3, 3)

                elif key.startswith("T_"):
                    cam_id = int(key.split("_")[-1])
                    self.T[cam_id] = values

    def load_velo_to_cam(self, filepath):
        filepath = Path(filepath)

        R = None
        T = None

        with filepath.open("r") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue

                key, raw_value = line.split(":", 1)
                key = key.strip()
                raw_value = raw_value.strip()

                try:
                    values = np.array([float(x) for x in raw_value.split()])
                except ValueError:
                    continue

                if key == "R":
                    R = values.reshape(3, 3)
                elif key == "T":
                    T = values.reshape(3)

        if R is None or T is None:
            raise ValueError("Calibration velo_to_cam incomplète")

        self.R_velo_to_cam = R
        self.T_velo_to_cam = T

    def load_imu_to_velo(self, filepath):
        filepath = Path(filepath)

        R = None
        T = None

        with filepath.open("r") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue

                key, raw_value = line.split(":", 1)
                key = key.strip()
                raw_value = raw_value.strip()

                try:
                    values = np.array([float(x) for x in raw_value.split()])
                except ValueError:
                    continue

                if key == "R":
                    R = values.reshape(3, 3)
                elif key == "T":
                    T = values.reshape(3)

        if R is None or T is None:
            raise ValueError("Calibration imu_to_velo incomplète")

        self.R_imu_to_velo = R
        self.T_imu_to_velo = T

    def load_all(self, cam_to_cam, velo_to_cam, imu_to_velo):
        self.load_cam_to_cam_file(cam_to_cam)
        self.load_velo_to_cam(velo_to_cam)
        self.load_imu_to_velo(imu_to_velo)
        
# Affichage du scan dans une figure 3D
def export_point_cloud_to_html(
    points: np.ndarray,
    output_html: str | Path,
    color_by: str = "z",
    max_points: int | None = None,
    point_size: int = 2,
    title: str = "Nuage de points 3D",
) -> Path:
    """
    Exporte un nuage de points 3D dans un fichier HTML interactif.

    Parameters
    ----------
    points : np.ndarray
        Tableau de forme (N, 3) ou (N, 4).
        Les trois premières colonnes sont x, y, z.
        La 4e colonne peut être la reflectance.
    output_html : str | Path
        Chemin du fichier HTML de sortie.
    color_by : str
        Mode de coloration :
        - "z"          : couleur selon la hauteur
        - "distance"   : couleur selon la distance à l'origine
        - "reflectance": couleur selon la 4e colonne
        - "none"       : couleur uniforme
    max_points : int | None
        Nombre maximal de points à afficher.
        Si le nuage est plus grand, sous-échantillonnage aléatoire.
    point_size : int
        Taille des points dans la visualisation.
    title : str
        Titre de la figure.

    Returns
    -------
    Path
        Chemin vers le fichier HTML généré.
    """
    if points.ndim != 2 or points.shape[1] not in (3, 4):
        raise ValueError("points doit être de forme (N, 3) ou (N, 4).")

    output_html = Path(output_html)

    # Sous-échantillonnage pour garder un HTML raisonnable
    if max_points is not None and len(points) > max_points:
        rng = np.random.default_rng(42)
        idx = rng.choice(len(points), size=max_points, replace=False)
        points = points[idx]

    xyz = points[:, :3]
    x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]

    marker_kwargs = {"size": point_size}

    if color_by == "z":
        color = z
        colorbar_title = "z [m]"
        marker_kwargs.update(
            color=color,
            colorscale="Viridis",
            colorbar=dict(title=colorbar_title),
        )
    elif color_by == "distance":
        color = np.linalg.norm(xyz, axis=1)
        colorbar_title = "Distance [m]"
        marker_kwargs.update(
            color=color,
            colorscale="Viridis",
            colorbar=dict(title=colorbar_title),
        )
    elif color_by == "reflectance":
        if points.shape[1] < 4:
            raise ValueError("La reflectance n'est pas disponible : points.shape[1] < 4.")
        color = points[:, 3]
        colorbar_title = "Reflectance"
        marker_kwargs.update(
            color=color,
            colorscale="Viridis",
            colorbar=dict(title=colorbar_title),
        )
    elif color_by == "none":
        marker_kwargs.update(color="blue")
    else:
        raise ValueError("color_by doit valoir 'z', 'distance', 'reflectance' ou 'none'.")

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="markers",
                marker=marker_kwargs,
            )
        ]
    )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="X [m]",
            yaxis_title="Y [m]",
            zaxis_title="Z [m]",
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, b=0, t=40),
    )

    fig.write_html(str(output_html), include_plotlyjs=True, full_html=True)
    return output_html

def export_global_cloud_with_trajectory_html(
    global_points,
    trajectory,
    output_html,
    max_points=None,
    point_size=1,
    color_by="z",
):
    """
    Exporte le nuage 3D global avec la trajectoire dans un fichier HTML interactif.
    """
    output_html = Path(output_html)

    points = global_points

    if max_points is not None and len(points) > max_points:
        rng = np.random.default_rng(42)
        idx = rng.choice(len(points), size=max_points, replace=False)
        points = points[idx]

    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]

    if color_by == "z":
        color = z
        colorbar_title = "z [m]"
    elif color_by == "distance":
        color = np.linalg.norm(points, axis=1)
        colorbar_title = "Distance [m]"
    else:
        color = None
        colorbar_title = None

    if color is None:
        marker = dict(size=point_size)
    else:
        marker = dict(
            size=point_size,
            color=color,
            colorscale="Viridis",
            colorbar=dict(title=colorbar_title),
        )

    cloud_trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers",
        marker=marker,
        name="Nuage LiDAR global",
    )

    traj_trace = go.Scatter3d(
        x=trajectory[:, 0],
        y=trajectory[:, 1],
        z=trajectory[:, 2],
        mode="lines+markers",
        line=dict(width=6),
        marker=dict(size=3),
        name="Trajectoire OXTS",
    )

    fig = go.Figure(data=[cloud_trace, traj_trace])

    fig.update_layout(
        title="Nuage de points 3D global et trajectoire du véhicule",
        scene=dict(
            xaxis_title="x local [m]",
            yaxis_title="y local [m]",
            zaxis_title="z local [m]",
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, b=0, t=40),
    )

    fig.write_html(str(output_html), include_plotlyjs=True, full_html=True)
    return output_html


def filter_lidar_points(
    points,
    x_min=0.0,
    x_max=50.0,
    y_min=-25.0,
    y_max=25.0,
    z_min=-2.5,
    z_max=2.0,
):
    """
    Filtrage simple dans le repère Velodyne :
    x devant, y gauche, z haut.
    """
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]

    mask = (
        (x >= x_min) & (x <= x_max) &
        (y >= y_min) & (y <= y_max) &
        (z >= z_min) & (z <= z_max)
    )

    return points[mask]

def voxel_downsample(points, voxel_size=0.20):
    """
    Réduit un nuage de points en gardant un point par voxel.

    points : ndarray (N, 3) ou (N, 4)
    voxel_size : taille du voxel en mètres
    """
    xyz = points[:, :3]

    voxel_indices = np.floor(xyz / voxel_size).astype(np.int64)

    _, unique_indices = np.unique(
        voxel_indices,
        axis=0,
        return_index=True
    )

    return points[unique_indices]