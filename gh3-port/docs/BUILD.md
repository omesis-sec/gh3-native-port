# Build the GH3 prototype (Windows)

The prototype is not playable; a complete clean-clone build has not yet been verified. Commands assume **PowerShell in `gh3-port/` inside this fork**, not the repository root or a separate prototype workspace. See [technical status](TECHNICAL_STATUS.md) for observed results.

## Prerequisites and existing work

Use Git, Python 3, CMake 3.21+, Visual Studio 2022 with the C++ workload and Windows SDK, and sufficient free disk space. Use Developer PowerShell with the tools on PATH. Supply your own lawfully obtained USA/NTSC SLUS-21672 ISO. `prepare_local.py` checks executable SHA-1 `15992cec17deb6bf8e3d8fa4a2a5f1ef1b60f47e`, not the full ISO; other releases are unvalidated.

The scripts read the ISO at its original location; they do not copy it into the repository. Extracted files and generated code go under ignored `local/`. Never commit game or BIOS data, generated game code, raw logs or build outputs.

For an existing checkout, inspect pending edits, active builds and `build/hybrid/CMakeCache.txt` first. Reuse compatible inputs and builds. Runtime-only changes do not need extraction or regeneration. Do not configure, regenerate or edit compiled sources while that checkout is building.

## Initial preparation only

Run commands individually and stop on failure. PowerShell does not necessarily stop after a native command fails: check `$LASTEXITCODE` before continuing. Preserve existing dependency checkouts rather than cloning over them or resetting their edits.

```powershell
git clone https://github.com/Ketbome/gh3-decomp.git reference/gh3-decomp
git -C reference/gh3-decomp checkout 5f24db7eb69ed9f3772bfe9124927670cf42405f
git clone https://github.com/raysan5/raylib.git reference/raylib
git -C reference/raylib checkout c1ab645ca298a2801097931d1079b10ff7eb9df8
```

Build the tools from this fork; no additional runtime checkout or prototype patch is required.

```powershell
cmake -S .. -B ../out/codex-build -G "Visual Studio 17 2022" -A x64 -DPS2X_BUILD_RUNTIME=OFF -DPS2X_BUILD_TEST=OFF -DPS2X_BUILD_STUDIO=OFF
if ($LASTEXITCODE -ne 0) { throw 'Tool configuration failed' }
cmake --build ../out/codex-build --config Release --target ps2_recomp ps2_analyzer --parallel 1
if ($LASTEXITCODE -ne 0) { throw 'Tool build failed' }
```

Replace the ISO placeholder. Run each step separately, checking its result.

```powershell
$iso = (Resolve-Path -LiteralPath 'PATH_TO_YOUR_ISO').Path
python scripts/prepare_local.py "$iso"
python scripts/recompile.py
python scripts/regenerate_hybrid.py
python scripts/extract_disc.py "$iso" --sounds
python scripts/extract_wad.py scripts/engine/engine_params.qb.ps2
```

`regenerate_hybrid.py` updates generated C++ and reapplies only transformations listed in that script, including memory/callback fixes. Preserve other experiments before running it. On a rejected function, inspect source and tool revisions rather than bypassing the check. The function map uses the separate decompilation reference. Neither that checkout nor generated game code belongs in a commit.

`--sounds` omits songs and movies; `--full` extracts those additional assets and is not required for this startup diagnostic. Configure after the hybrid tree exists; CMake can fetch additional dependencies.

```powershell
cmake -S . -B build/hybrid -G "Visual Studio 17 2022" -A x64 "-DGH3_GENERATED_DIR=$PWD/local/hybrid" "-DFETCHCONTENT_SOURCE_DIR_RAYLIB=$PWD/reference/raylib"
if ($LASTEXITCODE -ne 0) { throw 'Runner configuration failed' }
```

## Incremental build and relevant checks

Use Debug or Release consistently. Do not launch an older binary after a failed build. Runtime and runner use MSVC `/MP4`, so `--parallel 1` still permits several compiler processes.

```powershell
cmake --build build/hybrid --target ps2EntryRunner --config Release --parallel 1
if ($LASTEXITCODE -ne 0) { throw 'Runner build failed; do not run the previous binary' }
```

The runner is `build/hybrid/upstream/ps2xRuntime/Release/ps2EntryRunner.exe`. Confirm it includes the sources under investigation. For allocator changes, also run:

```powershell
cmake --build build/hybrid --target gh3_iop_memory_test --config Release --parallel 1
if ($LASTEXITCODE -ne 0) { throw 'Memory test build failed' }
& .\build\hybrid\Release\gh3_iop_memory_test.exe
if ($LASTEXITCODE -ne 0) { throw 'Memory test failed' }
```

For startup/runtime changes, after a successful corresponding build, set `$iso` as above and choose an unused log name:

```powershell
python scripts/run_diagnostic.py --build hybrid --config Release --seconds 55 --log run-release-01.log --iso "$iso"
```

The wrapper accepts 1–300 seconds and overwrites the selected log under `local/`. It prints the child exit code but **does not propagate child failure as its own exit status**. Inspect the printed result and log. Timeout is not a passing startup test. Record configuration, source revision/pending changes, relevant trace environment variables and virtual progression alongside wall time. Compilation and a bounded run do not establish playability.

Optional script diagnostics are disabled unless requested. In PowerShell, set `$env:GH3_TRACE_SCRIPT_ERRORS='1'` for bounded call/cursor statistics or `$env:GH3_TRACE_SCRIPT_STATES='1'` for up to 512 checkpoint samples per host thread after tick 300. Remove the variables afterwards with `Remove-Item Env:GH3_TRACE_SCRIPT_ERRORS, Env:GH3_TRACE_SCRIPT_STATES -ErrorAction SilentlyContinue`. Counters and periodic snapshots do not establish a matching reference stage.

For a selected guest object, `$env:GH3_TRACE_CURSOR_OBJECT='0xADDRESS'` enables bounded cursor-write diagnostics in the generated parser; replace the placeholder with an observed guest object address. Regeneration reapplies this instrumentation through `scripts/instrument_cursor_writes.py`. Remove the variable after use. Guest addresses are specific to an execution and must be validated before comparison.

For the optional script register sampling, set `$env:GH3_TRACE_SCRIPT_SAMPLES = '1'` before launching the wrapper and remove it with `Remove-Item Env:GH3_TRACE_SCRIPT_SAMPLES` afterward. The trace starts at virtual VSync tick 300, samples the configured PC range and stops after 512 events per host thread; an absent event does not prove a path was never executed. Logs stay local.

Choose checks for the affected behavior. Documentation-only edits do not require compiling or running the game.

## Optional video configuration

FFmpeg-backed MPEG decoding defaults to off. Add `-DPS2X_ENABLE_FFMPEG=ON` in a separate build directory for an experimental variant; this can download additional dependencies. Configuration success does not establish successful compilation or playback.

The diagnostic wrapper accepts only `--build hybrid` or `--build prototype`, using fixed paths under `build/`; it cannot select an arbitrary video build directory. Establish a bounded launch using that variant's actual executable and disc inputs before measuring it. Do not accidentally measure the old hybrid binary.
