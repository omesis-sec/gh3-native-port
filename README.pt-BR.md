# Guitar Hero III · Port nativo para Windows

[English](README.md) · **Português (Brasil)** · [Español](README.es.md)

Port nativo experimental de **Guitar Hero III: Legends of Rock** para PlayStation 2, voltado à edição USA/NTSC **SLUS-21672**. O primeiro marco jogável será completar uma música com áudio sincronizado, entrada e resultado.

> **Estado: o protótipo abre uma janela preta. Ainda não há menu nem build jogável verificados.**

**Você precisa possuir uma cópia original do jogo e fornecer sua própria imagem do disco.** Este repositório não fornece executável, ISO, músicas, vídeos, texturas ou arquivos extraídos do jogo. O projeto é não oficial e não tem vínculo com Activision, Neversoft, RedOctane ou os titulares dos direitos.

Este fork usa [PS2Recomp](https://github.com/ran-j/PS2Recomp) para traduzir o executável principal do PS2 em C++ e executá-lo com um runtime experimental de compatibilidade. O histórico original e a licença GPL-3.0 são preservados. O desenvolvimento utilizou OpenAI Codex em código, análise e documentação; os resultados abaixo vêm de testes locais e exigem validação independente.

## Progresso verificado

| Área | Resultado |
| --- | --- |
| Disco | O executável local `SLUS_216.72` coincidiu com o SHA-1 esperado. |
| Tradução | O mapa híbrido gerou 9.822 entradas, incluindo 84 stubs do runtime. |
| Inicialização | A build Debug carregou módulos IOP, arquivos e scripts do jogo. |
| Memória | O teste do alocador IOP passou em 50 mil ciclos de alocação/liberação. |
| Tela | A última execução observada durou 55 segundos, com janela preta. Não há menu ou música confirmados. |

A temporização do IOP e as respostas antecipadas de abertura ainda são aproximações. Gráficos, áudio, entrada e sincronização continuam pendentes. Consulte as [notas técnicas](gh3-port/docs/TECHNICAL_STATUS.md).

## Caminho até uma versão jogável

![Gráfico com cinco etapas até uma música jogável: estimativa geral de 15%, faixa de incerteza de 10–20%; disco verificado, inicialização parcial e tela, ritmo e música completa pendentes.](docs/images/road-to-playable.pt-BR.svg)

**15% é uma estimativa técnica subjetiva**, com faixa plausível de 10–20%. Ela considera a identificação do disco e a inicialização nativa parcial; ainda não foram demonstrados imagem, menu, áudio sincronizado, entrada ou uma música completa. Não mede cobertura de código nem prevê uma data de entrega. [ROADMAP.md](ROADMAP.md) define os testes de cada marco.

## Estrutura e compilação

`gh3-port/scripts/` contém extração local, mapas e diagnósticos; `gh3-port/src/` contém diagnósticos do host; `gh3-port/tests/` contém verificações do runtime. As alterações do runtime ficam em `ps2xIOP/` e `ps2xRuntime/`. Código gerado, dados do disco, logs e compilações ficam fora do Git.

Este é um **protótipo para desenvolvedores em Windows x64**. Requer Visual Studio 2022 com C++, CMake, Git, Python 3 e uma ISO local da edição indicada. Siga o [guia de compilação](gh3-port/docs/BUILD.md). Ainda não foi validada uma compilação completa de um clone limpo.

Mantido por [Iago Gomes](https://github.com/omesis-sec), que já publicou [testes e documentação de port em Intel UHD](https://github.com/omesis-sec/cybersecurity-portfolio/blob/main/docs/spartanport-validation.md). O [projeto de descompilação de GH3](https://github.com/Ketbome/gh3-decomp) fornece o mapa de funções usado localmente; seu código e os dados do jogo não são redistribuídos aqui. Contribuições devem trazer observações reproduzíveis, sem arquivos do jogo ou caminhos pessoais.

## Aviso legal

Este é um projeto independente e não oficial de preservação e interoperabilidade. Nem o projeto nem seu mantenedor são afiliados, patrocinados, endossados ou representam qualquer desenvolvedora, editora, fabricante de plataforma ou outro titular de direitos, incluindo Activision, Neversoft, Budcat Creations, RedOctane e Sony Interactive Entertainment. Títulos, nomes de empresas e marcas são usados apenas para identificar o jogo e pertencem a seus respectivos titulares.

Este repositório não fornece, hospeda ou distribui o jogo, sua imagem de disco, executável, músicas, vídeos, texturas ou outros dados proprietários. Para usar o projeto, você precisa possuir uma cópia original adquirida legalmente da edição de PlayStation 2 compatível e preparar seus próprios arquivos locais conforme a legislação aplicável. O mantenedor não fornece cópias do jogo nem auxilia na obtenção de cópias não autorizadas. O código e a documentação destinam-se a pesquisa e desenvolvimento; atualmente não há versão jogável disponível.
