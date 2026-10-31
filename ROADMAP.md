# Guitar Hero III native port · Milestones

Progress is measured by reproducible behavior, not by the number of translated functions. A generated executable is not itself a playable port.

The README visual shows a **subjective 15% estimate toward the first playable build** (plausible range: 10–20%). This reflects a verified disc and partial startup, while visible menus, synchronized audio, input and a complete song remain unverified. It is neither code coverage nor a schedule; revise it when a milestone is demonstrated.

| Milestone | State | Completion test |
| --- | --- | --- |
| Supported disc identified | Done | SLUS-21672 ELF hash matches the known build. |
| Native startup | Partial | Recompiled EE code starts, loads required IOP modules and archives, and runs without a critical loop or collision. Current Debug launches satisfy only part of this. |
| Visible, navigable menu | Next | Cold boot shows a menu and input can select a song repeatedly. |
| Audio and gameplay input | Pending | Music, note timing, rendering and controls remain synchronized in a selected song. |
| First playable build | Pending | Complete one song, display results and return to menu without crashing. |
| Compatibility release | Later | Test broader song/mode coverage, saves, controllers and performance on multiple PCs. |

Current priorities: investigate repeated script state resets against a reference; trace whether execution reaches the opening video; replace provisional IOP timing with correct synchronization; validate memory boundaries and file requests. A 180-second Release run reached presentation tick 3931 with no later change in monitored graphics submissions; this does not establish a boot deadlock or playability.
