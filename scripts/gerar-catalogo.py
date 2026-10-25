#!/usr/bin/env python3
"""Gera catalogo/ a partir de clones do openGym (texto, pt-BR) e do Everkinetic (desenhos).

Uso: python3 scripts/gerar-catalogo.py /caminho/para/openGym /caminho/para/everkinetic-data
Saída: catalogo/indice.json (busca), catalogo/passos.json (passo a passo, carregado sob demanda)
       e catalogo/img/<n>-0.webp, <n>-1.webp (duas poses de cada desenho, requer ImageMagick `convert`).

Os desenhos do Everkinetic (CC BY-SA) entram de duas formas: quando o nome bate com um exercício do openGym,
o desenho é ligado a ele; os demais viram exercícios novos (id 100000 + número), com nome traduzido em
scripts/everkinetic-nomes.json.
"""
import glob, json, os, re, subprocess, sys

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

EK_EQUIP = {"barbell":"barbell","barbell or dumbbell":"barbell","dumbbell":"dumbbell","dumbbells":"dumbbell","dumbell":"dumbbell",
  "cable":"cable","cable machine":"cable","v-bar":"cable","machine":"leverage machine","chest machine":"leverage machine",
  "bench press machine":"leverage machine","t-bar machine":"leverage machine","smith machine":"smith machine",
  "exercise band":"band","bands":"band","band":"band","exercise ball":"stability ball","swiss ball":"stability ball",
  "stability ball":"stability ball","bosu ball":"bosu ball","medicine ball":"medicine ball","weight plate":"weight plate",
  "weight":"weight plate","body":"body weight"}
# (bodyPart, target) por palavra do músculo principal do Everkinetic; a primeira que aparecer vence
EK_MUSCULO = [("neck",("neck","levator scapulae")),("chest",("chest","pectorals")),("triceps",("upper arms","triceps")),
  ("biceps",("upper arms","biceps")),("arms",("upper arms","biceps")),("quadriceps",("upper legs","quads")),
  ("hamstring",("upper legs","hamstrings")),("glut",("upper legs","glutes")),("deltoid",("shoulders","delts")),
  ("shoulder",("shoulders","delts")),("abdominal",("waist","abs")),("core",("waist","abs")),("oblique",("waist","abs")),
  ("calves",("lower legs","calves")),("lower back",("back","spine")),("lats",("back","lats")),("back",("back","upper back")),
  ("trapezius",("back","traps"))]

# quando a lista de equipamentos vem vazia ou só "body", o título costuma dizer (ex.: "Dead Lifts Smith Machine")
EK_NO_TITULO = [("smith","smith machine"),("machine","leverage machine"),("dumbbell","dumbbell"),("barbell","barbell"),
  ("cable","cable"),("band","band"),("stability ball","stability ball")]

def ek_campos(e):
    musc = (e.get("primary") or "chest").lower()      # único sem músculo é uma flexão de braço
    parte, alvo = next(v for k, v in EK_MUSCULO if k in musc)
    mapeados = [EK_EQUIP[q] for q in e.get("equipment", []) if q in EK_EQUIP]
    do_titulo = next((v for k, v in EK_NO_TITULO if k in e["title"].lower()), None)
    equip = next((q for q in mapeados if q != "body weight"), do_titulo or "body weight")
    return parte, equip, alvo

def toks(txt):
    t = re.findall(r"[a-z0-9]+", txt.lower().replace("-", " ").replace("\u2019", "").replace("'", ""))
    return frozenset(w[:-1] if w.endswith("s") and len(w) > 3 else w for w in t)

def imagens(ek_raiz, n):
    os.makedirs("catalogo/img", exist_ok=True)
    for i, pose in enumerate(("relaxation", "tension")):
        subprocess.run(["convert", f"{ek_raiz}/dist/png/{n}-{pose}.png", "-background", "white", "-alpha", "remove",
          "-trim", "+repage", "-resize", "320x320", "-bordercolor", "white", "-border", "8", "-quality", "70",
          f"catalogo/img/{n}-{i}.webp"], check=True, stderr=subprocess.DEVNULL)

def main(raiz, ek_raiz):
    pt = json.load(open(os.path.join(raiz, "catalogue/i18n/pt-BR.json"), encoding="utf-8"))
    indice, passos, porNome = [], {}, {}
    for f in sorted(glob.glob(os.path.join(raiz, "catalogue/exercises/*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if "name" not in d:            # variantes femininas só apontam para o exercício original
            continue
        t = pt.get(d["id"]) or pt.get(d["id"].lstrip("0")) or {}
        nome = (t.get("name") or d["name"]).strip()
        n = int(d["id"])
        indice.append([n, nome[:1].upper() + nome[1:], d["bodyPart"], d["equipment"], d["target"], ""])
        # sem tradução, o passo a passo vai em inglês e é marcado como tal
        passos[n] = t["instructions"] if t.get("instructions") else {"en": d["instructions"]}
        porNome.setdefault(toks(d["name"]), []).append(indice[-1])

    nomes = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "everkinetic-nomes.json"), encoding="utf-8"))
    usados = set()
    ek = json.load(open(os.path.join(ek_raiz, "exercises.json"), encoding="utf-8"))
    ids = {e["id_num"]: sum(1 for x in ek if x["id_num"] == e["id_num"]) for e in ek}
    for e in ek:
        # o id_num do exercises.json se repete (0020), então o desenho vem do que o .md do exercício referencia
        md = os.path.join(ek_raiz, "dist/md", e["name"] + ".md")
        ref = re.search(r"svg/(\d{4})-relaxation", open(md, encoding="utf-8").read()) if os.path.exists(md) else None
        n = ref.group(1) if ref else (e["id_num"] if ids[e["id_num"]] == 1 else None)
        if not n or not all(os.path.exists(f"{ek_raiz}/dist/png/{n}-{p}.png") for p in ("relaxation", "tension")):
            continue
        if n in usados:                               # dois exercícios do Everkinetic apontam para o mesmo desenho
            continue
        usados.add(n)
        k = toks(e["title"])
        achado = porNome.get(k) or next((porNome[k | toks(q)] for q in e.get("equipment", []) if k | toks(q) in porNome), None)
        if achado and achado[0][5]:                   # esse exercício do openGym já tem outro desenho
            continue
        if achado:
            achado[0][5] = n                          # liga o desenho ao exercício do openGym
        else:
            parte, equip, alvo = ek_campos(e)
            indice.append([100000 + int(n), nomes[n], parte, equip, alvo, n])
            passos[100000 + int(n)] = {"en": e["steps"]}
        imagens(ek_raiz, n)

    # tabelas de rótulos vão uma vez só, no topo do arquivo
    partes, equips, alvos = (sorted({r[i] for r in indice}) for i in (2, 3, 4))
    out = {"partes": [PARTES.get(p, p) for p in partes], "equip": [EQUIP.get(e, e) for e in equips],
           "alvos": [ALVO.get(a, a) for a in alvos],
           "ex": [[r[0], r[1], partes.index(r[2]), equips.index(r[3]), alvos.index(r[4]), r[5]] for r in indice]}
    os.makedirs("catalogo", exist_ok=True)
    json.dump(out, open("catalogo/indice.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump(passos, open("catalogo/passos.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(len(indice), "exercícios,", sum(1 for r in indice if r[5]), "com desenho")

main(sys.argv[1], sys.argv[2])
