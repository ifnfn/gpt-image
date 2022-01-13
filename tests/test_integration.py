from gpt_image import disk, table


def test_e2e():
    new_disk = disk.Disk("test-disk.raw", 2 * 1024 * 1024)

    t = table.Table(new_disk)
    t.write()
