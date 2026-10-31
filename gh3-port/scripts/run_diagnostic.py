"""Run a bounded diagnostic launch of a locally built prototype."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', choices=('prototype', 'hybrid'), default='hybrid')
    parser.add_argument('--seconds', type=int, default=25)
    parser.add_argument('--config', choices=('Debug', 'Release'), default='Debug')
    parser.add_argument('--log', default='run-diagnostic.log')
    parser.add_argument('--iso', type=Path, help='Optional original ISO for raw disc reads')
    args = parser.parse_args()
    if sys.platform != 'win32' or not 1 <= args.seconds <= 300:
        parser.error('Windows and a timeout from 1 to 300 seconds are required')
    exe = ROOT / 'build' / args.build / 'upstream/ps2xRuntime' / args.config / 'ps2EntryRunner.exe'
    disc = ROOT / 'local/disc'
    elf = disc / 'SLUS_216.72'
    if not exe.is_file() or not elf.is_file():
        parser.error('Build the prototype and extract the initial disc files first')
    log = ROOT / 'local' / Path(args.log).name
    env = os.environ.copy()
    if args.iso:
        if not args.iso.is_file():
            parser.error('ISO path does not exist')
        env['GH3_DISC_IMAGE'] = str(args.iso.resolve())
    with log.open('w', encoding='utf-8') as stream:
        proc = subprocess.Popen([str(exe), str(elf)], cwd=disc,
                                stdout=stream, stderr=subprocess.STDOUT,
                                creationflags=subprocess.CREATE_NO_WINDOW, env=env)
        try:
            result = proc.wait(timeout=args.seconds)
            print(f'Process exit code: {result}')
        except subprocess.TimeoutExpired:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            print(f'Diagnostic stopped after {args.seconds} seconds')
    print(f'Log: {log}')


if __name__ == '__main__':
    main()
