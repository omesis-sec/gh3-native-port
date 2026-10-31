"""Analyze and translate the locally extracted ELF with PS2Recomp."""
import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / "local"
BIN = ROOT.parent / "out/codex-build"


def run(args, log):
    with log.open("w", encoding="utf-8") as stream:
        result = subprocess.run([str(a) for a in args], cwd=ROOT,
                                stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}); see {log}")
    print(f"Completed: {args[0].name}; log: {log}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", action="store_true",
                        help="Use the experimental gh3-decomp function map")
    args = parser.parse_args()
    elf = LOCAL / "SLUS_216.72.elf"
    if not elf.exists():
        parser.error("Run scripts/prepare_local.py with your ISO first")
    analyzer = BIN / "ps2xAnalyzer/Release/ps2_analyzer.exe"
    recompiler = BIN / "ps2xRecomp/Release/ps2_recomp.exe"
    if not analyzer.exists() or not recompiler.exists():
        parser.error("Build PS2Recomp analyzer and recompiler first")
    analysis = LOCAL / "analysis.toml"
    run([analyzer, "local/SLUS_216.72.elf", "local/analysis.toml"], LOCAL / "analyzer.log")
    config = analysis.read_text(encoding="utf-8")
    destination = "mapped" if args.map else "baseline"
    config = config.replace('output = "local/output/"', f'output = "local/{destination}/"')
    config = config.replace('single_file_output = false',
                            'single_file_output = false\nlow_memory_mode = true\noutput_worker_threads = 4')
    if args.map:
        if not (LOCAL / "gh3-functions.csv").exists():
            parser.error("Function map missing; run prepare_local.py first")
        config = config.replace('ghidra_output = ""',
                                'ghidra_output = "local/gh3-functions.csv"')
    target = LOCAL / f"{destination}.toml"
    target.write_text(config, encoding="utf-8")
    run([recompiler, target], LOCAL / f"{destination}.log")
    print("Translation alone does not establish correct execution or gameplay.")


if __name__ == "__main__":
    main()
