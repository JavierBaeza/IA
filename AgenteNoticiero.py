# agente_noticias_simple.py
# Requisitos: pip install feedparser

import time
import datetime as dt
import feedparser

# 1) Elige tus fuentes RSS (puedes agregar/editar)
FEEDS = {
    "La Discusión": "https://www.ladiscusion.cl/feed/",
    "CNN Chile": "https://www.cnnchile.com/feed/",
}

INTERVALO_MINUTOS = 30   # cada cuánto revisar (puedes bajar a 10 para pruebas)
MAX_POR_FUENTE = 8       # cuántos ítems tomar por fuente en cada pasada
RESUMEN_PALABRAS = 30    # tamaño del resumen

def resumen_corto(texto, max_palabras=30):
    if not texto:
        return ""
    # Usa el primer punto si existe; si no, recorta por palabras
    punto = texto.find(". ")
    base = texto if punto == -1 else texto[:punto+1]
    palabras = base.split()
    if len(palabras) <= max_palabras:
        return base.strip()
    return " ".join(palabras[:max_palabras]).strip() + "…"

def formatea_fecha(entry):
    try:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            dt_pub = dt.datetime.fromtimestamp(time.mktime(entry.published_parsed))
            return dt_pub.strftime("%Y-%m-%d %H:%M")
    except Exception:
        pass
    return "—"

def leer_feed(nombre, url, limite=10):
    d = feedparser.parse(url)
    items = []
    for e in d.entries[:limite]:
        titulo = getattr(e, "title", "(sin título)").strip()
        enlace = getattr(e, "link", "").strip()
        resumen = getattr(e, "summary", "") or getattr(e, "description", "")
        items.append({
            "fuente": nombre,
            "titulo": titulo,
            "link": enlace,
            "publicado": formatea_fecha(e),
            "resumen": resumen_corto(resumen, RESUMEN_PALABRAS),
        })
    return items

def ciclo(seen):
    nuevos = []
    for nombre, url in FEEDS.items():
        for it in leer_feed(nombre, url, MAX_POR_FUENTE):
            clave = (it["fuente"], it["titulo"])
            if clave not in seen:
                seen.add(clave)
                nuevos.append(it)
    # Mostrar boletín simple
    if nuevos:
        ahora = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"\n=== BOLETÍN {ahora} ===")
        for it in nuevos:
            print(f"\n[{it['fuente']}] {it['titulo']}")
            if it["publicado"] != "—":
                print(f"  Hora: {it['publicado']}")
            if it["resumen"]:
                print(f"  Resumen: {it['resumen']}")
            print(f"  Link: {it['link']}")
    else:
        print("Sin novedades por ahora.")

def main():
    print("Agente de noticias (simple). Ctrl+C para salir.")
    seen = set()  # memoria en ejecución para evitar duplicados
    # Primera pasada inmediata
    ciclo(seen)
    # Pasadas periódicas
    try:
        while True:
            time.sleep(INTERVALO_MINUTOS * 30)
            ciclo(seen)
    except KeyboardInterrupt:
        print("\nSaliendo…")

if __name__ == "__main__":
    main()