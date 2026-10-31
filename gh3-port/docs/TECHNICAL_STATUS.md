# Technical status · 31 October 2026

The supported executable is `SLUS_216.72`, 2,625,152 bytes, SHA-1 `15992cec17deb6bf8e3d8fa4a2a5f1ef1b60f47e`. Only the executable hash was checked, not the full ISO. The analyzer identified 9,459 heuristic functions. A hybrid map combining game function boundaries with startup and library coverage yielded 9,822 translated entries, including 84 stubs and 1,904 indirect-flow warnings. Heuristic function names and boundaries remain provisional.

The native Debug runner opens a Windows window and has loaded the required IOP modules, including FILEIO and MSTREAM. It reads archives and scripts from local disc data. A bounded run passed the earlier invalid heap pointer, loaded over 150 packages, read the 2,617,312-byte `Z_Soundcheck` package, and remained active for 55 seconds. The observed window remained black. There is no verified menu, game input, synchronized sound or playable song.

## Changes made in this fork

- IOP command handlers are registered and early SIF commands are queued instead of silently discarded.
- IOP file services implement basic read-only open, close, read and seek operations.
- Freed IOP memory blocks are reused and free-space accounting considers fragmentation. The local allocation test passed 50,000 cycles.
- Recursive guest dispatch no longer treats a call returning to the same entry PC as already complete.
- The game's initial heap is limited below the callback stack reservation to avoid overwriting package data. This is applied to generated local code by `reserve_callback_memory.py`.
- The startup function map keeps the delay slot at `0x00101080` with its preceding `JAL`, and adds observed internal entry points.
- An early file-open callback guard prevents a completed response from being replaced by a provisional identifier. This is applied to generated local code by `fix_early_open_callback.py`.

The 200,000 EE-cycle SIF timing allowance is a temporary heuristic, not a faithful hardware model. File requests and the repeated opening of `sounds/sfx.wad` need investigation. The black window may involve rendering, scheduling, missing assets or another path; no single cause has been established. A locally rebuilt Release runner was observed for 55 seconds and stopped by the diagnostic timeout; that does not validate gameplay or a clean exit.

## Graphics investigation

An optional bounded register trace (`GH3_TRACE_SCRIPT_SAMPLES=1`) captured 158 script-range samples between VSync ticks 302 and 1194 during a 55-second Release diagnostic. A candidate script pointer recurred; an argument sampled at `0x0028E868`, called from the script loop-comparison routine, changed from 8 to 11. This establishes changing observed inputs, not successful boot progress or an infinite loop. The trace records at most 512 samples per guest thread after tick 300; a separate 12-second run with the variable unset emitted none. Both runs ended by timeout.

A subsequent 180-second Release observation reached presentation tick 3931 before timeout. After the initial blank sample, all 131 remaining presentation samples showed the same GIF counts (0,3,2), two primitive batches and 128 nonblack pixels. No instrumented MPEG events appeared. This longer observation does not prove an infinite loop or identify its cause. In the final 300 scheduler samples, PCs `0x002791E0` and `0x0027AF80` occurred 33 and 29 times; the former corresponds to a structure-cleanup routine in the decompilation reference, while the latter's semantics remain unverified.

A locally instrumented Release run reached approximately 1166 virtual VSync ticks during 55 seconds. At tick 1141, monitored GIF packet counts remained 0, 3 and 2, with two primitive batches and 128 nonblack pixels. The optional MPEG trace (`GH3_TRACE_MPEG=1`) recorded no events at its instrumented entry points; it does not cover every possible video path. The diagnostic ended by timeout. The trace is limited to 64 events per process and is disabled when the variable is unset.

A 55-second Debug run collected GIF packet, CPU primitive and presentation counters. At VSync tick 31, paths 1, 2 and 3 had submitted 0, 3 and 2 packets respectively, with two nonempty CPU primitive batches. The latched 640×448 image contained 128 pixels with a nonzero RGB channel. The same values appeared at ticks 61 and 91 while the guest scheduler continued to run. The display framebuffer was 0 and the presentation fallback selected source 70. This shows that some graphics reached the CPU backend, but it does not identify why subsequent monitored submissions stopped or establish whether the fallback source was appropriate.

The earlier invalid free was traced to the game's heap overlapping runtime callback stacks. Reserving the top MiB prevented the previously observed package terminator corruption; the bounded run passed both global archives and reached `Z_Soundcheck` without the former missing indirect-call target. The reserved region still needs a complete memory-layout audit.

An optional bounded IOP file trace (`GH3_TRACE_IOP_FILE=sfx.wad`) recorded 28 opens and 28 closes, 63 reads and 64 seeks on the matching file during a 55-second Debug run. The observed reads advanced through the file. These observations do not prove reference behavior, but the repeated opens alone are not evidence of an infinite open loop. The trace logs at most 512 events per IOP reset and is disabled when the filter is unset.

A reference PCSX2 fast boot of the supported disc logged opening FMV playback. The current native build defaults to FFmpeg-backed MPEG decoding disabled; it can be enabled at CMake configuration time, but video playback has not been validated. The standard `--sounds` extraction also omits movie files, though raw-disc reads can use the original ISO. It remains unverified whether the native execution reaches or waits for an FMV. The 55-second Debug observation advanced approximately 104 virtual VSync ticks; the temporary IOP timing allowance complicates time comparisons.

## Next investigation

1. Correlate the sampled script object and comparison inputs with an equivalent reference execution; identify the script and its expected progression before changing runtime semantics.
2. Trace startup scripts and outstanding file and audio operations alongside graphics submissions, then compare them with the reference.
3. Replace provisional IOP timing with request/response synchronization and verify no callback race remains.
4. Reach a navigable menu before testing audio, guitar controls and a full song.

Local logs and generated C++ are intentionally excluded. The developer workflow is in [BUILD.md](BUILD.md); public milestones are in the root [ROADMAP.md](../../../ROADMAP.md).
