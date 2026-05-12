import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup, Tag
import markdownify

if __name__ == '__main__':
    caminodesantiago = []
    title_html = subtitle_html = ""
    title = ''
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get("https://www.caminodesantiago.gal/es/sala-de-prensa", headers=HEADERS)
    for i in range(2, 27):
        if i > 1:
            response = requests.get(f"https://www.caminodesantiago.gal/en/press-room?numPag={i}&items=8&orden=&pos=",
                                    headers=HEADERS)
        if response.status_code == 200:
            data = response.text
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                noticias = bs.find('div', {'id': 'listResults'}).find_all('div', {'class': 'col-md-12 other-news-content'})
                for noticia in noticias:
                    url = "https://www.caminodesantiago.gal" + noticia.find('a').get('href')
                    response = requests.get(url, headers=HEADERS)
                    if response.status_code == 200:
                        data = response.text
                        bs = BeautifulSoup(data, "html.parser")
                        if bs:
                            title = bs.find('h2')
                            if title:
                                title_html = str(title)
                                title = title.text.strip()

                            date = bs.find('div', {'class': 'news-date'})
                            if date:
                                date = date.text.strip()

                            subtitle = bs.find('div', {'class': 'col-md-8'})
                            if subtitle:
                                subtitle = subtitle.find('ul')
                                if subtitle:
                                    subtitle_html = str(subtitle)
                                    subtitle = subtitle.text.strip()
                                else:
                                    subtitle = ''

                            content = bs.find('div', {'class': 'col-md-8'})
                            paragraphs = ''
                            if content:
                                content_html = str(content)
                                for element in content:
                                    if isinstance(element, Tag):
                                        if 'p' == element.name:
                                            paragraphs += element.text + '\n'

                                filename = title.lower().replace(' ', '_').replace('/', '_')
                                filename = re.sub(r'[\\/*?:"<>|¿\t\n]', '_', filename)
                                base_filename = f"{filename}"[:150]

                                html_filename = os.path.join("Turismo", "en", "caminodesantiago", "html", "2025-07",
                                                             f"{base_filename}.html")

                                # ❌ Si ya existe el HTML, no seguimos con esta noticia
                                # if os.path.exists(html_filename):
                                #     print(f"NOTICIA YA EXISTE: {html_filename}")
                                #     continue

                                with open(html_filename, "wb") as f:
                                    f.write(response._content)  # data es el contenido HTML original

                                html = title_html + '\n' + subtitle_html + '\n' + content_html
                                markdown = markdownify.markdownify(str(html), heading_style="ATX")
                                md_filename = os.path.join("Turismo", "en", "caminodesantiago", "md", "2025-07", f"{base_filename}.md")
                                with open(md_filename, "w", encoding="utf-8") as f:
                                    f.write(markdown)

                                txt_filename = os.path.join("Turismo", "en", "caminodesantiago", "plain", "2025-07", f"{base_filename}.txt")
                                with open(txt_filename, "w", encoding="utf-8") as f:
                                    f.write(paragraphs)

                                caminodesantiago.append(
                                    {'source': url,
                                     'title': title,
                                     'subtitle': subtitle,
                                     'date': date,
                                     'path2html': './html/2025-07/' + base_filename + ".html",
                                     'path2txt': './plain/2025-07/' + base_filename + ".txt",
                                     'path2md': './md/2025-07/' + base_filename + ".md"})

                                print("NOTICIA: " + url + " DESCARGADA.")

                    ruta = os.path.join("Turismo", "en", "caminodesantiago", "index.json")
                    f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                    f.write(json.dumps(caminodesantiago, indent=4, ensure_ascii=False))
                print("PÁGINA: " + str(i) + " DESCARGADA.")