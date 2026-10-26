# Catálogo de exercícios

Dados de texto do projeto [openGym](https://github.com/DuarteSantos8/openGym) (branch `main` na data da
importação), convertidos para um formato compacto pelo `scripts/gerar-catalogo.py`.

| Arquivo | Conteúdo |
|---|---|
| `indice.json` | 5.841 exercícios: id, nome em português, grupo, equipamento e músculo alvo (carregado ao abrir a busca) |
| `img/` | 536 imagens WebP: as duas poses (`<n>-0` e `<n>-1`) de 268 desenhos do Everkinetic, que o app alterna para animar o movimento |
| `passos.json` | Passo a passo por id (carregado só ao abrir "Como fazer"). Só 1.324 têm tradução; o resto vem em inglês e o app avisa |

## Licenças — este diretório NÃO é MIT

- O catálogo do openGym é **AGPL-3.0**. As 1.324 entradas herdadas do ExerciseDB (`textSource: "exercisedb"`) têm
  nomes, músculos e instruções sob licença **MIT** (© Hasan Emir Yıldırım, via
  [hasaneyldrm/exercises-dataset](https://github.com/hasaneyldrm/exercises-dataset)).
- As traduções para pt-BR foram produzidas pelo openGym com apoio de modelos de linguagem.
- **Desenhos (`img/`): [Everkinetic](https://everkinetic.com), de Greg Priday, licença
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)** (conforme o repositório
  [everkinetic/data](https://github.com/everkinetic/data)). Foram convertidos para WebP, recortados e reduzidos
  a 320 px; o app mostra o crédito junto ao desenho. Quem reutilizar esses arquivos precisa manter o crédito e
  compartilhá-los sob a mesma licença. Outros projetos que usam o Everkinetic citam a versão 3.0 da licença.
  268 exercícios têm desenho: 59 ligados a exercícios do openGym (pelo nome) e 209 exercícios próprios do
  Everkinetic (ids a partir de 100001), cujos nomes em português foram traduzidos em
  `scripts/everkinetic-nomes.json` e cujo passo a passo está em inglês.
- **As imagens e animações do openGym não foram incluídas de propósito.** Elas pertencem à Gym visual
  (gymvisual.com), não podem ser reutilizadas fora do openGym e não podem ser alimentadas a sistemas de IA.
  Para usar imagens aqui, é preciso licença própria.
- O restante do repositório (`index.html`, `sw.js` etc.) continua MIT. Ao redistribuir este repositório,
  mantenha este aviso junto da pasta `catalogo/`.

## Atualizar

```bash
git clone --depth 1 https://github.com/DuarteSantos8/openGym /tmp/openGym
git clone --depth 1 https://github.com/everkinetic/data /tmp/everkinetic
python3 scripts/gerar-catalogo.py /tmp/openGym /tmp/everkinetic   # precisa do ImageMagick (`convert`)
```
