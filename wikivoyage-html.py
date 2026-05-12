from pathlib import Path

if __name__ == '__main__':
    # Carpeta raíz donde zimdump extrajo los artículos
    ROOT = Path("wikivoyage")

    contador = 0

    for f in ROOT.rglob("*"):
        if f.is_file() and f.suffix == "":
            nuevo = f.with_suffix(".html")
            f.rename(nuevo)
            contador += 1

    print(f"✔ Archivos renombrados a .html: {contador}")
