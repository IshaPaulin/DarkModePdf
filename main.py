

import sys
from pathlib import Path
import fitz  # PyMuPDF



def convert_to_dark_mode(input_path: str, output_path: str = None, quality: int = 2):
    """
    Convert a PDF to dark mode by inverting all page colors.

    Args:
        input_path: Path to the input PDF
        output_path: Path for the output PDF (default: input_dark.pdf)
        quality:     Render scale factor — higher = sharper but larger file
                     1 = screen quality, 2 = good (default), 3 = high quality
    """
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    if output_path is None:
        output_path = input_path.with_stem(input_path.stem + "_dark")
    output_path = Path(output_path)

    print(f"Opening: {input_path}")
    doc = fitz.open(str(input_path))
    out = fitz.open()

    total = len(doc)
    print(f"Converting {total} page(s) to dark mode...")

    for i, page in enumerate(doc, start=1):
        print(f"  Page {i}/{total}", end="\r")

        # Render the page at the chosen quality scale
        mat = fitz.Matrix(quality, quality)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)

        # Invert all pixel colors
        pix.invert_irect(pix.irect)

        # Create a new page matching the original dimensions
        new_page = out.new_page(width=page.rect.width, height=page.rect.height)

        # Embed the inverted image into the new page
        new_page.insert_image(new_page.rect, pixmap=pix)

    out.save(str(output_path))
    print(f"\nDone! Saved to: {output_path}")


if __name__ == "__main__":
    input_path = input("Input PDF path: ")
    output_path = input("Output PDF path: ")
    convert_to_dark_mode(input_path, output_path)