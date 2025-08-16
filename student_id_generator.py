import argparse
from pathlib import Path
from typing import Optional

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = ImageDraw = ImageFont = None  # Placeholder for type checking


def generate_card(name: str, student_id: str, course: str, logo_path: Optional[str] = None, output: str = "id_card.png") -> None:
    """Generate a simple student ID card.

    Args:
        name: Student's full name.
        student_id: Enrollment or identification number.
        course: Course or department name.
        logo_path: Optional path to the institution's logo.
        output: Filename for the generated card.
    """
    if Image is None:
        raise RuntimeError("Pillow is required to generate the card.")

    width, height = 600, 350
    background_color = (255, 255, 255)

    card = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(card)

    # Simple fonts bundled with Pillow
    font_title = ImageFont.load_default()
    font_text = ImageFont.load_default()

    margin = 20
    y = margin

    draw.text((margin, y), "Carteirinha Estudantil", fill=(0, 0, 0), font=font_title)
    y += 40

    draw.text((margin, y), f"Nome: {name}", fill=(0, 0, 0), font=font_text)
    y += 20
    draw.text((margin, y), f"Matrícula: {student_id}", fill=(0, 0, 0), font=font_text)
    y += 20
    draw.text((margin, y), f"Curso: {course}", fill=(0, 0, 0), font=font_text)

    if logo_path:
        logo_file = Path(logo_path)
        if logo_file.exists():
            logo = Image.open(logo_file).convert("RGBA")
            logo.thumbnail((100, 100))
            card.paste(logo, (width - logo.width - margin, margin), logo)
        else:
            raise FileNotFoundError(f"Logo file not found: {logo_path}")

    card.save(output)
    print(f"Carteirinha salva em {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerador de carteirinha estudantil.")
    parser.add_argument("--name", required=True, help="Nome do estudante")
    parser.add_argument("--id", required=True, help="Número de matrícula")
    parser.add_argument("--course", required=True, help="Curso do estudante")
    parser.add_argument("--logo", help="Caminho para o logotipo da instituição")
    parser.add_argument("--output", default="id_card.png", help="Arquivo de saída")
    args = parser.parse_args()

    generate_card(
        name=args.name,
        student_id=args.id,
        course=args.course,
        logo_path=args.logo,
        output=args.output,
    )


if __name__ == "__main__":
    main()
