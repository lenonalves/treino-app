# Catálogo de exercícios

Dados de texto do projeto [openGym](https://github.com/DuarteSantos8/openGym) (branch `main` na data da
importação), convertidos para um formato compacto pelo `scripts/gerar-catalogo.py`.

| Arquivo | Conteúdo |
|---|---|
| `indice.json` | 5.632 exercícios: id, nome em português, grupo, equipamento e músculo alvo (carregado ao abrir a busca) |
| `passos.json` | Passo a passo por id (carregado só ao abrir "Como fazer"). Só 1.324 têm tradução; o resto vem em inglês e o app avisa |

## Licenças — este diretório NÃO é MIT

- O catálogo do openGym é **AGPL-3.0**. As 1.324 entradas herdadas do ExerciseDB (`textSource: "exercisedb"`) têm
  nomes, músculos e instruções sob licença **MIT** (© Hasan Emir Yıldırım, via
  [hasaneyldrm/exercises-dataset](https://github.com/hasaneyldrm/exercises-dataset)).
- As traduções para pt-BR foram produzidas pelo openGym com apoio de modelos de linguagem.
- **As imagens e animações do openGym não foram incluídas de propósito.** Elas pertencem à Gym visual
  (gymvisual.com), não podem ser reutilizadas fora do openGym e não podem ser alimentadas a sistemas de IA.
  Para usar imagens aqui, é preciso licença própria.
- O restante do repositório (`index.html`, `sw.js` etc.) continua MIT. Ao redistribuir este repositório,
  mantenha este aviso junto da pasta `catalogo/`.

## Atualizar

```bash
git clone --depth 1 https://github.com/DuarteSantos8/openGym /tmp/openGym
python3 scripts/gerar-catalogo.py /tmp/openGym
```
