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

An opt-in per-thread cursor trace found that, among 2,097,152 observed calls at the script parsing call site, the cursor differed from the preceding call 2,097,151 times but matched the value four calls earlier 2,081,171 times. Two bounded 16-address snapshots showed the same four-position sequence recurring. In 256 checkpoint samples at ticks 302–1194, eight showed a non-null status pointer. Local classification of two observed status messages identified an excessive-expression-operators condition and a stack-related condition. These observations do not establish which condition is primary, nor whether the sequence also occurs in an equivalent reference stage. Both traces are optional; the diagnostic ended by timeout.

Four corresponding parser return PCs repeated with the cursor sequence. At sampled calls from `0x00290BA0`, the generated branch observed depth 0, index 1, a zero base entry and a zero indexed word. These observations locate the condition that leads to the status-setting call; they do not establish why that state occurs.

An extended 180-second Release observation with more widely spaced checkpoint samples recorded 23 non-null status pointers in 254 samples across ticks 313–3860. At 4,194,304 observed parser calls, 4,178,283 cursor values matched the value four calls earlier. A 20-second control with optional traces disabled reached tick 425 and emitted none of their events. Both diagnostics ended by timeout. Sampling cadence and execution stage differ from the reference; these counts are not a direct statistical comparison.

A repeat with the final instrumentation recorded 24 non-null status pointers in 261 checkpoint samples through tick 3958 and reproduced the same four-call match count at 4,194,304 parser calls. Its 20-second disabled-trace control reached tick 432 without optional events. Both ended by timeout.

Among 1,043,907 completed parser calls observed from `0x0028AB90`, 1,043,860 returned an address numerically above the input, 47 returned the same address and none returned a lower one; yielded calls are excluded. A separate opt-in trace of selected generated code observed at least 524,288 writes decreasing the selected cursor by four bytes at guest PC `0x0028B3E4`. These observations do not identify the source of larger changes between parser calls or prove that a reference run behaves differently. Both 55-second traced diagnostics ended by timeout.

A further isolated PCSX2 run sampled the same four fixed-address fields about 50 times per second for 60 seconds. Among 2,890 successful batches, two reported depth 0, loop index 1, active 1, and a null status pointer; four reported depth 1 with the same remaining values. Eighteen early batches failed while the VM was starting; the remaining successful samples had loop index 0. Reads in each batch are sequential, and the reference call sites were not captured. The matching field tuple can occur in the reference and alone does not prove divergence.

A longer isolated 180-second reference observation yielded 8,710 successful batches, all with a null status pointer, plus 18 failed early startup reads. PCSX2 logged FMV playback during that run. The snapshots were sequential and not aligned with the native run's call sites or virtual time. PCSX2 applied GameDB settings and reported finding an optional game patch; the log alone does not establish whether that patch was enabled.

An additional 55-second Release trace sampled calls from `0x00287084` to `0x00290AA8` and reached 2,097,152 calls at tick 1124. The sampled cursor address repeated across some samples and changed across others; this does not describe every iteration. A 12-second disabled-trace control produced no optional events. In a separate isolated PCSX2 reference run, the instruction at `0x0028EB18` matched the target executable and 30 one-second reads of fields at the candidate fixed object reported depth 0, loop index 0, active 1 and no status pointer. The reference log recorded opening FMVs during that run. These snapshots may represent different boot stages and do not establish causality or matched call behavior.

An optional bounded trace (`GH3_TRACE_SCRIPT_ERRORS=1`) found 524,288 calls by VSync tick 770 to guest function `0x0028EB18`, which the decompilation reference identifies as clearing script state and storing a status pointer. Sampled calls involved the same candidate object and two observed call sites; sampled fields immediately before the calls had depth 0, loop index 1 and active flag 1. The trace logs the first 16 calls and powers of two afterwards, not every call or its full distribution. A 55-second Release run and a 12-second disabled-trace control both ended by timeout; the control emitted no optional events. The reason for the repeated resets and their relationship to the absent menu remain unproven.

An optional bounded register trace (`GH3_TRACE_SCRIPT_SAMPLES=1`) captured 158 script-range samples between VSync ticks 302 and 1194 during a 55-second Release diagnostic. A candidate script pointer recurred; an argument sampled at `0x0028E868`, called from the script loop-comparison routine, changed from 8 to 11. This establishes changing observed inputs, not successful boot progress or an infinite loop. The trace records at most 512 samples per host thread after tick 300; a separate 12-second run with the variable unset emitted none. Both runs ended by timeout.

A subsequent 180-second Release observation reached presentation tick 3931 before timeout. After the initial blank sample, all 131 remaining presentation samples showed the same GIF counts (0,3,2), two primitive batches and 128 nonblack pixels. No instrumented MPEG events appeared. This longer observation does not prove an infinite loop or identify its cause. In the final 300 scheduler samples, PCs `0x002791E0` and `0x0027AF80` occurred 33 and 29 times; the former corresponds to a structure-cleanup routine in the decompilation reference, while the latter's semantics remain unverified.

A locally instrumented Release run reached approximately 1166 virtual VSync ticks during 55 seconds. At tick 1141, monitored GIF packet counts remained 0, 3 and 2, with two primitive batches and 128 nonblack pixels. The optional MPEG trace (`GH3_TRACE_MPEG=1`) recorded no events at its instrumented entry points; it does not cover every possible video path. The diagnostic ended by timeout. The trace is limited to 64 events per process and is disabled when the variable is unset.

A 55-second Debug run collected GIF packet, CPU primitive and presentation counters. At VSync tick 31, paths 1, 2 and 3 had submitted 0, 3 and 2 packets respectively, with two nonempty CPU primitive batches. The latched 640×448 image contained 128 pixels with a nonzero RGB channel. The same values appeared at ticks 61 and 91 while the guest scheduler continued to run. The display framebuffer was 0 and the presentation fallback selected source 70. This shows that some graphics reached the CPU backend, but it does not identify why subsequent monitored submissions stopped or establish whether the fallback source was appropriate.

The earlier invalid free was traced to the game's heap overlapping runtime callback stacks. Reserving the top MiB prevented the previously observed package terminator corruption; the bounded run passed both global archives and reached `Z_Soundcheck` without the former missing indirect-call target. The reserved region still needs a complete memory-layout audit.

An optional bounded IOP file trace (`GH3_TRACE_IOP_FILE=sfx.wad`) recorded 28 opens and 28 closes, 63 reads and 64 seeks on the matching file during a 55-second Debug run. The observed reads advanced through the file. These observations do not prove reference behavior, but the repeated opens alone are not evidence of an infinite open loop. The trace logs at most 512 events per IOP reset and is disabled when the filter is unset.

A reference PCSX2 fast boot of the supported disc logged opening FMV playback. The current native build defaults to FFmpeg-backed MPEG decoding disabled; it can be enabled at CMake configuration time, but video playback has not been validated. The standard `--sounds` extraction also omits movie files, though raw-disc reads can use the original ISO. It remains unverified whether the native execution reaches or waits for an FMV. The 55-second Debug observation advanced approximately 104 virtual VSync ticks; the temporary IOP timing allowance complicates time comparisons.

## Next investigation

1. Compare expression parsing and stack transitions around the repeated four-position sequence against an equivalent PCSX2 stage; determine the triggering status before altering guest behavior.
2. Trace startup scripts and outstanding file and audio operations alongside graphics submissions, then compare them with the reference.
3. Replace provisional IOP timing with request/response synchronization and verify no callback race remains.
4. Reach a navigable menu before testing audio, guitar controls and a full song.

Local logs and generated C++ are intentionally excluded. The developer workflow is in [BUILD.md](BUILD.md); public milestones are in the root [ROADMAP.md](../../../ROADMAP.md).
