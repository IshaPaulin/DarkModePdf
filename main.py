"""
PDF Dark Mode Converter
"""

import fitz  # pip install pymupdf


def convert_to_dark_mode(input_path, output_path, quality=1.5):
    doc = fitz.open(input_path)
    out = fitz.open()

    total = len(doc)
    print(f"Converting {total} page(s)...")

    for i, page in enumerate(doc, start=1):
        print(f"  Page {i}/{total}", end="\r")

        mat = fitz.Matrix(quality, quality)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        pix.invert_irect(pix.irect)

        # Use JPEG compression to keep file size manageable
        img_bytes = pix.tobytes("jpeg")

        new_page = out.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(new_page.rect, stream=img_bytes)

    # Save with max compression
    out.save(output_path, deflate=True, garbage=4)
    print(f"\nDone! Saved to: {output_path}")


if __name__ == "__main__":
    input_path = input("Input PDF path: ")
    output_path = input("Output PDF path: ")
    convert_to_dark_mode(input_path, output_path)