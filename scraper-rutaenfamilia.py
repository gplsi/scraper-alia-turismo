import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup, Tag
import markdownify

if __name__ == '__main__':
    rutaenfamilia = []
    title_html = subtitle_html = ""
    title = meta = ''
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(f"https://www.rutaenfamilia.com/noticias-ruta/", headers=HEADERS)
    idx = 1
    for i in range(1, 26):
        if i > 1:
            response = requests.get(f"https://www.rutaenfamilia.com/noticias-ruta/page/{i}/?et_blog", headers=HEADERS)
        if response.status_code == 200:
            data = response.text
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                noticias = bs.find('div', {'class': 'et_pb_with_border et_pb_module et_pb_blog_0 blogs postrutaenfamilia et_pb_blog_grid_wrapper et_pb_bg_layout_light'}).find_all('article')
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

                            date = bs.find('span', {'class': 'published'})
                            if date:
                                date = date.text.strip()

                            content = bs.find('div', {'class': 'entry-content'})
                            if content:
                                content_html = str(content)
                                content = content.text.strip()

                                filename = "noticia" + str(idx)
                                base_filename = f"{filename}"

                                html_filename = os.path.join("Turismo", "es", "rutaenfamilia", "html", "2026-01",
                                                             f"{base_filename}.html")

                                # ❌ Si ya existe el HTML, no seguimos con esta noticia
                                # if os.path.exists(html_filename):
                                #     print(f"NOTICIA YA EXISTE: {html_filename}")
                                #     continue

                                with open(html_filename, "wb") as f:
                                    f.write(response._content)  # data es el contenido HTML original

                                html = title_html + '\n' + subtitle_html + '\n' + content_html
                                markdown = markdownify.markdownify(str(html), heading_style="ATX")
                                md_filename = os.path.join("Turismo", "es", "rutaenfamilia", "md", "2026-01", f"{base_filename}.md")
                                with open(md_filename, "w", encoding="utf-8") as f:
                                    f.write(markdown)

                                txt_filename = os.path.join("Turismo", "es", "rutaenfamilia", "plain", "2026-01", f"{base_filename}.txt")
                                with open(txt_filename, "w", encoding="utf-8") as f:
                                    f.write(content)

                                rutaenfamilia.append(
                                    {'source': url,
                                     'title': title,
                                     'date': date,
                                     'category': meta,
                                     'path2html': './html/2026-01/' + base_filename + ".html",
                                     'path2txt': './plain/2026-01/' + base_filename + ".txt",
                                     'path2md': './md/2026-01/' + base_filename + ".md"})

                                print("NOTICIA: " + url + " DESCARGADA.")
                                idx += 1

                    ruta = os.path.join("Turismo", "es", "rutaenfamilia", "index.json")
                    f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                    f.write(json.dumps(rutaenfamilia, indent=4, ensure_ascii=False))
                print("PÁGINA: " + str(i) + " DESCARGADA.")