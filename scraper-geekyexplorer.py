import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup, Tag
import markdownify

if __name__ == '__main__':
    geekyexplorer = []
    title_html = subtitle_html = ""
    title = ''
    idx = 1
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    response = requests.get(f"https://www.geekyexplorer.com/travel-blog", headers=HEADERS)
    for i in range(1, 9):
        if i > 0:
            response = requests.get(f"https://www.geekyexplorer.com/travel-blog/page/{i}/", headers=HEADERS)
        if response.status_code == 200:
            data = response.text
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                noticias = bs.find('main', {'id': 'main'}).find_all('article')
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

                            date = bs.find('time', {'class': 'entry-date published'})
                            if date:
                                date = date.text.strip()

                            content = bs.find('div', {'class': 'entry-content'})
                            if content:
                                content_html = str(content)
                                content = content.text.strip()

                                base_filename = f"noticia{idx}"

                                html_filename = os.path.join("Turismo", "en", "geekyexplorer", "html", "2025-12",
                                                             f"{base_filename}.html")

                                # ❌ Si ya existe el HTML, no seguimos con esta noticia
                                # if os.path.exists(html_filename):
                                #     print(f"NOTICIA YA EXISTE: {html_filename}")
                                #     continue

                                with open(html_filename, "wb") as f:
                                    f.write(response._content)  # data es el contenido HTML original

                                html = title_html + '\n' + subtitle_html + '\n' + content_html
                                markdown = markdownify.markdownify(str(html), heading_style="ATX")
                                md_filename = os.path.join("Turismo", "en", "geekyexplorer", "md", "2025-12", f"{base_filename}.md")
                                with open(md_filename, "w", encoding="utf-8") as f:
                                    f.write(markdown)

                                txt_filename = os.path.join("Turismo", "en", "geekyexplorer", "plain", "2025-12", f"{base_filename}.txt")
                                with open(txt_filename, "w", encoding="utf-8") as f:
                                    f.write(content)

                                geekyexplorer.append(
                                    {'source': url,
                                     'title': title,
                                     'date': date,
                                     'path2html': './html/2025-12/' + base_filename + ".html",
                                     'path2txt': './plain/2025-12/' + base_filename + ".txt",
                                     'path2md': './md/2025-12/' + base_filename + ".md"})

                                print("NOTICIA: " + url + " DESCARGADA.")
                                idx += 1

                    ruta = os.path.join("Turismo", "en", "geekyexplorer", "index.json")
                    f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                    f.write(json.dumps(geekyexplorer, indent=4, ensure_ascii=False))
                print("PÁGINA: " + str(i) + " DESCARGADA.")