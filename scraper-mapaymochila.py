import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup, Tag
import markdownify

if __name__ == '__main__':
    mapaymochila = []
    title_html = subtitle_html = ""
    title = meta = ''
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(f"https://mapaymochila.es/", headers=HEADERS)
    for i in range(1, 91):
        if i > 1:
            response = requests.get(f"https://mapaymochila.es/page/{i}/", headers=HEADERS)
        if response.status_code == 200:
            data = response.text
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                noticias = bs.find('section', {'id': 'content'}).find_all('article')
                for noticia in noticias:
                    url = noticia.find('a').get('href')
                    response = requests.get(url, headers=HEADERS)
                    if response.status_code == 200:
                        data = response.text
                        bs = BeautifulSoup(data, "html.parser")
                        if bs:
                            title = bs.find('h1')
                            if title:
                                title_html = str(title)
                                title = title.text.strip()

                            meta = bs.find('span', {'class': 'meta-category'})
                            if meta:
                                meta = meta.text.strip()

                            content = bs.find('div', {'class': 'entry clearfix'})
                            if content:
                                content_html = str(content)
                                content = content.text.strip()

                                filename = title.lower().replace(' ', '_').replace('/', '_')
                                filename = re.sub(r'[\\/*?:"<>|¿\t\n]', '_', filename)
                                base_filename = f"{filename}"

                                html_filename = os.path.join("Turismo", "es", "mapaymochila", "html", "2025-12",
                                                             f"{base_filename}.html")

                                # ❌ Si ya existe el HTML, no seguimos con esta noticia
                                # if os.path.exists(html_filename):
                                #     print(f"NOTICIA YA EXISTE: {html_filename}")
                                #     continue

                                with open(html_filename, "wb") as f:
                                    f.write(response._content)  # data es el contenido HTML original

                                html = title_html + '\n' + subtitle_html + '\n' + content_html
                                markdown = markdownify.markdownify(str(html), heading_style="ATX")
                                md_filename = os.path.join("Turismo", "es", "mapaymochila", "md", "2025-12", f"{base_filename}.md")
                                with open(md_filename, "w", encoding="utf-8") as f:
                                    f.write(markdown)

                                txt_filename = os.path.join("Turismo", "es", "mapaymochila", "plain", "2025-12", f"{base_filename}.txt")
                                with open(txt_filename, "w", encoding="utf-8") as f:
                                    f.write(content)

                                mapaymochila.append(
                                    {'source': url,
                                     'title': title,
                                     'category': meta,
                                     'path2html': './html/2025-12/' + base_filename + ".html",
                                     'path2txt': './plain/2025-12/' + base_filename + ".txt",
                                     'path2md': './md/2025-12/' + base_filename + ".md"})

                                print("NOTICIA: " + url + " DESCARGADA.")

                    ruta = os.path.join("Turismo", "es", "mapaymochila", "index.json")
                    f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                    f.write(json.dumps(mapaymochila, indent=4, ensure_ascii=False))
                print("PÁGINA: " + str(i) + " DESCARGADA.")