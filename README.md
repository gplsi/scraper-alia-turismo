# 📄 Web Scraper de Páginas Web con Dominio Turístico

Este repositorio incluye varios scripts de páginas webs con dominio turístico en español, valenciano e inglés, diseñado para extraer información estructurada desde sitios web de noticias o blogs:

| Nombre de la página web | URL |
|---|---|
| Notícies Digitals - Turisme | https://noticiesdigitals.com/category/turisme/ |
| Argentina Turismo | https://www.argentina.gob.ar/turismo |
| Camino de Santiago Galicia | https://www.caminodesantiago.gal/es/ |
| ClickTrip | https://clicktrip.es/ |
| Wikivoyage EN/ES | https://es.wikivoyage.org/wiki/P%C3%A1gina_principal |
| La Cultura del Agua | https://laculturadelagua.com/ |
| Mapa y Mochila | https://mapaymochila.es/ |
| Geeky Explorer Travel Blog | https://www.geekyexplorer.com/travel-blog/ |
| Asociación de San Jorge | https://www.asjordi.org |
| Unión Nacional de Entidades Festeras de Moros y Cristianos (UNDEF) | https://www.undef.eu/ |
| Madrid Destino - Prensa | https://www.madrid-destino.com/prensa?s=&since=&to=&c%5B163%5D=163 |
| Ruta en Familia | https://www.rutaenfamilia.com/ |
| El Diario de Madrid - Turismo | https://www.eldiariodemadrid.es/blog/section/turismo/ |
| BioBioChile - Turismo y Viajes | https://www.biobiochile.cl/lista/categorias/turismo-y-viajes |
| Cantabria - Comunicados Turismo | https://www.cantabria.es/web/comunicados/ver-busqueda?q=Turismo&delta=75&type=com.liferay.journal.model.JournalArticle |
| Valladolid Turismo - Noticias | https://www.valladolid.es/en/ciudad/turismo/utilidad/noticias |
| Gipuzkoa Turismo - Noticias | https://www.gipuzkoa.eus/es/web/turismoa/noticias |
| GR Alacant - Universidad de Alicante | https://gr-alacant.ua.es/es/index.htm |
| Spain.info | https://www.spain.info |
| MYC San Blas Alicante | https://www.mycsanblasalicante.es/ |
| Asociación de San Jorge | https://www.asjordi.org |
| Red de Parques Nacionales - MITECO | https://www.miteco.gob.es/es/parques-nacionales-oapn/red-parques-nacionales/parques-nacionales.html |

Cabe destacar que para la página web `Wikivoyage` se ha descargado el contenido de https://dumps.wikimedia.org/ y los scripts de wikivoyage de este repositorio se han utilizado para obtener el contenido en html, markdown y texto plano.

## 🧠 Objetivo de los scripts

El script realiza automáticamente:

- Descarga de páginas de listado de artículos.
- Extracción de enlaces individuales a noticias.
- Scraping de cada noticia para obtener:
  - **Título**
  - **Subtítulo** (si existe)
  - **Metadatos** (si existen)
  - **Fecha de publicación**
  - **Contenido textual** (párrafos)
- Normalización del contenido en un diccionario homogéneo.
- Almacenamiento final en un archivo JSON estructurado.

Este diseño permite usar el mismo esqueleto para varios medios simplemente modificando los selectores HTML.

## 🔧 Tecnologías Utilizadas

El script usa exclusivamente librerías ligeras y ampliamente compatibles:

| Librería | Uso |
|---------|------|
| `requests` | Realiza las peticiones HTTP |
| `BeautifulSoup4` | Parseo y navegación del HTML |
| `Tag` (bs4) | Validación de nodos HTML |
| `json` | Serialización del dataset |
| `os` | Gestión de rutas y archivos |

Algunos scripts pueden utilizar librerías como `Selenium` o `Playwright` si la página web carga el contenido textual de manera dinámica.

Instalación mínima:

```
pip install requests beautifulsoup4 selenium playwright
```

## ⚙️ Funcionamiento General

### 1️⃣ Descarga del listado de artículos

Se accede a una o varias páginas de listado que contienen enlaces a artículos.

### 2️⃣ Extracción de enlaces

Se obtiene la URL de cada noticia mediante selectores configurables.

### 3️⃣ Scraping de cada noticia

Se extraen:

- Título

- Subtítulo (si existe)
  
- Metadatos (si existen)

- Fecha

- Contenido consolidado

### 4️⃣ Normalización

Cada noticia procesada se almacena como:

```
{
    "id": 0,
    "url": "...",
    "title": "...",
    "subtitle": "...",
    "date": "...",
    "content": "..."
}
```


### 5️⃣ Exportación a JSON

El script genera un archivo estructurado en la raíz del proyecto, p. ej.:

```
argentina.json
```

## 📁 Ejemplo de JSON

```
[
  {
    "id": 0,
    "url": "https://medio.com/noticia1",
    "title": "Ejemplo de noticia",
    "subtitle": "Subtítulo opcional",
    "date": "2026-01-15",
    "content": "Contenido completo del artículo..."
  }
]
```

## 💰 Financiación

Este recurso está financiado por el Ministerio para la Transformación Digital y de la Función Pública — Financiado por la UE – NextGenerationEU, en el marco del proyecto Desarrollo de Modelos ALIA.

## 🙏 Agradecimientos

Expresamos nuestro agradecimiento a todas las personas e instituciones que han contribuido al desarrollo de este recurso.

Agradecimientos especiales a:

[Proveedores de datos]

[Proveedores de soporte tecnológico]

Asimismo, reconocemos las contribuciones financieras, científicas y técnicas del Ministerio para la Transformación Digital y de la Función Pública – Financiado por la UE – NextGenerationEU dentro del marco del proyecto Desarrollo de Modelos ALIA.

## 📚 Referencia

Por favor, cita este conjunto de datos usando la siguiente entrada BibTeX:

```
@misc{scraper_alia_turismo_2026,
  author       = {Espinosa Zaragoza, Sergio and Sep{\'u}lveda Torres, Robiert and Mu{\~n}oz Guillena, Rafael and Consuegra-Ayala, Juan Pablo},
  title        = {ALIA_Turismo Scraper}, 
  year         = {2026},
  institution  = {Language and Information Systems Group (GPLSI) and Centro de Inteligencia Digital (CENID), University of Alicante (UA)},
  howpublished = {\url{https://github.com/gplsi/scraper-alia-turismo}}
}
```

## ⚠️ Aviso Legal

Este recurso puede contener sesgos o artefactos no intencionados.
Cualquier tercero que utilice o implemente sistemas basados en este recurso es el único responsable de garantizar un uso conforme, seguro y ético, incluyendo el cumplimiento de las normativas relevantes en materia de IA y protección de datos.

La Universidad de Alicante, como creadora y propietaria del recurso, no asume ninguna responsabilidad por los resultados derivados del uso por parte de terceros.

## 📜 Licencia

Licencia Apache, Versión 2.0
