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

```mermaid
flowchart LR
    A["01 · Disc verified<br/>DONE"] --> B["02 · Native startup<br/>PARTIAL"]
    B --> C["03 · Visible menu<br/>NEXT"]
    C --> D["04 · Input + synced audio<br/>PENDING"]
    D --> E["05 · Full song + results<br/>PLAYABLE"]
    classDef done fill:#165a4c,stroke:#50d4a7,color:#fff;
    classDef partial fill:#7d5318,stroke:#f2ba57,color:#fff;
    classDef next fill:#244c7c,stroke:#74b7ff,color:#fff;
    classDef pending fill:#303743,stroke:#778293,color:#fff;
    class A done; class B partial; class C next; class D,E pending;
```

The graphic tracks observable milestones rather than an invented completion percentage. [ROADMAP.md](ROADMAP.md) defines their exit criteria.

## Source layout and build

`gh3-port/scripts/` contains local extraction, mapping and diagnostic tools; `gh3-port/src/` contains host diagnostics; `gh3-port/tests/` contains runtime checks. Runtime changes live in `ps2xIOP/` and `ps2xRuntime/`. Generated C++, disc files, logs and build outputs are excluded from Git.

This is a **Windows x64 developer prototype** requiring Visual Studio 2022 C++ tools, CMake, Git, Python 3 and a local ISO of the specified release. Follow the [build guide](gh3-port/docs/BUILD.md). A complete clean-clone build has not yet been verified.

Maintained by [Iago Gomes](https://github.com/omesis-sec), who previously published [Intel UHD port testing and documentation](https://github.com/omesis-sec/cybersecurity-portfolio/blob/main/docs/spartanport-validation.md). The [GH3 decompilation project](https://github.com/Ketbome/gh3-decomp) supplies the locally used function map; its source and game data are not redistributed here. Contributions should include reproducible observations and avoid uploading game files or personal paths.
