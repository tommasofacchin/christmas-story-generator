#core/export.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image


def export_storybook_pdf(pdf_path: str, title: str, scenes: list[str], image_paths: list[str]):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader

    c = canvas.Canvas(pdf_path, pagesize=A4)
    page_w, page_h = A4
    margin = 36

    for i, (scene, img_path) in enumerate(zip(scenes, image_paths), start=1):
        c.setFont("Helvetica-Bold", 18)
        c.drawString(margin, page_h - margin, f"{title}  ({i}/{len(image_paths)})")

        img = Image.open(img_path).convert("RGB")
        iw, ih = img.size

        max_w = page_w - 2 * margin
        max_h = page_h * 0.60
        scale = min(max_w / iw, max_h / ih)
        draw_w = iw * scale
        draw_h = ih * scale
        x = (page_w - draw_w) / 2
        y = page_h - margin - 40 - draw_h

        c.drawImage(ImageReader(img), x, y, width=draw_w, height=draw_h, preserveAspectRatio=True, mask='auto')

        c.setFont("Helvetica", 11)
        text_obj = c.beginText(margin, y - 20)
        text_obj.setLeading(14)

        words = scene.split()
        line = ""
        for w in words:
            cand = (line + " " + w).strip()
            if c.stringWidth(cand, "Helvetica", 11) <= (page_w - 2 * margin):
                line = cand
            else:
                text_obj.textLine(line)
                line = w
        if line:
            text_obj.textLine(line)

        c.drawText(text_obj)
        c.showPage()

    c.save()