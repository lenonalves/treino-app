#!/usr/bin/env python3
"""Gera catalogo/ a partir de um clone do openGym (só texto, em pt-BR).

Uso: python3 scripts/gerar-catalogo.py /caminho/para/openGym
Saída: catalogo/indice.json (busca) e catalogo/passos.json (passo a passo, carregado sob demanda).
"""
import glob, json, os, sys

PARTES = {"chest":"Peito","back":"Costas","shoulders":"Ombros","upper arms":"Braços","lower arms":"Antebraços",
  "upper legs":"Coxas","lower legs":"Panturrilhas","waist":"Abdômen","neck":"Pescoço","cardio":"Cardio","full body":"Corpo todo"}
EQUIP = {"body weight":"Peso do corpo","dumbbell":"Halter","cable":"Polia","barbell":"Barra","leverage machine":"Máquina",
  "band":"Elástico","resistance band":"Elástico","kettlebell":"Kettlebell","weighted":"Com carga","suspension trainer":"Suspensão (TRX)",
  "roller":"Rolo","smith machine":"Smith","stability ball":"Bola suíça","medicine ball":"Medicine ball","ez barbell":"Barra W",
  "sled machine":"Trenó","weight plate":"Anilha","rope":"Corda","assisted":"Assistido","landmine":"Landmine","bosu ball":"Bosu",
  "sandbag":"Saco de areia","trap bar":"Barra hexagonal","olympic barbell":"Barra olímpica","stationary bike":"Bicicleta",
  "elliptical machine":"Elíptico","wheel roller":"Roda abdominal","macebell":"Macebell","tire":"Pneu","hammer":"Marreta",
  "upper body ergometer":"Ergômetro de braço","skierg machine":"SkiErg","stepmill machine":"Escada rolante"}
ALVO = {"abductors":"Abdutores","abs":"Abdômen","adductors":"Adutores","biceps":"Bíceps","calves":"Panturrilhas",
  "cardiovascular system":"Sistema cardiovascular","delts":"Deltoides","forearms":"Antebraços","glutes":"Glúteos",
  "hamstrings":"Posteriores de coxa","lats":"Dorsais","levator scapulae":"Elevador da escápula","pectorals":"Peitorais",
  "quads":"Quadríceps","serratus anterior":"Serrátil","spine":"Coluna","traps":"Trapézio","triceps":"Tríceps","upper back":"Costas altas"}

def main(raiz):
    pt = json.load(open(os.path.join(raiz, "catalogue/i18n/pt-BR.json"), encoding="utf-8"))
    indice, passos = [], {}
    for f in sorted(glob.glob(os.path.join(raiz, "catalogue/exercises/*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if "name" not in d:            # variantes femininas só apontam para o exercício original
            continue
        t = pt.get(d["id"]) or pt.get(d["id"].lstrip("0")) or {}
        nome = (t.get("name") or d["name"]).strip()
        n = int(d["id"])
        indice.append([n, nome[:1].upper() + nome[1:], d["bodyPart"], d["equipment"], d["target"]])
        # sem tradução, o passo a passo vai em inglês e é marcado como tal
        passos[n] = t["instructions"] if t.get("instructions") else {"en": d["instructions"]}
    # tabelas de rótulos vão uma vez só, no topo do arquivo
    partes, equips, alvos = (sorted({r[i] for r in indice}) for i in (2, 3, 4))
    out = {"partes": [PARTES.get(p, p) for p in partes], "equip": [EQUIP.get(e, e) for e in equips],
           "alvos": [ALVO.get(a, a) for a in alvos],
           "ex": [[r[0], r[1], partes.index(r[2]), equips.index(r[3]), alvos.index(r[4])] for r in indice]}
    os.makedirs("catalogo", exist_ok=True)
    json.dump(out, open("catalogo/indice.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump(passos, open("catalogo/passos.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(len(indice), "exercícios")

main(sys.argv[1])
