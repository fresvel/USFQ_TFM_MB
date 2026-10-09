"""Versión 5 de la defensa (09/10/2026): integra en el guion los cambios hechos a mano en slides.com (deck 3695765,
editado el 08/10/2026), los normaliza al estilo USFQ del motor (títulos numerados en la banda, pie con «· USFQ»,
numeración automática, viñetas reales, citas abajo a la derecha) y actualiza los datos a la tesis corregida del
09/10/2026 (21 muestras de SARS-CoV-2 secuenciadas, VP1 y no VP4 en enterovirus, RSV sin lecturas del virus,
linajes descendientes de JN.1 con Freyja, ARN a −80 °C, quince barrios).
Entrada: defensa_tfm_v4.yaml, figuras_v5/ (figuras_slides.py y las imágenes bajadas del deck en figuras_v5/slides).
Salida: defensa_tfm_v5.yaml."""
import copy
import csv
import re
from pathlib import Path

import yaml
from PIL import Image

AQUI = Path(__file__).resolve().parent
DATOS = AQUI.parent / "Latex/assets/datos"
F5 = "figuras_v5"
SL = f"{F5}/slides"
NEG, GRIS, ROJO, CREMA, BEIGE = "negro_usfq", "gris_usfq", "rojo", "crema", "beige"
X0, X1, Y0, Y1 = 70, 1210, 132, 630

v4 = yaml.safe_load(open(AQUI / "defensa_tfm_v4.yaml", encoding="utf-8"))
D4 = v4["diapositivas"]


def d4(n):
    return copy.deepcopy(D4[n - 1])


def P(t, b=False, a="left"):
    return f'<p style="text-align:{a}">{f"<strong>{t}</strong>" if b else t}</p>'


def UL(items):
    return "<ul>" + "".join(f'<li style="text-align:left">{i}</li>' for i in items) + "</ul>"


def texto(x, y, w, html, tam=70, color=NEG):
    return {"tipo": "texto", "x": x, "y": y, "w": w, "html": html, "tam": tam, "color": color}


def imagen(ruta, caja):
    """Imagen ajustada a la caja (x, y, w, h) sin deformarla, centrada."""
    x, y, w, h = caja
    with Image.open(AQUI / ruta) as im:
        nw, nh = im.size
    k = min(w / nw, h / nh)
    iw, ih = round(nw * k), round(nh * k)
    return {"tipo": "imagen", "imagen": ruta, "x": round(x + (w - iw) / 2), "y": round(y + (h - ih) / 2),
            "w": iw, "h": ih}


def lienzo(numero, titulo, elementos, notas=None, cita=None):
    d = {"diseno": "lienzo", "titulo": titulo, "elementos": elementos}
    if numero:
        d["numero"] = numero
    if cita:
        d["cita"] = cita
    if notas:
        d["notas"] = notas
    return d


def html_txt(e):
    return re.sub(r"<[^>]+>", "", str(e.get("html") or e.get("contenido") or ""))


def reemplazar(d, viejo, nuevo):
    """Reemplaza texto dentro del html/contenido de los elementos de un lienzo."""
    n = 0
    for e in d["elementos"]:
        for k in ("html", "contenido"):
            if e.get(k) and viejo in e[k]:
                e[k] = e[k].replace(viejo, nuevo)
                n += 1
    assert n, f"no se encontró «{viejo}»"


S = []

# 1 · portada (igual)
S.append(d4(1))

# 2 · índice: títulos y descripciones según la tesis corregida y la estructura actual del deck
d = d4(2)
d["items"][4]["texto"] = "Coxsackievirus A1 en la región VP1"
d["items"][5] = {"titulo": "Resultados III: virus sincitial respiratorio",
                 "texto": "Sin lecturas del virus y muestras retrospectivas"}
d["items"][6] = {"titulo": "Limitaciones", "texto": "Matriz, conservación, diseño temporal y controles"}
S.append(d)

# 3 · vigilancia: sin la línea «Cada paso filtra», segunda fila más abajo e ilustración de la PTAR (cambios del deck)
d = d4(3)
d["elementos"] = [e for e in d["elementos"] if not html_txt(e).startswith("Cada paso filtra")]
for e in d["elementos"]:
    yy = e.get("y", e.get("y1"))
    if html_txt(e) == "Aguas residuales":
        e["y"] = 352
    elif yy is not None and 400 <= yy <= 460:
        for k in ("y", "y1", "y2"):
            if k in e:
                e[k] += 22
    elif html_txt(e).startswith("con y sin síntomas"):
        e["y"] = 550
d["elementos"].append(imagen(f"{SL}/13094702.png", (712, 262, 196, 168)))
S.append(d)

# 4 · antecedente: quince barrios y caudal promedio (tesis); mapa del Ecuador junto a las barras (deck)
d = d4(4)
reemplazar(d, "<strong>11</strong>", "<strong>15</strong>")
reemplazar(d, "caudal del influente", "caudal promedio del influente")
d["elementos"].append(imagen(f"{SL}/13094830_c0.png", (690, 470, 150, 150)))
d["notas"] = ("Esta tesis parte de ese sitio centinela ya validado y lo amplía a otros virus. (1 min)\n"
              "Mejía Calle (2024) instaló un muestreo pasivo semanal de 24 h con un dispositivo impreso en 3D en el "
              "influente de la PTAR Quitumbe, en el sur de Quito, que recibe las aguas residuales de quince barrios y "
              "reportó un caudal de 75 L/s. Ese estudio detectó JN.1 en el agua antes de su identificación clínica. "
              "Ecuador depositó 5 102 genomas de SARS-CoV-2 en 2022 y solo 744 en 2024 (Bruno et al., 2025), y no hay "
              "datos ambientales ecuatorianos de RSV ni de poliovirus.")
S.append(d)

# 5 · por qué estos tres virus (igual)
S.append(d4(5))

# 6–8 · fichas de cada virus (agregadas en el deck): título numerado, viñetas reales y citas al pie
S.append(lienzo("01", "SARS-CoV-2", [
    texto(X0, 138, 470, UL(["ARN monocatenario de sentido positivo (+ssRNA), 30 kb",
                            "Proteínas espícula (S), nucleocápside (N), envoltura (E) y membrana (M)",
                            "Receptor: enzima convertidora de angiotensina 2 (ACE2)",
                            "Mutaciones de la espícula: D614G, N501Y y E484K"]), 84),
    imagen(f"{SL}/13094711.png", (560, 134, 650, 236)),
    imagen(f"{SL}/13094777.png", (X0, 392, 380, 232)),
    imagen(f"{SL}/13094741.png", (470, 384, 740, 240)),
], cita="Lamers & Haagmans (2022); Aguilar-Gamboa et al. (2021); Bergmann & Silverman (2020)"))

S.append(lienzo("01", "Poliovirus", [
    texto(X0, 136, 480, UL(["Especie <em>Enterovirus C</em>; tres serotipos salvajes: WPV1, WPV2 y WPV3",
                            "Transmisión fecal-oral y respiratoria",
                            "GPEI (1988): erradicación de WPV2 y WPV3",
                            "WPV1: endémico en Afganistán y Pakistán",
                            "VDPV: poliovirus derivado de la vacuna"]), 82),
    imagen(f"{SL}/13092980_c0.png", (575, 132, 635, 262)),
    imagen(f"{SL}/13094231.png", (X0, 432, 520, 96)),
    imagen(f"{SL}/13094229.png", (X0, 532, 520, 96)),
    texto(640, 404, 570, P("Replicación del enterovirus A71", True, "center"), 58, GRIS),
    imagen(f"{SL}/13094230_c0.png", (640, 436, 570, 192)),
], cita="Mbani et al. (2023); Feferbaum-Leite et al. (2023)"))

S.append(lienzo("01", "Virus sincitial respiratorio", [
    imagen(f"{SL}/13095055.png", (X0, 136, 600, 84)),
    texto(700, 136, 510, UL(["Infecta las células del tracto respiratorio humano",
                             "Dos glicoproteínas principales: G y F",
                             "ARN de cadena negativa, 15 kb",
                             "Dos subgrupos: A y B",
                             "Sin datos ambientales de RSV en Ecuador"]), 82),
    imagen(f"{SL}/13094979.png", (X0, 228, 470, 260)),
    imagen(f"{SL}/13095047_c35.png", (X0, 494, 250, 134)),
    imagen(f"{SL}/13095049_c0.png", (560, 398, 650, 230)),
], cita="Jung et al. (2020); Zhang et al. (2025); CDC (2026)"))

# 9–10 · pregunta y objetivos (iguales)
S.append(d4(6))
S.append(d4(7))

# 11 · metodología (el deck renombró «Flujo multipatógeno» y quitó la leyenda de colores)
d = d4(10)
d["titulo"] = "Metodología"
d["elementos"] = [e for e in d["elementos"] if not html_txt(e).startswith("Azul: etapas comunes")]
S.append(d)

# 12 · muestreo pasivo con la nueva figura de fotos del procedimiento (deck); viñetas con el estilo del v4
d = d4(9)
d["imagen"] = f"{SL}/13097111.png"
d["ancho"] = 800
d["notas"] = d["notas"].replace("antes de cualquier tratamiento", "antes del pretratamiento")
S.append(d)

# 13–15 · preconcentración, extracción y RT-qPCR (agregadas en el deck)
S.append({"diseno": "imagen", "numero": "03", "titulo": "Preconcentración viral", "imagen": f"{SL}/13097252_c11.png"})
S.append({"diseno": "imagen", "numero": "03", "titulo": "Extracción de ARN", "imagen": f"{SL}/13097118_c28.png"})
S.append(lienzo("03", "RT-qPCR de SARS-CoV-2", [
    imagen(f"{SL}/13097256_c7.png", (X0, 160, 500, 280)),
    imagen(f"{SL}/13097620.png", (330, 450, 240, 34)),
    {"tipo": "tabla", "x": 600, "y": 170, "w": 610, "tam": 64,
     "encabezados": ["Blanco", "Región del genoma", "Amplicón", "Fluoróforo"],
     "filas": [["N1", "~28\u00a0287–28\u00a0358 (inicio del gen N)", "~72 pb", "HEX"],
               ["N2", "~29\u00a0164–29\u00a0230 (final del gen N)", "~67 pb", "FAM"],
               ["RNasa P humana", "ARNm del gen RPP30", "~65 pb", "Cy5"]]},
], cita="New England Biolabs (2021)"))

# 16 · selección y controles (el deck cambió la última caja y quitó la línea de introducción)
d = d4(11)
d["elementos"] = [e for e in d["elementos"] if not html_txt(e).startswith("Una muestra pasa")]
for e in d["elementos"]:
    if "Nanopore R10.4.1" in str(e.get("contenido") or e.get("html") or ""):
        e[("contenido" if "contenido" in e else "html")] = re.sub(r"Nanopore R10\.4\.1", "Secuenciación ONT",
                                                                    e.get("contenido") or e.get("html"))
S.append(d)

# 17 · amplificación multiplex de SARS-CoV-2 (agregada en el deck; la misma figura en dos recortes)
S.append(lienzo("03", "Amplificación de SARS-CoV-2", [
    texto(X0, 138, 1140, P("PCR multiplex por amplicones en mosaico (ARTIC V3 y VarSkip)", True), 76),
    imagen(f"{SL}/13097613_c0.png", (X0, 192, 500, 430)),
    texto(588, 380, 60, P("+", True, "center"), 160, NEG),
    imagen(f"{SL}/13097614_c53.png", (690, 200, 520, 420)),
], cita="New England Biolabs (2021)"))

# 18 · enterovirus y RSV (vacía en el deck: «Poliovirus y RSV»); contenido de la metodología de la tesis
S.append({"diseno": "columnas", "numero": "03", "titulo": "Enterovirus y RSV",
          "columnas": [
              {"titulo": "Enterovirus: PCR anidada de VP1",
               "texto": ["1.ª ronda: cebadores pan-enterovirus (5'NTR y Cre)",
                         "2.ª ronda: región VP1 con Y7 y Q8",
                         "Protocolo DDNS de detección directa por Nanopore"]},
              {"titulo": "RSV: PCR multiplex ARTIC RSV",
               "texto": ["Amplicones de ~400 pb en dos pools por subgrupo (A y B)",
                         "ARN diluido y sin diluir, por duplicado",
                         "Selección solo por bandas: sin RT-qPCR de RSV"]}],
          "cita": "Arita et al. (2015); Shaw et al. (2020); Maloney et al. (2025)",
          "notas": ("Enterovirus siguió el protocolo DDNS de detección directa de poliovirus por secuenciación "
                    "Nanopore: una PCR anidada cuya primera ronda usa cebadores pan-enterovirus de las regiones "
                    "5'NTR y Cre, y la segunda amplifica VP1 con los cebadores Y7 y Q8. VP1 es la región que "
                    "distingue poliovirus Sabin, salvaje y derivado de la vacuna. RSV se intentó con el esquema "
                    "ARTIC RSV, amplicones de unos 400 pb en dos pools por subgrupo, por duplicado con ARN diluido y "
                    "sin diluir. Como RSV no tuvo RT-qPCR, la selección para secuenciar dependió solo de las bandas "
                    "del gel. (1 min)")})

# 19 · secuenciación ONT (vacía en el deck); contenido de la metodología de la tesis
S.append({"diseno": "columnas", "numero": "03", "titulo": "Secuenciación ONT",
          "columnas": [
              {"titulo": "Bibliotecas",
               "texto": ["Native Barcoding Kit 96 V14 (SQK-NBD114.96)",
                         "Reparación de extremos, código de barras por muestra y adaptadores",
                         "Celdas R10.4.1 · MinKNOW y Dorado"]},
              {"titulo": "Análisis",
               "texto": ["SARS-CoV-2: EPI2ME wf-artic, Nextclade y Freyja",
                         "Enterovirus: minimap2 contra la especie C, BLAST y árbol de VP1",
                         "RSV: minimap2 contra RSV-A y RSV-B"]}],
          "cita": "Oxford Nanopore Technologies (2025); Aksamentov et al. (2021); Karthikeyan et al. (2022)",
          "notas": ("Los amplicones se secuenciaron con el Native Barcoding Kit 96 V14 en celdas R10.4.1: reparación "
                    "de extremos, un código de barras por muestra, agrupación y ligación de adaptadores. MinKNOW y "
                    "Dorado hicieron el basecalling y la demultiplexación. Para SARS-CoV-2, EPI2ME generó los "
                    "consensos, Nextclade asignó clado y linaje, y Freyja estimó la mezcla de linajes. Para "
                    "enterovirus, las lecturas se alinearon contra un panel de la especie C, el consenso de VP1 se "
                    "comparó con BLAST y se contrastó con un árbol de máxima verosimilitud. Para RSV, las lecturas "
                    "se alinearon contra RSV-A y RSV-B. (1 min)")})

# 20 · total de muestras analizadas (deck: nuevo título y frase final)
d = d4(8)
d["titulo"] = "Total de muestras analizadas"
d["texto"] = (str(d.get("texto") or "").rstrip() + "\n\nEn total se analizaron 22 muestras para enterovirus y para RSV.")
S.append(d)

# 21 · resultados: rendimiento con las cifras de la tesis corregida
d = d4(12)
d["titulo"] = "Resultados por virus"
d["imagen"] = f"{F5}/rendimiento.png"
d["texto"] = ("**SARS-CoV-2:** 21 de 42 muestras secuenciadas y 6 con linaje.\n\n"
              "**Enterovirus:** 2 de 22 caracterizadas, ambas Coxsackievirus A1 (VP1).\n\n"
              "**RSV:** 4 de 22 secuenciadas, sin lecturas del virus.")
d["notas"] = ("Panorama antes de entrar a cada virus: la secuenciación rindió de forma desigual. De las 42 muestras de "
              "SARS-CoV-2 se secuenciaron 21 y 6 permitieron asignar clado y linaje. En enterovirus, 2 de 22 "
              "muestras dieron secuencia de VP1, tipificada como Coxsackievirus A1, y ninguna rindió poliovirus. En "
              "RSV se secuenciaron 4 muestras y ninguna aportó lecturas del virus. (1 min)")
S.append(d)

# 22 · valores de Cq (figura regenerada con los datos actuales)
d = d4(13)
d["imagen"] = f"{F5}/cq_sars.png"
d["notas"] = ("El gen N1 se detectó en 31 de las 42 muestras y N2 en 21, con Cq tardíos propios de una matriz con baja "
              "carga. Las seis muestras con linaje tuvieron la mediana más baja (34,0), seguidas de las 14 "
              "secuenciadas sin caracterización (36,4) y de las 11 no secuenciadas (38,5); las diferencias son "
              "significativas, pero los rangos se solapan, así que el Cq acompaña la probabilidad de recuperar "
              "información genómica sin determinarla. El eje está invertido: más arriba, más carga viral. (1 min)")
S.append(d)

# 23 · linajes: consenso y Freyja (la tesis reemplazó la línea de tiempo)
d = d4(15)
d["imagen"] = f"{F5}/linajes_sars.png"
d["texto"] = ("**6 semanas** con linaje (3 a 9)\n\n"
              "Consenso: JN.1, LZ.5 y LU.2.1.1 (24A) y LF.7.1.3 (24H)\n\n"
              "Freyja: 86–97 % **QA.4**\n\n"
              "Todos descienden de **JN.1**")
d["notas"] = ("Los consensos de EPI2ME cubrieron entre el 3 y el 17 % del genoma; con esa información parcial, "
              "Nextclade ubicó las semanas 3 a 8 en el clado 24A (JN.1, LZ.5 y LU.2.1.1) y la semana 9 en el 24H "
              "(LF.7.1.3). Freyja, que estima la mezcla a partir de todas las lecturas, atribuyó entre el 86 y el 97 % "
              "de cada biblioteca a QA.4, un sublinaje de LF.7.1.3. Todos son descendientes de JN.1. Los datos "
              "describen su presencia conjunta, no una sucesión en el tiempo, y sin un control negativo secuenciado "
              "no se descarta la contaminación cruzada. (1 min)")
S.append(d)

# 24 · enterovirus: la tesis corrigió VP4 → VP1 (el reanálisis con la especie C ubicó las lecturas en VP1)
d = d4(16)
for e in d["elementos"]:
    t = html_txt(e)
    if e["tipo"] == "forma" and e.get("relleno") == ROJO:
        e["x"], e["w"] = 455, 105                                           # amplicón bajo VP1
    if t.startswith("Genoma de enterovirus"):
        e["html"] = P("Genoma de enterovirus")
    if t.startswith("blanco esperado"):
        e["html"] = P("blanco: VP1 (cebadores Y7/Q8)")
    if t.startswith("amplicón obtenido"):
        e["html"] = P("amplicón obtenido: VP1, 1094 pb", True)
        e["x"], e["w"] = 300, 420
    if t.startswith("Coxsackievirus A"):
        e["contenido"] = (P("Coxsackievirus A1", True, "center") + P("semanas 45 y 46 · 87,1 % de identidad", a="center")
                          + P("0 de 22 muestras con poliovirus", a="center"))
d["elementos"].append(texto(X0, 520, 590, P("El análisis inicial, solo contra poliovirus, ubicó las lecturas en VP4; "
                                             "el reanálisis contra la especie C las ubicó en VP1."), 68, GRIS))
d["notas"] = ("La PCR anidada recuperó enterovirus en las semanas 45 y 46 (febrero de 2026), con bandas de 1100 a "
              "1200 pb. El análisis inicial alineó las lecturas solo contra poliovirus 1, 2 y 3 y las ubicó entre las "
              "posiciones 529 y 1049, en VP4. El reanálisis contra un panel de enterovirus de la especie C corrigió esa "
              "lectura: la mayoría de las lecturas correspondió a VP1, con más del 97 % del amplicón de 1094 pb "
              "cubierto a 20 lecturas. Ninguna de las 22 muestras rindió poliovirus, y como el ensayo no tuvo control "
              "positivo de poliovirus, ese negativo no es concluyente. (1 min)")
S.append(d)

# 25 · Coxsackievirus A1 (vacía en el deck): detalle del árbol de VP1 de la tesis
S.append({"diseno": "imagen", "numero": "05", "titulo": "Coxsackievirus A1",
          "imagen": f"{F5}/arbol_vp1_detalle.png", "lado": "derecha", "ancho": 790,
          "texto": ("VP1 **idéntica** (1087 pb) en las semanas 45 y 46\n\n"
                    "**87,1 %** de identidad con CVA1 (PQ566821.1)\n\n"
                    "Bootstrap del **100 %**"),
          "pie": "Detalle del árbol de máxima verosimilitud de VP1 (IQ-TREE)",
          "notas": ("Las secuencias consenso de VP1 de las dos semanas resultaron idénticas en 1087 pb, y su mayor "
                    "identidad en el GenBank fue del 87,1 % con un Coxsackievirus A1 de 2023; las 20 secuencias más "
                    "cercanas también fueron Coxsackievirus A1. Esa identidad supera el 75 % que exige la tipificación "
                    "por VP1, y el árbol ubicó ambas secuencias en el clado de Coxsackievirus A1 con un apoyo del 100 %. "
                    "La identidad completa es compatible con una misma cepa en semanas consecutivas, aunque ambas se "
                    "procesaron juntas sin un control negativo secuenciado. (1 min)")})

# 26 · RSV: sin lecturas del virus (tesis)
d = d4(17)
reemplazar(d, "con subgrupo o clado", "con lecturas de RSV")
for e in d["elementos"]:
    if html_txt(e).startswith("EPI2ME no alineó"):
        e["html"] = P("Las bandas fueron amplificación inespecífica: fragmentos de 155–234 pb frente a ~400 pb del esquema")
d["notas"] = ("RSV se intentó en las 22 muestras. Las de las semanas 50, 52, 53 y 54 mostraron bandas y se "
              "secuenciaron en ocho bibliotecas, con 581 826 lecturas, pero ninguna alineó con RSV-A ni con RSV-B. "
              "Entre el 73 y el 78 % de las lecturas llevaba cebadores del esquema en sus extremos y medía de 155 a "
              "234 pb, por debajo de los 400 pb de los amplicones, así que las bandas fueron amplificación "
              "inespecífica. Sin RT-qPCR de RSV, el resultado es un intento de detección negativo. (45 s)")
S.append(d)

# 27 · ventanas de análisis: mapa de calor nativo recalculado con los datos actuales
d = d4(19)
estado_col = {"No analizado": "#eeeeee", "No secuenciado": "#9ecae1", "Secuenciado: no determinado": "#fdae6b",
              "Secuenciado: determinado": "#74c476", "Secuenciado: Coxsackie A": "#9e9ac8"}
grid = {(r["virus"], int(r["semana"])): r["estado"] for r in csv.DictReader(open(DATOS / "vigilancia_long.csv"))}
virus = ["SARS-CoV-2", "Poliovirus", "RSV"]
# rótulos del CSV de la tesis corregida → colores del mapa; la leyenda pasa a la terminología de la tesis
ALIAS = {"Secuenciado: sin caracterización": "Secuenciado: no determinado",
         "Secuenciado: Coxsackievirus A1": "Secuenciado: Coxsackie A"}
LEYENDA = {"Secuenciado: no determinado": "Secuenciado: sin caracterización",
           "Secuenciado: determinado": "Secuenciado: linaje determinado",
           "Secuenciado: Coxsackie A": "Secuenciado: Coxsackievirus A1"}
for e in d["elementos"]:
    if e["tipo"] == "texto" and html_txt(e) in LEYENDA:
        e["html"] = e["html"].replace(html_txt(e), LEYENDA[html_txt(e)])
celdas = [e for e in d["elementos"] if e["tipo"] == "forma" and e.get("w") == 33 and e.get("h") == 36]
k = 0
for panel, (w0, w1) in enumerate([(1, 28), (29, 56)]):
    for vk in virus:
        for sem in range(w0, w1 + 1):
            celdas[k]["relleno"] = estado_col.get(ALIAS.get(grid.get((vk, sem)), grid.get((vk, sem))), "#eeeeee")
            k += 1
assert k == len(celdas), (k, len(celdas))
S.append(d)

# 28 · limitaciones (la tesis cambió «Métodos»: VP1 sí se amplificó; la limitación son los controles)
d = d4(23)
reemplazar(d, "<strong>Métodos</strong>", "<strong>Controles</strong>")
for e in d["elementos"]:
    if html_txt(e).startswith("Cebadores de VP1"):
        e["html"] = P("Sin control positivo de poliovirus, RT-qPCR de RSV ni control negativo secuenciado")
d["notas"] = ("La principal limitación fue el poco material viral en una matriz diluida: la detección por RT-qPCR no "
              "se tradujo en caracterización en la mayoría de las muestras. Las retrospectivas, conservadas en "
              "Shield 2X y PBS 1X, no rindieron secuencia. Los análisis de los tres virus se solaparon poco en el "
              "tiempo. Y faltaron controles: sin control positivo de poliovirus ni RT-qPCR de RSV, sus negativos no son "
              "concluyentes, y sin un control negativo secuenciado no se descarta la contaminación entre bibliotecas. "
              "Además, hay pocos genomas clínicos de 2025 para comparar (Bruno et al., 2025). (1 min)")
S.append(d)

# 29 · conclusiones: RSV sin recuperar (tesis) y frase final de la conclusión general
d = d4(24)
rsv_y = None
for e in d["elementos"]:
    if html_txt(e) == "RSV":
        rsv_y = e["y"]
for e in d["elementos"]:
    if rsv_y is not None and e["tipo"] == "icono" and abs(e["y"] - (rsv_y - 11)) < 15:
        e["nombre"], e["color"] = "minus-circle", "#d6d2cb"
    if rsv_y is not None and e["tipo"] == "forma" and abs(e["y"] - (rsv_y + 19)) < 15:
        e["relleno"] = "#e6e3dd"
t_conc = {"linajes JN.1 (24A, 24H)": "descendientes de JN.1", "Coxsackievirus A": "Coxsackievirus A1 (VP1)",
          "sin subgrupo": "sin lecturas del virus"}
for e in d["elementos"]:
    t = html_txt(e)
    if t in t_conc:
        e["html"] = e["html"].replace(t, t_conc[t])
    if t.startswith("La carga viral y la conservación"):
        e[("contenido" if "contenido" in e else "html")] = e.get("contenido", e.get("html")).replace(
            t, "Detectar fue más accesible que caracterizar: dependió de la carga viral y de la amplificación.")
d["notas"] = ("Esta es la respuesta a la pregunta de investigación. (1 min) El mismo flujo se aplicó a los tres virus y "
              "la evidencia difiere entre ellos. SARS-CoV-2 se detectó en la mayoría de las semanas y se caracterizó "
              "en seis, con descendientes de JN.1. En enterovirus, VP1 permitió tipificar un Coxsackievirus A1, y la "
              "ausencia de poliovirus no es concluyente. Para RSV el resultado es negativo. La detección resultó más "
              "accesible que la caracterización genómica, que dependió de la carga viral y de la amplificación.")
S.append(d)

# 30 · aporte y recomendaciones (las de la tesis)
d = d4(25)
cambios = {"Seleccionar<br>por Cq": "Controlar", "y amplificar el genoma": "negativo secuenciado y curva estándar",
           "antes de secuenciar": "sólidos y RT-qPCR previa"}
for e in d["elementos"]:
    for a, b in cambios.items():
        if a in str(e.get("html") or ""):
            e["html"] = e["html"].replace(a, b)
d["notas"] = ("Aporte: la primera línea de base molecular y genómica multipatógeno de aguas residuales en Quito, con "
              "SARS-CoV-2, enterovirus y RSV en una misma matriz; la PTAR Quitumbe puede funcionar como sitio "
              "centinela para varios virus. (1 min) Recomendaciones: procesar el material poco después de recogerlo; "
              "incluir en cada corrida un control negativo secuenciado y, en la RT-qPCR, curva estándar, control de "
              "recuperación y PMMoV; para RSV, trabajar con sólidos sedimentados y seleccionar por RT-qPCR antes de "
              "secuenciar; ampliar muestras y réplicas, cruzar con secuencias clínicas y mantener la vigilancia de "
              "enterovirus por VP1.")
S.append(d)

# 31–34 · agradecimientos (deck): sin número de sección; la foto del campus va bajo la banda, sin tapar el título
S.append(lienzo(None, "Agradecimientos", [imagen(f"{SL}/13101532.png", (X0, 128, 1140, 512))]))
for a, b in (("13101565.png", "13101570.jpeg"), ("13101637.jpeg", "13101640.jpeg"), ("13101644.jpeg", "13101659.jpeg")):
    S.append(lienzo(None, "Agradecimientos", [imagen(f"{SL}/{a}", (95, 132, 535, 500)),
                                              imagen(f"{SL}/{b}", (650, 132, 535, 500))]))

# 35+ · referencias: las del v4 más las fuentes de las figuras nuevas verificadas en Crossref y las de la metodología
refs = [r for d_ in D4[25:28] for r in d_["items"]]
refs += [
    "Aguilar-Gamboa, F. R., et al. (2021). Diversidad genómica en SARS-CoV-2: Mutaciones y variantes. *Revista del Cuerpo Médico Hospital Nacional Almanzor Aguinaga Asenjo*, *14*(4), 572–582. https://doi.org/10.35434/rcmhnaaa.2021.144.1465",
    "Aksamentov, I., et al. (2021). Nextclade: Clade assignment, mutation calling and quality control for viral genomes. *Journal of Open Source Software*, *6*(67), 3773. https://doi.org/10.21105/joss.03773",
    "Arita, M., et al. (2015). Development of an efficient entire-capsid-coding-region amplification method for direct detection of poliovirus from stool extracts. *Journal of Clinical Microbiology*, *53*(1), 73–78. https://doi.org/10.1128/JCM.02384-14",
    "Bergmann, C. C., & Silverman, R. H. (2020). COVID-19: Coronavirus replication, pathogenesis, and therapeutic strategies. *Cleveland Clinic Journal of Medicine*, *87*(6), 321–327. https://doi.org/10.3949/ccjm.87a.20047",
    "Feferbaum-Leite, S., et al. (2023). Insights into enterovirus A-71 antiviral development: From natural sources to synthetic nanoparticles. *Archives of Microbiology*, *205*(10), 334. https://doi.org/10.1007/s00203-023-03660-3",
    "Karthikeyan, S., et al. (2022). Wastewater sequencing reveals early cryptic SARS-CoV-2 variant transmission. *Nature*, *609*, 101–108. https://doi.org/10.1038/s41586-022-05049-6",
    "Lamers, M. M., & Haagmans, B. L. (2022). SARS-CoV-2 pathogenesis. *Nature Reviews Microbiology*, *20*(5), 270–284. https://doi.org/10.1038/s41579-022-00713-0",
    "Maloney, D. M., et al. (2025). ARTIC RSV amplicon sequencing reveals global RSV genotype dynamics. *Wellcome Open Research*, *10*, 323. https://doi.org/10.12688/wellcomeopenres.24311.1",
    "Mbani, C. J., et al. (2023). The fight against poliovirus is not over. *Microorganisms*, *11*(5), 1323. https://doi.org/10.3390/microorganisms11051323",
    "New England Biolabs. (2021). *Instruction manual: NEBNext ARTIC SARS-CoV-2 RT-PCR module*.",
    "Oxford Nanopore Technologies. (2025). *Ligation sequencing amplicons: Native Barcoding Kit 96 V14 (SQK-NBD114.96)*. https://nanoporetech.com",
]
import unicodedata
clave = lambda r: unicodedata.normalize("NFKD", r).encode("ascii", "ignore").decode().lower()
refs = sorted(set(refs), key=clave)
POR = 6
partes = [refs[i:i + POR] for i in range(0, len(refs), POR)]
for k, items in enumerate(partes, 1):
    d = {"diseno": "referencias", "titulo": f"Referencias ({k}/{len(partes)})", "items": items}
    if k == 1:
        d["notas"] = D4[25].get("notas", "")
    S.append(d)

# cierre: el deck quitó «¿Preguntas?»
d = d4(29)
d.pop("acento", None)
S.append(d)

g = {k: v for k, v in v4.items() if k != "diapositivas"}
g["titulo"] = v4["titulo"].replace("(v4, mixta)", "(v5)")
g["diapositivas"] = S
yaml.safe_dump(g, open(AQUI / "defensa_tfm_v5.yaml", "w", encoding="utf-8"), allow_unicode=True, sort_keys=False,
               width=120)
print(f"defensa_tfm_v5.yaml: {len(S)} diapositivas, {len(refs)} referencias en {len(partes)} diapositivas")
