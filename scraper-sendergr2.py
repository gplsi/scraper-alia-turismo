import os
import json
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import markdownify

if __name__ == '__main__':

    sendergr = []
    title_html = subtitle_html = ""
    idx = 19

    url_inicio = "https://gr-alacant.ua.es/es/etapes01_universitat-alacant-tibi.htm"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # pon False si quieres ver el navegador
        page = browser.new_page()

        # 1️⃣ Cargar página principal
        page.goto(url_inicio, timeout=60000)
        page.wait_for_load_state("networkidle")
        time.sleep(2)  # da tiempo al JS del menú

        html = page.content()
        bs = BeautifulSoup(html, "html.parser")

        # 2️⃣ AQUÍ ya existe el menú
        menu = bs.find('ul', {'class': 'navbar-nav ml-xl-auto'})
        if not menu:
            print("❌ Menú no encontrado")
            browser.close()
            exit()

        menu = menu.find_all('li', {
                'class': 'nav-item'})[3]

        noticias = menu.find('div', {'class': 'col-md-12'}).find_all('li')

        for noticia in noticias:
            enlace = noticia.find('a')
            if not enlace:
                continue

            url_noticia = "https://gr-alacant.ua.es/es/" + enlace.get('href')

            # 3️⃣ Abrir cada noticia con Playwright
            page.goto(url_noticia, timeout=60000)
            page.wait_for_load_state("networkidle")
            time.sleep(1)

            html_noticia = page.content()
            bs_noticia = BeautifulSoup(html_noticia, "html.parser")

            title = bs_noticia.find('h1')
            if not title:
                continue

            title_html = str(title)
            title_text = title.text.strip()

            content = bs_noticia.find('section', {
                'class': 'full-width-section light-gray-bg'
            })

            if not content:
                continue

            content_html = str(content)
            content_text = content.text.strip()

            base_filename = f"pagina{idx}"

            # Rutas
            html_filename = os.path.join(
                "Turismo", "es", "sendergr", "html", "2026-02",
                f"{base_filename}.html"
            )

            md_filename = os.path.join(
                "Turismo", "es", "sendergr", "md", "2026-02",
                f"{base_filename}.md"
            )

            txt_filename = os.path.join(
                "Turismo", "es", "sendergr", "plain", "2026-02",
                f"{base_filename}.txt"
            )

            # Guardar HTML
            with open(html_filename, "w", encoding="utf-8") as f:
                f.write(html_noticia)

            # Guardar Markdown
            markdown = markdownify.markdownify(content_html, heading_style="ATX")
            with open(md_filename, "w", encoding="utf-8") as f:
                f.write(markdown)

            # Guardar TXT
            with open(txt_filename, "w", encoding="utf-8") as f:
                f.write(content_text)

            # Index
            sendergr.append({
                'source': url_noticia,
                'title': title_text,
                'path2html': f'./html/2026-02/{base_filename}.html',
                'path2txt': f'./plain/2026-02/{base_filename}.txt',
                'path2md': f'./md/2026-02/{base_filename}.md'
            })

            print("NOTICIA:", url_noticia, "DESCARGADA.")
            idx += 1

        browser.close()

    # 4️⃣ Guardar index.json UNA VEZ
    ruta = os.path.join("Turismo", "es", "sendergr", "index.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(sendergr, f, indent=4, ensure_ascii=False)

    print("PÁGINA: DESCARGADA.")
