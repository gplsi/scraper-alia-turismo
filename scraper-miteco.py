import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup, Tag
import markdownify

if __name__ == '__main__':
    miteco = []
    title_html = subtitle_html = ""
    title = ''
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    url = "https://www.miteco.gob.es/es/parques-nacionales-oapn/red-parques-nacionales/parques-nacionales/mardelascalmas.html"
    response = requests.get(url, headers=HEADERS)
    idx = 0
    if response.status_code == 200:
        data = response.text
        bs = BeautifulSoup(data, "html.parser")
        if bs:
            links = bs.find_all('div', {'class': 'button button--green button--full-width aem-GridColumn--default--none aem-GridColumn aem-GridColumn--default--12 aem-GridColumn--offset--default--0'})
            for link in links:
                idx += 1
                url = "https://www.miteco.gob.es" + link.find('a').get('href')
                response = requests.get(url, headers=HEADERS)
                if response.status_code == 200:
                    data = response.text
                    bs = BeautifulSoup(data, "html.parser")
                    if bs:
                        content = bs.find_all('div', {'class': 'cmp-container'})[4]
                        if content:
                            content_html = str(content)
                            content = content.text.strip()

                            base_filename = "mardelascalmas-" + str(idx)

                            html_filename = os.path.join("Turismo", "es", "miteco", "html", "2026-03",
                                                         f"{base_filename}.html")

                            # ❌ Si ya existe el HTML, no seguimos con esta noticia
                            # if os.path.exists(html_filename):
                            #     print(f"NOTICIA YA EXISTE: {html_filename}")
                            #     continue

                            with open(html_filename, "wb") as f:
                                f.write(response._content)  # data es el contenido HTML original

                            html = content_html
                            markdown = markdownify.markdownify(str(html), heading_style="ATX")
                            md_filename = os.path.join("Turismo", "es", "miteco", "md", "2026-03", f"{base_filename}.md")
                            with open(md_filename, "w", encoding="utf-8") as f:
                                f.write(markdown)

                            txt_filename = os.path.join("Turismo", "es", "miteco", "plain", "2026-03", f"{base_filename}.txt")
                            with open(txt_filename, "w", encoding="utf-8") as f:
                                f.write(content)

                            miteco.append(
                                {'source': url,
                                 'title': title,
                                 'path2html': './html/2026-03/' + base_filename + ".html",
                                 'path2txt': './plain/2026-03/' + base_filename + ".txt",
                                 'path2md': './md/2026-03/' + base_filename + ".md"})

                            print("NOTICIA: " + url + " DESCARGADA.")


        ruta = os.path.join("Turismo", "es", "miteco", "index.json")
        f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
        f.write(json.dumps(miteco, indent=4, ensure_ascii=False))