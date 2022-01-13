import pathlib


class Geometry:
    """Geometry of disk image

    Attributes:
        sector_size: statically set to 512 bytes
        total_bytes: disk size in bytes
        total_sectors: number of sectors on the disk
        total_lba: number of logical blocks on the disk
        partition_start_lba: logical block where the partitions start
        partition_last_lba: logical block where the partitions end
        primary_header_lba: logical block location of primary header
        primary_header_byte: byte where primary header starts
        primary_array_lba: logical block where the primary partition array starts
        primary_array_byte: byte where the primary partition array starts
        backup_header_lba: logical block where the backup header starts
        backup_header_byte: byte where the backup header starts
        backup_header_array_lba: logical block where backup partition array starts
        backup_header_array_byte: byte where the backup partition array starts
    """

    def __init__(self, size: int) -> None:
        """Init Geometry with size in bytes"""
        self.sector_size = 512
        self.total_bytes = size
        self.total_sectors = int(size / self.sector_size)
        self.total_lba = int(size / self.sector_size)
        self.partition_start_lba = 34
        self.partition_last_lba = int(self.total_lba - 34)
        self.primary_header_lba = 1
        self.primary_header_byte = int(self.primary_header_lba * self.sector_size)
        self.primary_array_lba = 2
        self.primary_array_byte = int(self.primary_array_lba * self.sector_size)
        self.backup_header_lba = int(self.total_lba - 1)
        self.backup_header_byte = int(self.backup_header_lba * self.sector_size)
        self.backup_header_array_lba = int(self.total_lba - 33)
        self.backup_header_array_byte = int(
            self.backup_header_array_lba * self.sector_size
        )


class Disk:
    """GPT disk

    A disk objects represents a new or existing GPT disk image.  If the file exists,
    it is assumed to be an existing GPT image. If it does not, a new file is created.

    Attributes:
        image_path: file image path (absolute or relative)
        size: disk image size in bytes
        geometry:
    """

    def __init__(self, image_path: str, size: int = 0) -> None:
        """Init Disk with a file path and size in bytes"""
        # @TODO: check that disk is large enough to contain all table data
        self._image_path = pathlib.Path(image_path)
        self.name = self._image_path.name
        self._size = size
        if self._image_path.exists():
            self._size = self._image_path.stat().st_size
        self.geometry = Geometry(self._size)

    def write(self) -> None:
        """Write blank disk"""
        self._image_path.write_bytes(b"\x00" * self.geometry.total_bytes)
