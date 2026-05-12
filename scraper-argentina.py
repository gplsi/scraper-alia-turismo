import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup
import markdownify

if __name__ == '__main__':
    argentina = []
    title = ''
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get("https://www.argentina.gob.ar/interior/turismo/noticias", headers=HEADERS)
    for i in range(62, 130):
        if i > 0:
            response = requests.get(f"https://www.argentina.gob.ar/node/56177/noticias?page={i}",
                                    headers=HEADERS)
        if response.status_code == 200:
            data = response.text
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                noticias = bs.find_all('div', {'id': 'divnoticias'})[1].find_all('div', {'class': 'col-xs-12 col-sm-3'})
                for noticia in noticias:
                    url = 'https://www.argentina.gob.ar' + noticia.find('a').get('href')
                    response = requests.get(url, headers=HEADERS)
                    if response.status_code == 200:
                        data = response.text
                        bs = BeautifulSoup(data, "html.parser")
                        if bs:
                            title = bs.find('div', {'class': 'title-description'})
                            if title:
                                title = title.text.strip()

                            subtitle = bs.find('div', {'class': 'news__lead'})
                            if subtitle:
                                subtitle = subtitle.text.strip()
                                
                            date = bs.find('div', {'class': 'news__time'})
                            if date:
                                date = date.text.strip()

                            content = bs.find('section', {'class': 'content_format'})
                            if content:
                                content = content.text.strip()

                                filename = title.lower().replace(' ', '_').replace('/', '_')
                                filename = re.sub(r'[\\/*?:"<>|¿\t\n]', '_', filename)
                                base_filename = f"{filename}"

                                html_filename = os.path.join("Turismo", "argentina", "html", "2025-05",
                                                             f"{base_filename}.html")

                                # ❌ Si ya existe el HTML, no seguimos con esta noticia
                                # if os.path.exists(html_filename):
                                #     print(f"NOTICIA YA EXISTE: {html_filename}")
                                #     continue

                                with open(html_filename, "wb") as f:
                                    f.write(response._content)  # data es el contenido HTML original

                                markdown = markdownify.markdownify(str(bs), heading_style="ATX")
                                md_filename = os.path.join("Turismo", "argentina", "md", "2025-05", f"{base_filename}.md")
                                with open(md_filename, "w", encoding="utf-8") as f:
                                    f.write(markdown)

                                txt_filename = os.path.join("Turismo", "argentina", "plain", "2025-05", f"{base_filename}.txt")
                                with open(txt_filename, "w", encoding="utf-8") as f:
                                    f.write(content)

                                argentina.append(
                                    {'source': url,
                                     'title': title,
                                     'subtitle': subtitle,
                                     'date': date,
                                     'path2html': './html/2025-05/' + base_filename + ".html",
                                     'path2txt': './plain/2025-05/' + base_filename + ".txt",
                                     'path2md': './md/2025-05/' + base_filename + ".md"})

                                print("NOTICIA: " + url + " DESCARGADA.")

                    ruta = os.path.join("Turismo", "argentina", "index-2.json")
                    f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                    f.write(json.dumps(argentina, indent=4, ensure_ascii=False))
                print("PÁGINA: " + str(i) + " DESCARGADA.")