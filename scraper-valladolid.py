import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup, Tag
import markdownify

if __name__ == '__main__':
    valladolid = []
    title_html = subtitle_html = ""
    title = meta = ''
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(f"https://www.valladolid.es/en/ciudad/turismo/utilidad/noticias", headers=HEADERS)
    idx = 1
    for i in range(0, 25):
        if i > 0:
            response = requests.get(f"https://www.valladolid.es/en/ciudad/turismo/utilidad/noticias.children,{i*10},10", headers=HEADERS)
        if response.status_code == 200:
            data = response.text
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                noticias = bs.find('ul', {'class': 'cmContentList nElements-10'}).find_all('li')
                for noticia in noticias:
                    url = "https://www.valladolid.es" + noticia.find('a').get('href')
                    response = requests.get(url, headers=HEADERS)
                    if response.status_code == 200:
                        data = response.text
                        bs = BeautifulSoup(data, "html.parser")
                        if bs:
                            title = bs.find('h2', {'id': 'contentName'})
                            if title:
                                title_html = str(title)
                                title = title.text.strip()

                            subtitle = bs.find('p', {'id': 'contentAbstract'})
                            if subtitle:
                                subtitle_html = str(subtitle)
                                subtitle = subtitle.text.strip()

                            date = bs.find('div', {'class': 'section-data pval pval-date-news pval-datetime'})
                            if date:
                                date = date.text.strip()

                            content = bs.find('div', {'class': 'block block-description block-html'})
                            if content:
                                content_html = str(content)
                                content = content.text.strip()

                                filename = "noticia" + str(idx)
                                base_filename = f"{filename}"

                                html_filename = os.path.join("Turismo", "es", "valladolid", "html", "2026-01",
                                                             f"{base_filename}.html")

                                # ❌ Si ya existe el HTML, no seguimos con esta noticia
                                # if os.path.exists(html_filename):
                                #     print(f"NOTICIA YA EXISTE: {html_filename}")
                                #     continue

                                with open(html_filename, "wb") as f:
                                    f.write(response._content)  # data es el contenido HTML original

                                html = title_html + '\n' + subtitle_html + '\n' + content_html
                                markdown = markdownify.markdownify(str(html), heading_style="ATX")
                                md_filename = os.path.join("Turismo", "es", "valladolid", "md", "2026-01", f"{base_filename}.md")
                                with open(md_filename, "w", encoding="utf-8") as f:
                                    f.write(markdown)

                                txt_filename = os.path.join("Turismo", "es", "valladolid", "plain", "2026-01", f"{base_filename}.txt")
                                with open(txt_filename, "w", encoding="utf-8") as f:
                                    f.write(content)

                                valladolid.append(
                                    {'source': url,
                                     'title': title,
                                     'date': date,
                                     'path2html': './html/2026-01/' + base_filename + ".html",
                                     'path2txt': './plain/2026-01/' + base_filename + ".txt",
                                     'path2md': './md/2026-01/' + base_filename + ".md"})

                                print("NOTICIA: " + url + " DESCARGADA.")
                                idx += 1

                    ruta = os.path.join("Turismo", "es", "valladolid", "index.json")
                    f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                    f.write(json.dumps(valladolid, indent=4, ensure_ascii=False))
                print("PÁGINA: " + str(i) + " DESCARGADA.")