import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup, Tag
import markdownify

if __name__ == '__main__':
    sendergr = []
    title_html = subtitle_html = ""
    title = meta = ''
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    url = "https://gr-alacant.ua.es/es/etapes01_universitat-alacant-tibi.htm"
    response = requests.get(url, headers=HEADERS)
    idx = 19
    if response.status_code == 200:
        data = response.text
        bs = BeautifulSoup(data, "html.parser")
        if bs:
            menu = bs.find('div', {'class': 'col-lg-8 ml-lg-auto'}).find_all('li', {
                'class': 'row horizontal-item'})[3]
            if menu:
                noticias = bs.find('div', {'class': 'col-md-12'}).find_all('li')
                for noticia in noticias:
                    url = "https://gr-alacant.ua.es/es/" + noticia.find('a').get('href')
                    response = requests.get(url, headers=HEADERS)
                    if response.status_code == 200:
                        data = response.text
                        bs = BeautifulSoup(data, "html.parser")
                        if bs:
                            title = bs.find('h1')
                            if title:
                                title_html = str(title)
                                title = title.text.strip()

                            content = bs.find('section', {'class': 'full-width-section light-gray-bg'})
                            if content:
                                content_html = str(content)
                                content = content.text.strip()

                                filename = "pagina" + str(idx)
                                base_filename = f"{filename}"

                                html_filename = os.path.join("Turismo", "es", "sendergr", "html", "2026-02",
                                                             f"{base_filename}.html")

                                # ❌ Si ya existe el HTML, no seguimos con esta noticia
                                # if os.path.exists(html_filename):
                                #     print(f"NOTICIA YA EXISTE: {html_filename}")
                                #     continue

                                with open(html_filename, "wb") as f:
                                    f.write(response._content)  # data es el contenido HTML original

                                html = title_html + '\n' + subtitle_html + '\n' + content_html
                                markdown = markdownify.markdownify(str(content_html), heading_style="ATX")
                                md_filename = os.path.join("Turismo", "es", "sendergr", "md", "2026-02", f"{base_filename}.md")
                                with open(md_filename, "w", encoding="utf-8") as f:
                                    f.write(markdown)

                                txt_filename = os.path.join("Turismo", "es", "sendergr", "plain", "2026-02", f"{base_filename}.txt")
                                with open(txt_filename, "w", encoding="utf-8") as f:
                                    f.write(content)

                                sendergr.append(
                                    {'source': url,
                                     'title': title,
                                     'path2html': './html/2026-02/' + base_filename + ".html",
                                     'path2txt': './plain/2026-02/' + base_filename + ".txt",
                                     'path2md': './md/2026-02/' + base_filename + ".md"})

                                print("NOTICIA: " + url + " DESCARGADA.")
                                idx += 1

                                ruta = os.path.join("Turismo", "es", "sendergr", "index.json")
                                f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                                json.dump(sendergr, f, indent=4, ensure_ascii=False)
                                # f.write(json.dumps(sendergr, indent=4, ensure_ascii=False))
            print("PÁGINA: DESCARGADA.")