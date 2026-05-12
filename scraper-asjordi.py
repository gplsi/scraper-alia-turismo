import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup, Tag
import markdownify
from langdetect import detect

if __name__ == '__main__':
    asjordi_va = []
    asjordi_es = []
    title_html = subtitle_html = ""
    title = ''
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get("https://www.asjordi.org/es/actualidad", headers=HEADERS)
    for i in range(1, 36):
        if i > 1:
            response = requests.get(f"https://www.asjordi.org/es/actualidad?page={i}&init=1",
                                    headers=HEADERS)
        if response.status_code == 200:
            data = response.text
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                noticias = bs.find('div', {'class': 'm-blogList'}).find('ul').find_all('li')
                for noticia in noticias:
                    url = noticia.find('a').get('href')
                    date = noticia.find('time')
                    if date:
                        date = date.text.strip()
                    response = requests.get(url, headers=HEADERS)
                    if response.status_code == 200:
                        data = response.text
                        bs = BeautifulSoup(data, "html.parser")
                        if bs:
                            title = bs.find('h1')
                            if title:
                                title_html = str(title)
                                title = title.text.strip()

                            content = bs.find('div', {'class': 'p-blogItem__content -editorContent'})
                            if content:
                                content_html = str(content)
                                content = content.text.strip()

                                idioma = detect(title + '\n' + content)
                                if idioma == "ca":
                                    idioma = "va"

                                if idioma != "va" and idioma != "es":
                                    continue

                                filename = title.lower().replace(' ', '_').replace('/', '_')
                                filename = re.sub(r'[\\/*?:"<>|¿\t\n]', '_', filename)
                                base_filename = f"{filename}"

                                html_filename = os.path.join("Turismo", idioma, "asjordi", "html", "2026-03",
                                                             f"{base_filename}.html")

                                # ❌ Si ya existe el HTML, no seguimos con esta noticia
                                # if os.path.exists(html_filename):
                                #     print(f"NOTICIA YA EXISTE: {html_filename}")
                                #     continue

                                with open(html_filename, "wb") as f:
                                    f.write(response._content)  # data es el contenido HTML original

                                html = title_html + '\n' + subtitle_html + '\n' + content_html
                                markdown = markdownify.markdownify(str(html), heading_style="ATX")
                                md_filename = os.path.join("Turismo", idioma, "asjordi", "md", "2026-03", f"{base_filename}.md")
                                with open(md_filename, "w", encoding="utf-8") as f:
                                    f.write(markdown)

                                txt_filename = os.path.join("Turismo", idioma, "asjordi", "plain", "2026-03", f"{base_filename}.txt")
                                with open(txt_filename, "w", encoding="utf-8") as f:
                                    f.write(content)

                                if idioma == "va":
                                    asjordi_va.append(
                                        {'source': url,
                                         'title': title,
                                         'date': date,
                                         'path2html': './html/2026-03/' + base_filename + ".html",
                                         'path2txt': './plain/2026-03/' + base_filename + ".txt",
                                         'path2md': './md/2026-03/' + base_filename + ".md"})

                                    ruta = os.path.join("Turismo", idioma, "asjordi", "index.json")
                                    f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                                    f.write(json.dumps(asjordi_va, indent=4, ensure_ascii=False))
                                if idioma == 'es':
                                    asjordi_es.append(
                                        {'source': url,
                                         'title': title,
                                         'date': date,
                                         'path2html': './html/2026-03/' + base_filename + ".html",
                                         'path2txt': './plain/2026-03/' + base_filename + ".txt",
                                         'path2md': './md/2026-03/' + base_filename + ".md"})

                                    ruta = os.path.join("Turismo", idioma, "asjordi", "index.json")
                                    f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                                    f.write(json.dumps(asjordi_es, indent=4, ensure_ascii=False))

                                print("NOTICIA: " + url + " DESCARGADA.")
                print("PÁGINA: " + str(i) + " DESCARGADA.")