# Guitar Hero III · Native Windows Port

**English** · [Português (Brasil)](README.pt-BR.md) · [Español](README.es.md)

Experimental native Windows port of **Guitar Hero III: Legends of Rock** for PlayStation 2, targeting the USA/NTSC **SLUS-21672** release. The first playable milestone is one complete song with synchronized audio, input, and results.

> **Status: the prototype opens a black window. No menu or playable build has been verified.**

**You must own an original copy of the game and supply your own disc image.** This repository provides no game executable, ISO, music, video, textures, or extracted game files. This unofficial project is not affiliated with Activision, Neversoft, RedOctane, or the rights holders.

This fork uses [PS2Recomp](https://github.com/ran-j/PS2Recomp) to translate the main PS2 executable into C++ and run it with an experimental compatibility runtime. It retains the upstream history and GPL-3.0 license. Development used OpenAI Codex for code, analysis, and documentation; results below come from local tests and require independent validation.

## Verified progress

| Area | Result |
| --- | --- |
| Disc | Local `SLUS_216.72` executable matched the expected SHA-1. |
| Translation | Hybrid map generated 9,822 entries, including 84 runtime stubs. |
| Startup | Debug build loaded IOP modules and read game archives and scripts. |
| Memory | IOP allocator test passed 50,000 allocate/free cycles. |
| Display | Last observed 55-second launch remained active, with a black window. No menu or song confirmed. |

IOP timing and early file callbacks are currently approximations. Graphics, audio, input, and timing remain open engineering work. See [technical status](gh3-port/docs/TECHNICAL_STATUS.md).

## Road to playable

![A five-stage roadmap to a first playable song, with an estimated 15% overall progress and a 10–20% uncertainty range. Disc verification is done, startup is partial, and menu, rhythm input, audio and a full song remain open.](docs/images/road-to-playable.en.svg)

**15% is a subjective engineering estimate**, with a plausible 10–20% range. It is based on verified disc identification and partial native startup; rendering, menu navigation, synchronized audio, input and a complete song have not been demonstrated. It is not a code-coverage measurement or delivery forecast. [ROADMAP.md](ROADMAP.md) defines the test required for each milestone.

## Source layout and build

`gh3-port/scripts/` contains local extraction, mapping and diagnostic tools; `gh3-port/src/` contains host diagnostics; `gh3-port/tests/` contains runtime checks. Runtime changes live in `ps2xIOP/` and `ps2xRuntime/`. Generated C++, disc files, logs and build outputs are excluded from Git.

This is a **Windows x64 developer prototype** requiring Visual Studio 2022 C++ tools, CMake, Git, Python 3 and a local ISO of the specified release. Follow the [build guide](gh3-port/docs/BUILD.md). A complete clean-clone build has not yet been verified.

Maintained by [Iago Gomes](https://github.com/omesis-sec), who previously published [Intel UHD port testing and documentation](https://github.com/omesis-sec/cybersecurity-portfolio/blob/main/docs/spartanport-validation.md). The [GH3 decompilation project](https://github.com/Ketbome/gh3-decomp) supplies the locally used function map; its source and game data are not redistributed here. Contributions should include reproducible observations and avoid uploading game files or personal paths.

## Legal notice

This is an independent, unofficial preservation and interoperability project. Neither the project nor its maintainer is affiliated with, sponsored by, endorsed by, or acting on behalf of any game developer, publisher, platform company or other rights holder, including Activision, Neversoft, Budcat Creations, RedOctane and Sony Interactive Entertainment. Game titles, company names and trademarks are used only to identify the game and belong to their respective owners.

This repository does not provide, host or distribute the game, a disc image, its executable, music, videos, textures or other proprietary game data. To use the project, you must supply a lawfully obtained original copy of the supported PlayStation 2 release and prepare your own local game files in accordance with applicable law. The maintainer does not supply game copies or assist in obtaining unauthorized copies. The code and documentation are provided for research and development; no playable release is currently offered.
