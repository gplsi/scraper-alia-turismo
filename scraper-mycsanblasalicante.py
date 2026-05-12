import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup, Tag
import markdownify

if __name__ == '__main__':
    mycsanblasalicante = []
    title_html = subtitle_html = ""
    title = ''
    categories = ['https://www.mycsanblasalicante.es/la-asociacion/junta-directiva/', 'https://www.mycsanblasalicante.es/la-asociacion/local-social/', 'https://www.mycsanblasalicante.es/cargos/', 'https://www.mycsanblasalicante.es/cargos/cargos-de-la-fiesta-anos-anteriores/',
                  'https://www.mycsanblasalicante.es/filaes/fila-abbasidas/', 'https://www.mycsanblasalicante.es/filaes/fila-abbassies/', 'https://www.mycsanblasalicante.es/filaes/fila-alfaquies/', 'https://www.mycsanblasalicante.es/filaes/fila-beduinos/',
                  'https://www.mycsanblasalicante.es/filaes/fila-abencerrajes/', 'https://www.mycsanblasalicante.es/filaes/fila-magenta/', 'https://www.mycsanblasalicante.es/filaes/fila-marrakets/', 'https://www.mycsanblasalicante.es/filaes/fila-negros-kalibenos/',
                  'https://www.mycsanblasalicante.es/filaes/fila-negros-senegaleses/', 'https://www.mycsanblasalicante.es/filaes/fila-nomadas/', 'https://www.mycsanblasalicante.es/filaes/fila-almogavares/', 'https://www.mycsanblasalicante.es/filaes/fila-aragoneses/',
                  'https://www.mycsanblasalicante.es/filaes/fila-caballeros-hospitalarios/', 'https://www.mycsanblasalicante.es/filaes/fila-caballeros-de-montesa/', 'https://www.mycsanblasalicante.es/filaes/fila-cantabros/', 'https://www.mycsanblasalicante.es/filaes/fila-cides/',
                  'https://www.mycsanblasalicante.es/filaes/fila-cruzados/', 'https://www.mycsanblasalicante.es/filaes/fila-navarros/', 'https://www.mycsanblasalicante.es/filaes/fila-leoneses/', 'https://www.mycsanblasalicante.es/filaes/fila-lucentinos/',
                  'https://www.mycsanblasalicante.es/filaes/fila-templarios/', 'https://www.mycsanblasalicante.es/la-musica-y-la-fiesta/himno-de-san-blas/', 'https://www.mycsanblasalicante.es/la-musica-y-la-fiesta/conciertos-homenaje/', 'https://www.mycsanblasalicante.es/la-musica-y-la-fiesta/composiciones-del-barrio/',
                  'https://www.mycsanblasalicante.es/historia-de-la-fiesta/', 'https://www.mycsanblasalicante.es/historia-de-la-fiesta/pregoneros-de-la-fiesta/', 'https://www.mycsanblasalicante.es/historia-de-la-fiesta/historia-de-las-embajadas-de-san-blas/', 'https://www.mycsanblasalicante.es/visita-nuestro-programa/']
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    for i in range(1, 33):
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

                content = bs.find('div', {'class': 'container_inner default_template_holder clearfix page_container_inner'})
                if content:
                    content_html = str(content)
                    content = content.text.strip()

                    base_filename = title

                    html_filename = os.path.join("Turismo", "es", "mycsanblasalicante", "html", "2026-03",
                                                 f"{base_filename}.html")

                    # ❌ Si ya existe el HTML, no seguimos con esta noticia
                    # if os.path.exists(html_filename):
                    #     print(f"NOTICIA YA EXISTE: {html_filename}")
                    #     continue

                    with open(html_filename, "wb") as f:
                        f.write(response._content)  # data es el contenido HTML original

                    html = title_html + '\n' + subtitle_html + '\n' + content_html
                    markdown = markdownify.markdownify(str(html), heading_style="ATX")
                    md_filename = os.path.join("Turismo", "es", "mycsanblasalicante", "md", "2026-03", f"{base_filename}.md")
                    with open(md_filename, "w", encoding="utf-8") as f:
                        f.write(markdown)

                    txt_filename = os.path.join("Turismo", "es", "mycsanblasalicante", "plain", "2026-03", f"{base_filename}.txt")
                    with open(txt_filename, "w", encoding="utf-8") as f:
                        f.write(content)

                    mycsanblasalicante.append(
                        {'source': url,
                         'title': title,
                         'path2html': './html/2026-03/' + base_filename + ".html",
                         'path2txt': './plain/2026-03/' + base_filename + ".txt",
                         'path2md': './md/2026-03/' + base_filename + ".md"})

                    print("NOTICIA: " + url + " DESCARGADA.")

        ruta = os.path.join("Turismo", "es", "mycsanblasalicante", "index-2.json")
        f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
        f.write(json.dumps(mycsanblasalicante, indent=4, ensure_ascii=False))
        print("PÁGINA: " + str(i) + " DESCARGADA.")