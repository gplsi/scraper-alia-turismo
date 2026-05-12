import os
import json
import time
import requests
import markdownify
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.biobiochile.cl/lista/categorias/turismo-y-viajes"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

OUTPUT_BASE = os.path.join("Turismo", "es", "biobiochile")
YEAR_MONTH = "2026-01"


def cargar_todas_las_noticias():
    """Usa Playwright para hacer click infinito en el botón fetch-btn"""
    urls = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=HEADERS["User-Agent"],
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        page.goto(BASE_URL, timeout=60000)

        page.wait_for_load_state("networkidle")

        last_count = 0

        while True:
            articles = page.query_selector_all("div.article-content-container")
            print(f"Artículos cargados: {len(articles)}")

            # Extraer URLs visibles
            for art in articles:
                a = art.query_selector("a")
                if a:
                    href = a.get_attribute("href")
                    if href:
                        urls.add(href)

            # Intentar click en botón "cargar más"
            try:
                btn = page.query_selector("button.fetch-btn")
                if not btn or not btn.is_visible():
                    print("No hay más botón fetch-btn.")
                    break

                page.evaluate("document.querySelector('button.fetch-btn').click()")
                page.wait_for_timeout(2500)

                if len(articles) == last_count:
                    print("No se cargan más artículos.")
                    break

                last_count = len(articles)

            except Exception as e:
                print("Fin del scroll infinito:", e)
                break

        browser.close()

    return list(urls)


def procesar_noticia(url, idx, biobiochile):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return idx

    bs = BeautifulSoup(response.text, "html.parser")

    title_tag = bs.find("h1")
    title = title_tag.text.strip() if title_tag else ""
    title_html = str(title_tag) if title_tag else ""

    date_tag = bs.find("div", {"class": "post-date"})
    date = date_tag.text.strip() if date_tag else ""

    content_tag = bs.find("div", {"class": "container-redes-contenido"})
    if not content_tag:
        return idx

    content_html = str(content_tag)
    content_text = content_tag.text.strip()

    filename = f"noticia{idx}"

    html_path = os.path.join(OUTPUT_BASE, "html", YEAR_MONTH, f"{filename}.html")
    md_path = os.path.join(OUTPUT_BASE, "md", YEAR_MONTH, f"{filename}.md")
    txt_path = os.path.join(OUTPUT_BASE, "plain", YEAR_MONTH, f"{filename}.txt")

    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    os.makedirs(os.path.dirname(txt_path), exist_ok=True)

    with open(html_path, "wb") as f:
        f.write(response.content)

    html_combined = title_html + "\n" + content_html
    markdown = markdownify.markdownify(html_combined, heading_style="ATX")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content_text)

    biobiochile.append({
        "source": url,
        "title": title,
        "date": date,
        "path2html": f"./html/{YEAR_MONTH}/{filename}.html",
        "path2txt": f"./plain/{YEAR_MONTH}/{filename}.txt",
        "path2md": f"./md/{YEAR_MONTH}/{filename}.md",
    })

    print(f"✅ NOTICIA DESCARGADA: {url}")
    return idx + 1


if __name__ == "__main__":
    biobiochile = []
    idx = 1

    print("🚀 Cargando noticias con Playwright...")
    urls = cargar_todas_las_noticias()
    print(f"🔗 Total URLs encontradas: {len(urls)}")

    for url in urls:
        idx = procesar_noticia(url, idx, biobiochile)

        index_path = os.path.join(OUTPUT_BASE, "index.json")
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(biobiochile, f, indent=4, ensure_ascii=False)

    print("🎉 Proceso terminado.")
