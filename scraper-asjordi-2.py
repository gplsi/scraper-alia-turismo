import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup, Tag
import markdownify

if __name__ == '__main__':
    asjordi = []
    title_html = subtitle_html = ""
    title = ''
    categories = ['https://www.asjordi.org/es/fiestas/58/historia', 'https://www.asjordi.org/es/fiestas/59/filaes', 'https://www.asjordi.org/es/fiestas/60/actos-festeros', 'https://www.asjordi.org/es/san-jorge/el-santo/77/vida-de-san-jorge',
                  'https://www.asjordi.org/es/san-jorge/el-santo/78/patron-de-alcoy', 'https://www.asjordi.org/es/san-jorge/el-santo/79/leyenda-creencias-y-patronazgos', 'https://www.asjordi.org/es/san-jorge/el-santo/80/iconografia', 'https://www.asjordi.org/es/san-jorge/iglesia/81/saluda-del-vicario',
                  'https://www.asjordi.org/es/san-jorge/iglesia/82/historia-de-la-iglesia-de-san-jorge', 'https://www.asjordi.org/es/san-jorge/iglesia/83/el-templo', 'https://www.asjordi.org/es/san-jorge/iglesia/84/las-fachadas-de-la-iglesia-de-san-jorge', 'https://www.asjordi.org/es/san-jorge/iglesia/85/el-interior-de-la-iglesia-de-san-jorge',
                  'https://www.asjordi.org/es/san-jorge/iglesia/86/organo-blancafort-de-san-jorge', 'https://www.asjordi.org/es/museo/88/el-museu-alcoia-de-la-festa-maf', 'https://www.asjordi.org/es/museo/89/el-edificio-del-maf', 'https://www.asjordi.org/es/asociacion/68/organizacion',
                  'https://www.asjordi.org/es/asociacion/64/objetivos-y-fines', 'https://www.asjordi.org/es/asociacion/91/casal-de-sant-jordi', 'https://www.asjordi.org/es/marchas-oficiales', 'https://www.asjordi.org/es/premio-de-composicion-musica-festera',
                  'https://www.asjordi.org/es/certamen-de-interpretacion-de-musica-festera', 'https://www.asjordi.org/es/publicaciones/124/revista-de-la-fiesta']
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    for i in range(0, 22):
        url = categories[i]
        response = requests.get(categories[i], headers=HEADERS)
        if response.status_code == 200:
            data = response.text
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                title = bs.find('h1')
                if title:
                    title_html = str(title)
                    title = title.text.strip()

                content = bs.find('div', {'class': 'p-page__content o-contentGroup__content'})
                if content:
                    content_html = str(content)
                    content = content.text.strip()

                    base_filename = title

                    html_filename = os.path.join("Turismo", "es", "asjordi", "html", "2026-03",
                                                 f"{base_filename}.html")

                    # ❌ Si ya existe el HTML, no seguimos con esta noticia
                    # if os.path.exists(html_filename):
                    #     print(f"NOTICIA YA EXISTE: {html_filename}")
                    #     continue

                    with open(html_filename, "wb") as f:
                        f.write(response._content)  # data es el contenido HTML original

                    html = title_html + '\n' + subtitle_html + '\n' + content_html
                    markdown = markdownify.markdownify(str(html), heading_style="ATX")
                    md_filename = os.path.join("Turismo", "es", "asjordi", "md", "2026-03", f"{base_filename}.md")
                    with open(md_filename, "w", encoding="utf-8") as f:
                        f.write(markdown)

                    txt_filename = os.path.join("Turismo", "es", "asjordi", "plain", "2026-03", f"{base_filename}.txt")
                    with open(txt_filename, "w", encoding="utf-8") as f:
                        f.write(content)

                    asjordi.append(
                        {'source': url,
                         'title': title,
                         'path2html': './html/2026-03/' + base_filename + ".html",
                         'path2txt': './plain/2026-03/' + base_filename + ".txt",
                         'path2md': './md/2026-03/' + base_filename + ".md"})

                    print("NOTICIA: " + url + " DESCARGADA.")

        ruta = os.path.join("Turismo", "es", "asjordi", "index-2.json")
        f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
        f.write(json.dumps(asjordi, indent=4, ensure_ascii=False))
        print("PÁGINA: " + str(i) + " DESCARGADA.")