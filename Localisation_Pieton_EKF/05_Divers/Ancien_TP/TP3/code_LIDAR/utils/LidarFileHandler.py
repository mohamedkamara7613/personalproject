import struct
from pathlib import Path


class LidarBinaryWriter:
    """
    Écriture de scans LiDAR dans un format binaire simple.

    Format :
    - Header global
    - Suite de scans
    - Chaque scan contient :
        timestamp_us (uint64)
        scan_id (uint32)
        point_count (uint16)
        puis point_count points :
            quality (uint8)
            angle_centideg (uint16)
            distance_mm (uint16)
    """

    MAGIC = b"LSCAN01\x00"
    VERSION = 1

    HEADER_STRUCT = struct.Struct("<8sHffffH")
    SCAN_HEADER_STRUCT = struct.Struct("<QIH")
    POINT_STRUCT = struct.Struct("<BHH")

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.file = None
        self.scan_id = 0
        self.header_written = False

    def open(self):
        self.file = open(self.file_path, "wb")

    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None

    def write_header(self,
                     min_angle,
                     max_angle,
                     min_range,
                     max_range,
                     quality_threshold):
        """
        Écrit le header global du fichier.
        """
        if self.file is None:
            self.open()

        packed = self.HEADER_STRUCT.pack(
            self.MAGIC,
            self.VERSION,
            float(min_angle),
            float(max_angle),
            float(min_range),
            float(max_range),
            int(quality_threshold),
        )
        self.file.write(packed)
        self.header_written = True

    def write_scan(self, timestamp, scan):
        """
        Écrit un scan dans le fichier.

        Parameters
        ----------
        timestamp : float
            Timestamp en secondes (time.time()).
        scan : list[tuple]
            Liste de mesures (quality, angle_deg, distance_mm).
        """
        if self.file is None:
            raise RuntimeError("Le fichier n'est pas ouvert.")
        if not self.header_written:
            raise RuntimeError("Le header doit être écrit avant les scans.")

        timestamp_us = int(timestamp * 1_000_000)
        point_count = len(scan)

        self.file.write(
            self.SCAN_HEADER_STRUCT.pack(
                timestamp_us,
                self.scan_id,
                point_count
            )
        )

        for quality, angle_deg, distance_mm in scan:
            angle_centideg = int(round(angle_deg * 100.0))
            distance_mm = int(round(distance_mm))

            if angle_centideg < 0:
                angle_centideg = 0
            elif angle_centideg > 65535:
                angle_centideg = 65535

            if distance_mm < 0:
                distance_mm = 0
            elif distance_mm > 65535:
                distance_mm = 65535

            if quality < 0:
                quality = 0
            elif quality > 255:
                quality = 255

            self.file.write(
                self.POINT_STRUCT.pack(
                    int(quality),
                    angle_centideg,
                    distance_mm
                )
            )

        self.scan_id += 1

    def flush(self):
        if self.file is not None:
            self.file.flush()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class LidarBinaryReader:
    """
    Lecture de fichiers binaires LiDAR au format LSCAN.
    
    Exemple d'utilisation:
    
    from utils.LidarFileHandler import LidarBinaryReader
    with LidarBinaryReader("acquisition.lscan") as reader:
        header = reader.read_header()
        print(header)
        for scan_data in reader.iter_scans():
            print(scan_data["scan_id"], scan_data["timestamp"], len(scan_data["scan"]))
    """

    HEADER_STRUCT = struct.Struct("<8sHffffH")
    SCAN_HEADER_STRUCT = struct.Struct("<QIH")
    POINT_STRUCT = struct.Struct("<BHH")

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.file = None
        self.header = None

    def open(self):
        self.file = open(self.file_path, "rb")

    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None

    def read_header(self):
        """
        Lit le header global et le retourne sous forme de dict.
        """
        if self.file is None:
            self.open()

        raw = self.file.read(self.HEADER_STRUCT.size)
        if len(raw) != self.HEADER_STRUCT.size:
            raise ValueError("Fichier trop court ou header invalide.")

        magic, version, min_angle, max_angle, min_range, max_range, quality_threshold = \
            self.HEADER_STRUCT.unpack(raw)

        if magic != b"LSCAN01\x00":
            raise ValueError("Magic invalide : ce fichier n'est pas un .lscan reconnu.")

        self.header = {
            "magic": magic,
            "version": version,
            "min_angle": min_angle,
            "max_angle": max_angle,
            "min_range": min_range,
            "max_range": max_range,
            "quality_threshold": quality_threshold,
        }
        return self.header

    def read_scan(self):
        """
        Lit un scan.
        Retourne None si fin de fichier.
        """
        if self.file is None:
            raise RuntimeError("Le fichier n'est pas ouvert.")
        if self.header is None:
            raise RuntimeError("Le header doit être lu avant les scans.")

        raw = self.file.read(self.SCAN_HEADER_STRUCT.size)
        if len(raw) == 0:
            return None
        if len(raw) != self.SCAN_HEADER_STRUCT.size:
            raise ValueError("Header de scan incomplet.")

        timestamp_us, scan_id, point_count = self.SCAN_HEADER_STRUCT.unpack(raw)

        scan = []
        for _ in range(point_count):
            point_raw = self.file.read(self.POINT_STRUCT.size)
            if len(point_raw) != self.POINT_STRUCT.size:
                raise ValueError("Point incomplet dans le fichier.")

            quality, angle_centideg, distance_mm = self.POINT_STRUCT.unpack(point_raw)
            angle_deg = angle_centideg / 100.0

            scan.append((quality, angle_deg, distance_mm))

        return {
            "timestamp": timestamp_us / 1_000_000.0,
            "scan_id": scan_id,
            "scan": scan,
        }

    def iter_scans(self):
        """
        Itère sur tous les scans du fichier.
        """
        while True:
            scan = self.read_scan()
            if scan is None:
                break
            yield scan

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()