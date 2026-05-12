import os
import json
import asyncio
import markdownify
from playwright.async_api import async_playwright

async def main():
    noticiesdigitals = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url = "https://noticiesdigitals.com/parlem-desport-divendres-23-de-marc-de-2018/"
        idx = 3550
        # Iteramos páginas de noticias
        while idx < 3725:
            response = await page.goto(url, wait_until="domcontentloaded")
            # await page.wait_for_load_state("networkidle")

            # Todos los artículos
            await page.wait_for_selector("div.cm-post-categories")
            categorias = page.locator("div.cm-post-categories a")
            n = await categorias.count()

            for i in range(n):
                categoria = categorias.nth(i)
                if await categoria.text_content() == "Turisme":
                    # Guardar HTML original
                    raw_html = await response.text()
                    base_filename = f"noticia{idx}"
                    html_filename = os.path.join("Turismo", "va", "noticiesdigitals", "html", "2025-09", f"{base_filename}.html")
                    os.makedirs(os.path.dirname(html_filename), exist_ok=True)
                    with open(html_filename, "w", encoding="utf-8") as f:
                        f.write(raw_html)

                    # Extraer datos renderizados con selectores
                    title = await page.locator("h1.cm-entry-title").first.text_content()
                    date = await page.locator("time.entry-date").first.text_content()
                    container = page.locator("div.cm-entry-summary")
                    container_count = await container.count()
                    content_text_list = []
                    content_html_list = []

                    if container_count > 0:
                        c = container.nth(0)

                        # Contamos todos los hijos directos <p> o <div>
                        children_count = await c.locator(":scope > p, :scope > div").count()

                        for i in range(children_count):
                            child = c.locator(":scope > *").nth(i)
                            tag_name = await child.evaluate("el => el.tagName")

                            if tag_name.lower() == "div":
                                break  # Stop at first div
                            elif tag_name.lower() == "p":
                                text = await child.text_content()
                                html = await child.evaluate("el => el.outerHTML")
                                if text:
                                    content_text_list.append(text.strip())
                                if html:
                                    content_html_list.append(html)

                    content = "\n".join(content_text_list)
                    content_html = "\n".join(content_html_list)

                    title_html = await page.locator("h1.cm-entry-title").first.evaluate("el => el.outerHTML") or ""

                    # Guardar Markdown
                    html = f"{title_html}\n{content_html}"
                    markdown = markdownify.markdownify(html, heading_style="ATX")
                    md_filename = os.path.join("Turismo", "va", "noticiesdigitals", "md", "2025-09", f"{base_filename}.md")
                    os.makedirs(os.path.dirname(md_filename), exist_ok=True)
                    with open(md_filename, "w", encoding="utf-8") as f:
                        f.write(markdown)

                    # Guardar TXT
                    txt_filename = os.path.join("Turismo", "va", "noticiesdigitals", "plain", "2025-09", f"{base_filename}.txt")
                    os.makedirs(os.path.dirname(txt_filename), exist_ok=True)
                    with open(txt_filename, "w", encoding="utf-8") as f:
                        f.write(content or "")

                    # Agregar al índice
                    noticiesdigitals.append({
                        "source": url,
                        "title": title.strip() if title else "",
                        "date": date.strip() if date else "",
                        "path2html": f"./html/2025-09/{base_filename}.html",
                        "path2txt": f"./plain/2025-09/{base_filename}.txt",
                        "path2md": f"./md/2025-09/{base_filename}.md",
                    })

                    print(f"NOTICIA: {url} DESCARGADA.")

                    # Actualizar index.json
                    ruta = os.path.join("Turismo", "va", "noticiesdigitals", "index18.json")
                    os.makedirs(os.path.dirname(ruta), exist_ok=True)
                    with open(ruta, "w", encoding="utf-8") as f:
                        f.write(json.dumps(noticiesdigitals, indent=4, ensure_ascii=False))

                    idx += 1
                    print(f"PÁGINA {idx} DESCARGADA.")
                else:
                    print("No turismo")

            url = await page.locator('li.previous a').get_attribute("href")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())