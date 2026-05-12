import requests
from bs4 import BeautifulSoup
import os
import markdownify
import json
import re

if __name__ == '__main__':
    headline = date = intro = paragraphs = ''
    title_html = subtitle_html = ""
    pags = True
    clicktrip = []
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    urls = ['https://clicktrip.es/los-mejores-destinos-para-viajar/', 'https://clicktrip.es/trekking-senderismo-rutas-de-montana-naturaleza/',
            'https://clicktrip.es/destinos-navidenos-de-europa-viajar-en-navidad-barato/', 'https://clicktrip.es/miscelanea/']
    pages = [10, 5, 5, 1]
    idx = 0
    for url in urls:
        for i in range(1, pages[idx]):
            response = requests.get(url + "page/" + str(i), headers=HEADERS)
            if response.status_code == 200:
                data = response._content
                bs = BeautifulSoup(data, "html.parser")
                if bs:
                    noticias = bs.find('ul', {'class': 'penci-grid'}).find_all('article')
                    for noticia in noticias:
                        link = noticia.find('a').get('href')
                        response = requests.get(link, headers=HEADERS)
                        if response.status_code == 200:
                            data = response._content
                            bs = BeautifulSoup(data, "html.parser")
                            if bs:
                                title = bs.find('h1')
                                if title:
                                    title_html = str(title)
                                    title = title.text.strip()

                                content = bs.find('div', {'class': 'post-entry'})
                                if content:
                                    content_html = str(content)
                                    content = content.text.strip()

                                    filename = title.lower().replace(' ', '_').replace('/', '_')
                                    filename = re.sub(r'[\\/*?:"<>|¿\t\n]', '_', filename)
                                    base_filename = f"{filename}"

                                    html_filename = os.path.join("Turismo", "es", "clicktrip", "html", "2025-12",
                                                                 f"{base_filename}.html")

                                    # ❌ Si ya existe el HTML, no seguimos con esta noticia
                                    # if os.path.exists(html_filename):
                                    #     print(f"NOTICIA YA EXISTE: {html_filename}")
                                    #     continue

                                    with open(html_filename, "wb") as f:
                                        f.write(response._content)  # data es el contenido HTML original

                                    html = title_html + '\n' + subtitle_html + '\n' + content_html
                                    markdown = markdownify.markdownify(str(html), heading_style="ATX")
                                    md_filename = os.path.join("Turismo", "es", "clicktrip", "md", "2025-12", f"{base_filename}.md")
                                    with open(md_filename, "w", encoding="utf-8") as f:
                                        f.write(markdown)

                                    txt_filename = os.path.join("Turismo", "es", "clicktrip", "plain", "2025-12", f"{base_filename}.txt")
                                    with open(txt_filename, "w", encoding="utf-8") as f:
                                        f.write(content)

                                    clicktrip.append(
                                        {'source': link, 'title': title,
                                         'language': 'es',
                                         'path2html': './html/2025-12/' + base_filename + ".html",
                                         'path2txt': './plain/2025-12/' + base_filename + ".txt",
                                         'path2md': './plain/2025-12/' + base_filename + ".md"})

                                    print("NOTICIA: " + link + " DESCARGADA.")

                    ruta = os.path.join("Turismo", "es", "clicktrip", "index.json")
                    f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                    f.write(json.dumps(clicktrip, indent=4, ensure_ascii=False))
                    print("PÁGINA " + str(i) + " DESCARGADA.")
        print("URL " + url + " DESCARGADA.")
        idx += 1