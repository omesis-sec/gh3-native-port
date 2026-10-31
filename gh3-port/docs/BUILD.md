# Build the GH3 prototype (Windows)

This guide is for developers. The prototype is not playable and a full clean-clone build has not yet been verified. Commands assume PowerShell in `gh3-port/` inside this fork. You need Git, Python 3, CMake 3.21+, Visual Studio 2022 C++ tools, sufficient free disk space, and your own ISO of the USA/NTSC SLUS-21672 game.

The ISO and every extracted file stay under `gh3-port/local/`, which is ignored by Git. `prepare_local.py` checks SHA-1 `15992cec17deb6bf8e3d8fa4a2a5f1ef1b60f47e` for the executable. Other regional releases are not validated.

```powershell
git clone https://github.com/Ketbome/gh3-decomp.git reference/gh3-decomp
git -C reference/gh3-decomp checkout 5f24db7eb69ed9f3772bfe9124927670cf42405f
git clone https://github.com/raysan5/raylib.git reference/raylib
git -C reference/raylib checkout c1ab645ca298a2801097931d1079b10ff7eb9df8

cmake -S .. -B ../out/codex-build -G "Visual Studio 17 2022" -A x64 -DPS2X_BUILD_RUNTIME=OFF -DPS2X_BUILD_TEST=OFF -DPS2X_BUILD_STUDIO=OFF
cmake --build ../out/codex-build --config Release --target ps2_recomp ps2_analyzer --parallel 4
python scripts/prepare_local.py "PATH_TO_YOUR_ISO"
python scripts/recompile.py
python scripts/regenerate_hybrid.py
python scripts/extract_disc.py "PATH_TO_YOUR_ISO" --sounds
python scripts/extract_wad.py scripts/engine/engine_params.qb.ps2
cmake -S . -B build/hybrid -G "Visual Studio 17 2022" -A x64 "-DGH3_GENERATED_DIR=$PWD/local/hybrid" "-DFETCHCONTENT_SOURCE_DIR_RAYLIB=$PWD/reference/raylib"
cmake --build build/hybrid --target ps2EntryRunner gh3_iop_memory_test --config Debug --parallel 4
.\build\hybrid\Debug\gh3_iop_memory_test.exe
python scripts/run_diagnostic.py --build hybrid --config Debug --seconds 55 --log run-diagnostic.log --iso "PATH_TO_YOUR_ISO"
```

Replace `PATH_TO_YOUR_ISO`. CMake can fetch additional upstream dependencies. The diagnostic process is bounded; it terminates after the given time and writes a log under `local/`. It is a test of startup, not a way to play the game. The optional `--full` disc extraction includes songs and videos and is not required by the sequence above.

`scripts/regenerate_hybrid.py` creates a candidate tree, updates generated C++ and reapplies instrumentation and the two game-specific memory/callback fixes. If it rejects an unexpected generated function, inspect the source and tool revisions rather than bypassing the check. The generated function map uses the separately cloned decompilation project as reference; neither that checkout nor generated game code belongs in a commit.
