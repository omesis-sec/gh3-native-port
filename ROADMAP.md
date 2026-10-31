# Guitar Hero III native port · Milestones

Progress is measured by reproducible behavior, not by the number of translated functions. A generated executable is not itself a playable port.

| Milestone | State | Completion test |
| --- | --- | --- |
| Supported disc identified | Done | SLUS-21672 ELF hash matches the known build. |
| Native startup | Partial | Recompiled EE code starts, loads required IOP modules and archives, and runs without a critical loop or collision. Current Debug launches satisfy only part of this. |
| Visible, navigable menu | Next | Cold boot shows a menu and input can select a song repeatedly. |
| Audio and gameplay input | Pending | Music, note timing, rendering and controls remain synchronized in a selected song. |
| First playable build | Pending | Complete one song, display results and return to menu without crashing. |
| Compatibility release | Later | Test broader song/mode coverage, saves, controllers and performance on multiple PCs. |

Current priorities: determine why rendering stays black; compare the execution with a reference; replace provisional IOP timing with correct synchronization; validate memory boundaries and file requests. Avoid presenting the current 55-second run as evidence of playability.
