import os
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import markdownify as md

if __name__ == '__main__':
    root = Path("wikivoyage")  # carpeta donde están los .html

    out_txt = Path("wikivoyage_txt")
    out_md = Path("wikivoyage_md")

    out_txt.mkdir(exist_ok=True)
    out_md.mkdir(exist_ok=True)

    for html_file in root.rglob("*.html"):
        rel = html_file.relative_to(root)

        # Rutas de salida
        txt_out = out_txt / rel.with_suffix(".txt")
        md_out = out_md / rel.with_suffix(".md")

        txt_out.parent.mkdir(parents=True, exist_ok=True)
        md_out.parent.mkdir(parents=True, exist_ok=True)

        # Leer HTML
        with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        soup = BeautifulSoup(content, "lxml")

        # Eliminar scripts y estilos
        for s in soup(["script", "style", "noscript"]):
            s.extract()

        # TXT limpio
        text = soup.get_text("\n").strip()

        # Markdown usando markdownify
        md_text = md(str(soup), heading_style="ATX").strip()

        # Guardar TXT
        with open(txt_out, "w", encoding="utf-8") as f:
            f.write(text)

        # Guardar Markdown
        with open(md_out, "w", encoding="utf-8") as f:
            f.write(md_text)

    print("✔ Conversión completada con markdownify.")
