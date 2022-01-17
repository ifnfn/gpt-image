"""
Header information reference: https://en.wikipedia.org/wiki/GUID_Partition_Table

"""
import binascii
import uuid
from dataclasses import dataclass

from gpt_image.disk import Disk, Geometry


@dataclass
class TableEntry:
    """Individual table entries

    Creates a consistent structure for writing GPT table data to its
    respective locations.  This is used for headers and partitions.

    The data field only accepts bytes to simplify writing back to a buffer.
    """

    offset: int
    length: int
    data: bytes
    # @TODO: make default data b"\x00" * length


class ProtectiveMBR:
    """Protective MBR Table Entry

    Provides the bare minimum entries needed to represent a protective MBR.
    https://thestarman.pcministry.com/asm/mbr/PartTables.htm#pte


    """

    def __init__(self, geometry: Geometry):
        self.boot_indictor = TableEntry(0, 1, b"\x00")  # not bootable
        self.start_chs = TableEntry(1, 3, b"\x00\x00\x00")  # ignore the start CHS
        self.partition_type = TableEntry(4, 1, b"\xEE")  # GPT partition type
        self.end_chs = TableEntry(5, 3, b"\x00\x00\x00")  # ignore the end CHS
        self.start_sector = TableEntry(
            8, 4, geometry.primary_header_lba.to_bytes(4, "little")
        )
        self.partition_size = TableEntry(
            12, 4, geometry.total_sectors.to_bytes(4, "little")
        )
        self.signature = TableEntry(510, 4, b"\x55\xAA")

        self.mbr_fields = [
            self.boot_indictor,
            self.start_chs,
            self.partition_type,
            self.end_chs,
            self.start_sector,
            self.partition_size,
        ]

    def as_bytes(self):
        """Get the Protective MBR as bytes

        Does not include the signature

        """
        byte_list = [x.data for x in self.mbr_fields]
        return b"".join(byte_list)


class Header:
    """GPT Partition Table Header Object

    Each table has two GPT headers, primary and secondary (backup). The primary is
    written to LBA 1 and secondary is written to LBA -1. The GPT Headers contain
    various data including the locations of one another. Therefore two headers
    are created for each table.

    """

    def __init__(self, geometry: Geometry, is_backup: bool = False):
        self.backup = is_backup
        self.geometry = geometry
        # @NOTE: the offsets are not being used, at may be removed
        self.header_sig = TableEntry(0, 8, b"EFI PART")
        self.revision = TableEntry(8, 4, b"\x00\x00\x01\x00")
        self.header_size = TableEntry(12, 4, (92).to_bytes(4, "little"))
        self.header_crc = TableEntry(16, 4, (0).to_bytes(4, "little"))
        self.reserved = TableEntry(20, 4, (0).to_bytes(4, "little"))
        self.primary_header_lba = TableEntry(
            24, 8, (self.geometry.primary_header_lba).to_bytes(8, "little")
        )
        self.secondary_header_lba = TableEntry(
            32, 8, (self.geometry.backup_header_lba).to_bytes(8, "little")
        )
        self.partition_start_lba = TableEntry(
            40, 8, (self.geometry.partition_start_lba).to_bytes(8, "little")
        )
        self.partition_last_lba = TableEntry(
            48, 8, (self.geometry.partition_last_lba).to_bytes(8, "little")
        )
        # self.disk_guid = TableEntry(56, 16, uuid.uuid4().bytes_le)
        self.disk_guid = TableEntry(
            56, 16, uuid.UUID("B3D6E0E0-7378-4E9A-B0A8-503D8C58E536").bytes_le
        )
        self.partition_array_start = TableEntry(
            72, 8, (self.geometry.primary_array_lba).to_bytes(8, "little")
        )
        self.partition_array_length = TableEntry(80, 4, (128).to_bytes(4, "little"))
        self.partition_entry_size = TableEntry(84, 4, (128).to_bytes(4, "little"))
        self.partition_array_crc = TableEntry(88, 4, (0).to_bytes(4, "little"))
        self.reserved_padding = TableEntry(92, 420, b"\x00" * 420)
        # the secondary header adjustments
        if self.backup:
            self.primary_header_lba.data, self.secondary_header_lba.data = (
                self.secondary_header_lba.data,
                self.primary_header_lba.data,
            )
            self.partition_array_start.data = (self.geometry.backup_array_lba).to_bytes(
                8, "little"
            )

        # header start byte relative the table itself, not the disk
        # primary will be 0 secondary will be LBA 32
        self.header_start_byte = 0
        self.partition_entry_start_byte = int(1 * self.geometry.sector_size)
        if self.backup:
            self.header_start_byte = int(32 * self.geometry.sector_size)
            self.partition_entry_start_byte = 0

        # group the header fields to allow byte operations such as
        # checksum
        # this can be done with the `inspect` module OR just use bytearrays
        # and remove the TableEntry entirely
        self.header_fields = [
            self.header_sig,
            self.revision,
            self.header_size,
            self.header_crc,
            self.reserved,
            self.primary_header_lba,
            self.secondary_header_lba,
            self.partition_start_lba,
            self.partition_last_lba,
            self.disk_guid,
            self.partition_array_start,
            self.partition_array_length,
            self.partition_entry_size,
            self.partition_array_crc,
        ]

    def as_bytes(self) -> bytes:
        """Return the header as bytes"""
        byte_list = [x.data for x in self.header_fields]
        return b"".join(byte_list)


class Partition:
    """Partition class represents a GPT partition

    Start and end LBA are set to None because they must be calculated
    from a table's partition list.
    """

    @dataclass
    class Type:
        """GPT Partition Types

        https://en.wikipedia.org/wiki/GUID_Partition_Table#Partition_entries
        """

        LinuxFileSystem = "0FC63DAF-8483-4772-8E79-3D69D8477DE4"
        EFISystemPartition = "C12A7328-F81F-11D2-BA4B-00A0C93EC93B"

    def __init__(
        self,
        name: str = None,
        size: int = 0,
        partition_guid: uuid.UUID = None,
        alignment: int = 8,
    ):
        """Initialize Partition Object

        All parameters have a default value to allow Partition() to create
        an empty partition object.  If "name" is set, we assume this is not
        an empty object and set the other values.
        """
        # create an empty partition object
        self.type_guid = TableEntry(0, 16, b"\x00" * 16)
        self.partition_guid = TableEntry(16, 16, b"\x00" * 16)
        self.first_lba = TableEntry(32, 8, b"\x00" * 8)
        self.last_lba = TableEntry(40, 8, b"\x00" * 8)
        self.attribute_flags = TableEntry(48, 8, b"\x00" * 8)
        self.partition_name = TableEntry(56, 72, b"\x00" * 72)

        # if name is set, this isn't an empty partition. Set relevant fields
        if name:
            self.type_guid.data = uuid.UUID(Partition.Type.LinuxFileSystem).bytes_le
            if not partition_guid:
                self.partition_guid.data = uuid.uuid4().bytes_le
            else:
                self.partition_guid.data = partition_guid.bytes_le
            b_name = bytes(name, encoding="utf_16_le")
            # ensure the partition name is padded
            self.partition_name.data = b_name + bytes(72 - len(b_name))

        self.alignment = alignment
        self.size = size

        self.partition_fields = [
            self.type_guid,
            self.partition_guid,
            self.first_lba,
            self.last_lba,
            self.attribute_flags,
            self.partition_name,
        ]

    def as_bytes(self) -> bytes:
        """Return the partition as bytes"""
        byte_list = [x.data for x in self.partition_fields]
        return b"".join(byte_list)


class Table:
    """GPT Partition Table Object

    The Table class the meant to be used by the consumer.  The underlying
    classes should be called through functions in this class and not
    directly used.
    """

    def __init__(self, disk: Disk, sector_size: int = 512) -> None:
        self.disk = disk
        self.geometry = disk.geometry
        self.protective_mbr = ProtectiveMBR(self.geometry)
        self.primary_header = Header(self.geometry)
        self.secondary_header = Header(self.geometry, is_backup=True)

        self.partition_entries = [Partition()] * 128

    def write(self):
        """Write the table to disk"""
        # calculate partition checksum and write to header
        self.checksum_partitions(self.primary_header)
        self.checksum_partitions(self.secondary_header)

        # calculate header checksum and write to header
        self.checksum_header(self.primary_header)
        self.checksum_header(self.secondary_header)

        with open(self.disk.image_path, "r+b") as f:
            # write protective MBR
            f.seek(446)
            f.write(self.protective_mbr.as_bytes())
            f.seek(510)
            f.write(self.protective_mbr.signature.data)

            # write primary header
            f.seek(self.geometry.primary_header_byte)
            f.write(self.primary_header.as_bytes())

            # write primary partition table
            f.seek(self.geometry.primary_array_byte)
            f.write(self._partition_entries_as_bytes())

            # move to secondary header location and write
            f.seek(self.geometry.backup_header_byte)
            f.write(self.secondary_header.as_bytes())

            # write secondary partition table
            f.seek(self.geometry.backup_array_byte)
            f.write(self._partition_entries_as_bytes())

    def create_partition(
        self, name: str, size: int, guid: uuid.UUID, alignment: int = 8
    ):
        part = Partition(
            name,
            size,
            guid,
            alignment,
        )
        # find the first empty partition index
        for idx, partition in enumerate(self.partition_entries):
            if int.from_bytes(partition.partition_name.data, byteorder="little") == 0:
                part.first_lba.data = self._first_lba()
                last_lba = int(part.size / self.geometry.sector_size) + int.from_bytes(
                    part.first_lba.data, byteorder="little"
                )
                part.last_lba.data = (last_lba).to_bytes(8, "little")
                self.partition_entries[idx] = part
                break

    def _first_lba(self) -> bytes:
        """Find the last LBA used by a partition"""
        last_lba = 0
        for partition in self.partition_entries:
            last_lba_int = int.from_bytes(partition.last_lba.data, byteorder="little")
            if last_lba_int > last_lba:
                last_lba = last_lba_int
        if last_lba == 0:
            return (34).to_bytes(8, "little")
        # @NOTE: this is NOT proper alignment
        return (last_lba + 1).to_bytes(8, "little")

    def _partition_entries_as_bytes(self):
        parts = [x.as_bytes() for x in self.partition_entries]
        return b"".join(parts)

    def checksum_partitions(self, header: Header):
        """Checksum the partition entries"""
        part_entry_bytes = self._partition_entries_as_bytes()
        header.partition_array_crc.data = binascii.crc32(part_entry_bytes).to_bytes(
            4, "little"
        )

    def checksum_header(self, header: Header):
        """Checksum the table header

        This CRC includes the partition checksum, and must be calculated
        after that has been written.
        """
        # zero the old checksum before calculating
        header.header_crc.data = b"\x00" * 4
        header.header_crc.data = binascii.crc32(header.as_bytes()).to_bytes(4, "little")
