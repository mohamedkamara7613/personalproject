import matplotlib.pyplot as plt
import numpy as np


def plot_single_scan(points,
                     min_range=None,
                     max_range=None):
    """
    Affiche un scan LiDAR dans un plan cartésien.

    Parameters
    ----------
    points : list[[x, y]]
        Points cartésiens du scan.
    min_range : float
        Portée minimale du LiDAR.
    max_range : float
        Portée maximale du LiDAR.
    """

    if not points:
        print("Aucun point à afficher.")
        return

    x = np.array([p[0] for p in points])
    y = np.array([p[1] for p in points])

    distances = np.sqrt(x**2 + y**2)

    fig, ax = plt.subplots()

    # Points LiDAR colorés par distance
    scatter = ax.scatter(x, y,
                         c=distances,
                         s=6,
                         cmap="viridis")

    plt.colorbar(scatter, label="Distance")

    # Robot au centre
    ax.scatter(0, 0, marker='x', s=80, color='red', label="Robot")

    # Cercle portée max
    if max_range:
        circle_max = plt.Circle((0, 0),
                                max_range,
                                fill=False,
                                linestyle='--',
                                color='gray')
        ax.add_patch(circle_max)

    # Cercle portée min
    if min_range:
        circle_min = plt.Circle((0, 0),
                                min_range,
                                fill=False,
                                linestyle=':',
                                color='gray')
        ax.add_patch(circle_min)

    # Limites axes
    if max_range:
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)

    ax.set_aspect("equal")

    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_title("LiDAR Scan")

    ax.grid(True)
    ax.legend()

    plt.show()
    

def live_scan_plot(scan_iterator,
                   min_range=None,
                   max_range=None,
                   refresh_interval=0.001,
                   point_size=6):
    """
    Affiche en temps réel des scans LiDAR dans un plan cartésien.

    Parameters
    ----------
    scan_iterator : iterable
        Itérateur renvoyant des tuples du type :
        (timestamp, scan, points)
        où points est une liste de couples [x, y].
    min_range : float, optional
        Portée minimale du LiDAR.
    max_range : float, optional
        Portée maximale du LiDAR.
    refresh_interval : float, optional
        Temps de pause matplotlib entre deux mises à jour.
    point_size : int, optional
        Taille des points affichés.
    """

    plt.ion()
    fig, ax = plt.subplots(figsize=(7, 7))

    scatter = ax.scatter([], [], s=point_size)
    robot = ax.scatter([0], [0], marker='x', s=80, color='red', label="Robot")

    circle_max = None
    circle_min = None

    if max_range is not None:
        circle_max = plt.Circle(
            (0, 0),
            max_range,
            fill=False,
            linestyle='--',
            color='gray'
        )
        ax.add_patch(circle_max)

    if min_range is not None and min_range > 0:
        circle_min = plt.Circle(
            (0, 0),
            min_range,
            fill=False,
            linestyle=':',
            color='gray'
        )
        ax.add_patch(circle_min)

    if max_range is not None:
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
    else:
        ax.set_xlim(-1000, 1000)
        ax.set_ylim(-1000, 1000)

    ax.set_aspect("equal")
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_title("Live LiDAR Scan")
    ax.grid(True)
    ax.legend()

    timestamp_text = ax.text(
        0.02, 0.98, "",
        transform=ax.transAxes,
        verticalalignment="top"
    )

    try:
        for timestamp, scan, points in scan_iterator:
            if not plt.fignum_exists(fig.number):
                break

            if points:
                coords = np.array(points)
                scatter.set_offsets(coords)
            else:
                scatter.set_offsets(np.empty((0, 2)))

            timestamp_text.set_text(f"Timestamp: {timestamp:.3f}\nPoints: {len(points)}")

            fig.canvas.draw_idle()
            plt.pause(refresh_interval)

    except KeyboardInterrupt:
        print("\nAffichage temps réel interrompu par l'utilisateur.")

    finally:
        plt.ioff()
        plt.show()