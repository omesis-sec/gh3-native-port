"""Prepare local input and an experimental function map for SLUS-21672."""
import argparse
import csv
import hashlib
from pathlib import Path

SECTOR = 2048
EXPECTED_SHA1 = "15992cec17deb6bf8e3d8fa4a2a5f1ef1b60f47e"
ROOT = Path(__file__).resolve().parent.parent


def extract_elf(iso):
    with iso.open("rb") as image:
        image.seek(16 * SECTOR)
        pvd = image.read(SECTOR)
        if pvd[1:6] != b"CD001":
            raise ValueError("ISO9660 primary volume descriptor not found")
        record = pvd[156:]
        extent = int.from_bytes(record[2:6], "little")
        size = int.from_bytes(record[10:14], "little")
        image.seek(extent * SECTOR)
        directory = image.read(size)
        pos = 0
        while pos < len(directory):
            length = directory[pos]
            if not length:
                pos = (pos // SECTOR + 1) * SECTOR
                continue
            entry = directory[pos:pos + length]
            name = entry[33:33 + entry[32]].decode("ascii", errors="replace")
            if name.upper() == "SLUS_216.72;1":
                image.seek(int.from_bytes(entry[2:6], "little") * SECTOR)
                return image.read(int.from_bytes(entry[10:14], "little"))
            pos += length
    raise ValueError("SLUS_216.72 was not found in the ISO root")


def function_map(path, out):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        fields = line.split()
        if len(fields) != 4 or not fields[1].startswith("0x"):
            continue
        name, start, size = fields[0], int(fields[1], 16), int(fields[2], 16)
        if size <= 0:
            raise ValueError(f"Invalid function size: {name}")
        rows.append((name, start, size))
    # This entry-point boundary comes from PS2Recomp's heuristic baseline;
    # it is provisional and should be checked independently.
    rows.append(("_start", 0x103D08, 0x140))
    rows.sort(key=lambda item: item[1])
    if len({start for _, start, _ in rows}) != len(rows):
        raise ValueError("Duplicate function addresses")
    if any(a + size > b for (_, a, size), (_, b, _) in zip(rows, rows[1:])):
        raise ValueError("Overlapping function ranges")
    with out.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(("Name", "Start", "End", "Size"))
        for name, start, size in rows:
            writer.writerow((name, f"0x{start:08X}", f"0x{start+size:08X}", size))
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("iso", type=Path, help="Path to the local PS2 ISO")
    args = parser.parse_args()
    data = extract_elf(args.iso)
    digest = hashlib.sha1(data).hexdigest()
    if digest != EXPECTED_SHA1:
        raise ValueError(f"Unexpected executable SHA-1: {digest}")
    output = ROOT / "local"
    output.mkdir(exist_ok=True)
    (output / "SLUS_216.72.elf").write_bytes(data)
    source = ROOT / "reference/gh3-decomp/config/functions.txt"
    if source.exists():
        count = function_map(source, output / "gh3-functions.csv")
        print(f"Function map: {count} entries (including provisional _start)")
    print(f"ELF extracted to {output}; SHA-1 verified: {digest}")


if __name__ == "__main__":
    main()
