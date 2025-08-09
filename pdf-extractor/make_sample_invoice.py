from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas


def ensure_examples_dir() -> Path:
    examples_dir = Path(__file__).parent / "examples"
    examples_dir.mkdir(parents=True, exist_ok=True)
    return examples_dir


def draw_text(c: canvas.Canvas, x: int, y: int, text: str) -> None:
    c.drawString(x, y, text)


def generate_sample_invoice(pdf_path: Path) -> None:
    c = canvas.Canvas(str(pdf_path), pagesize=LETTER)
    width, height = LETTER

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    draw_text(c, 50, y, "INVOICE")

    c.setFont("Helvetica", 10)
    y -= 20
    draw_text(c, 50, y, "Invoice Number: INV-2024-001")
    y -= 15
    draw_text(c, 50, y, "Invoice Date: 2024-07-15")

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    draw_text(c, 50, y, "Vendor")
    c.setFont("Helvetica", 10)
    y -= 15
    draw_text(c, 50, y, "Acme Supplies LLC")
    y -= 15
    draw_text(c, 50, y, "123 Main Street, Springfield, USA")

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    draw_text(c, 50, y, "Bill To")
    c.setFont("Helvetica", 10)
    y -= 15
    draw_text(c, 50, y, "Indal Tech Pvt Ltd")
    y -= 15
    draw_text(c, 50, y, "456 Market Road, Pune, India")

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    draw_text(c, 50, y, "Line Items")

    c.setFont("Helvetica", 10)
    y -= 18
    draw_text(c, 50, y, "1. USB-C Cable (Qty: 2)  Unit Price: 9.99  Amount: 19.98")
    y -= 15
    draw_text(c, 50, y, "2. Wireless Mouse (Qty: 1)  Unit Price: 25.00  Amount: 25.00")
    y -= 15
    draw_text(c, 50, y, "3. Laptop Stand (Qty: 1)  Unit Price: 35.00  Amount: 35.00")

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    draw_text(c, 50, y, "Totals")
    c.setFont("Helvetica", 10)
    y -= 18
    draw_text(c, 50, y, "Currency: USD")
    y -= 15
    draw_text(c, 50, y, "Total Amount: 79.98")

    y -= 40
    c.setFont("Helvetica-Oblique", 9)
    draw_text(c, 50, y, "Thank you for your business!")

    c.showPage()
    c.save()


if __name__ == "__main__":
    out_dir = ensure_examples_dir()
    out_file = out_dir / "sample_invoice.pdf"
    generate_sample_invoice(out_file)
    print(str(out_file.resolve()))
