# Treino 12 Semanas

App de ficha de treino que instala no celular. Registra repetições e carga série
a série, compara com a semana anterior e acompanha medidas corporais num painel
estilo HUD de jogo.

**[→ Abrir o app](https://lenonalves.github.io/treino-app/)**

<!-- Depois de publicar, tire um print da tela inicial no celular, arraste a
     imagem para dentro desta linha ao editar o README pelo próprio GitHub
     (ele hospeda a imagem sozinho) e apague este comentário. -->

## O que ele faz

- **Trilha semanal** — os treinos da semana em cards, com progresso de séries em cada um.
- **Registro série a série** — repetições e carga com botões de +/−, marcação de série
  concluída e cronômetro de descanso automático.
- **Memória de carga** — cada série mostra o que você fez na mesma série da semana passada.
- **Editor de plano** — renomear exercícios, mudar séries, adicionar ou remover, definir
  a duração do ciclo. Ao terminar a periodização, o ciclo vai para o histórico e um novo começa.
- **Catálogo de exercícios** — busca entre 5.632 exercícios em português (por nome, músculo, equipamento ou
  grupo muscular) ao adicionar ou trocar exercícios no plano, e um painel *Como fazer* com o passo a passo
  na tela do exercício. Baixado só quando você abre a busca e depois funciona offline.
- **Aba Corpo** — peso, percentual de gordura e nove medidas exibidas sobre um boneco,
  com a variação em relação à avaliação anterior.
- **XP e ofensiva** — porque terminar a série rende mais quando tem número subindo.
- **Funciona offline** e guarda tudo no próprio aparelho.

## Como foi feito

HTML, CSS e JavaScript puros, num arquivo só — sem framework, sem build, sem
dependência. Instalável como PWA (`manifest.webmanifest` + service worker) e os
dados ficam no `localStorage`.

| Arquivo | Função |
|---|---|
| `index.html` | O app inteiro: interface, estilos e lógica |
| `manifest.webmanifest` | Nome, ícone e cores do app instalado |
| `sw.js` | Cache para funcionar sem internet |
| `catalogo/` | Catálogo de exercícios (dados do [openGym](https://github.com/DuarteSantos8/openGym), [licença própria](catalogo/LEIAME.md)) |
| `scripts/gerar-catalogo.py` | Regera o catálogo a partir de um clone do openGym |
| `icon-*.png` | Ícones da tela de início |

## Rodar localmente

```bash
python3 -m http.server 8000
```

E abrir `http://localhost:8000`. Abrir o `index.html` direto também mostra a
interface, mas o service worker só liga em `http(s)`.

## Instalar no celular

- **iPhone:** abra o link no Safari → Compartilhar → *Adicionar à Tela de Início*
- **Android:** abra no Chrome → menu ⋮ → *Instalar app*

## Limitações conhecidas

- Os dados ficam só no aparelho: limpar os dados do navegador apaga o histórico.
- Sem sincronização entre dispositivos (a fazer).

## Licença

MIT para o app. A pasta `catalogo/` vem do openGym (AGPL-3.0 e MIT) e tem as condições descritas em
[`catalogo/LEIAME.md`](catalogo/LEIAME.md).
