import os
from io import BytesIO

from fpdf import FPDF


FONTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "static", "fonts"
)


class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", os.path.join(FONTS_DIR, "DejaVuSans.ttf"))
        self.add_font("DejaVu", "B", os.path.join(FONTS_DIR, "DejaVuSans-Bold.ttf"))
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("DejaVu", "B", 10)
        self.cell(0, 8, "ProShield — Визначення коефіцієнта захисту", align="C", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.cell(0, 10, f"Сторінка {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("DejaVu", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, title, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def label_value(self, label, value):
        self.set_font("DejaVu", "B", 10)
        self.cell(90, 6, label, new_x="RIGHT")
        self.set_font("DejaVu", "", 10)
        self.cell(0, 6, str(value), new_x="LMARGIN", new_y="NEXT")

    def materials_table(self, title, materials):
        self.set_font("DejaVu", "B", 10)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

        # Table header
        self.set_font("DejaVu", "B", 9)
        self.set_fill_color(200, 200, 200)
        col_widths = [10, 65, 65, 50]
        headers = ["#", "Матеріал", "Підматеріал", "Товщина (см)"]
        for w, h in zip(col_widths, headers):
            self.cell(w, 6, h, border=1, fill=True)
        self.ln()

        # Table rows
        self.set_font("DejaVu", "", 9)
        for i, m in enumerate(materials, 1):
            self.cell(col_widths[0], 6, str(i), border=1)
            self.cell(col_widths[1], 6, m["material"], border=1)
            self.cell(col_widths[2], 6, m["submaterial"], border=1)
            self.cell(col_widths[3], 6, str(m["thickness"]), border=1)
            self.ln()
        self.ln(2)


def _round3(val):
    return round(val, 3)


def generate_calculation_pdf(data: dict) -> bytes:
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Розрахунок коефіцієнта захисту", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "захисної споруди цивільного захисту", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Section 1: Input parameters
    pdf.section_title("1. Вхідні параметри")

    pdf.label_value("Клас захисної споруди:", data["shelter_class_name"])
    pdf.label_value("Ступінь захисту (Аз):", str(data["az"]))
    pdf.ln(2)

    # Wall materials
    pdf.materials_table("Матеріали стін огороджувальної конструкції:", data["wall_materials"])

    # Roof materials
    pdf.materials_table("Матеріали стелі огороджувальної конструкції:", data["roof_materials"])

    # Building parameters
    pdf.set_font("DejaVu", "B", 10)
    pdf.cell(0, 7, "Параметри забудови:", new_x="LMARGIN", new_y="NEXT")
    pdf.label_value("Тип забудови:", data["building_type_name"])
    pdf.label_value("Поверховість:", data["building_height"])
    pdf.label_value("Щільність забудови:", str(data["building_density"]))

    # Optional: building wall params (6-step flow)
    if data.get("building_wall_params"):
        bwp = data["building_wall_params"]
        pdf.ln(2)
        pdf.set_font("DejaVu", "B", 10)
        pdf.cell(0, 7, "Параметри стін будівлі:", new_x="LMARGIN", new_y="NEXT")
        pdf.label_value("Матеріал стін будівлі:", bwp["material"])
        pdf.label_value("Товщина стін будівлі:", bwp["thickness"])
        pdf.label_value("Відсоток отворів:", f"{bwp['openings_percent']}%")

    pdf.ln(4)

    # Section 2: Results
    pdf.section_title("2. Результати розрахунку")

    az = data["az"]
    azf_wall = _round3(data["AZF_WALL"])
    azf_roof = _round3(data["AZF_ROOF"])

    # Wall result
    pdf.set_font("DejaVu", "B", 10)
    pdf.cell(0, 7, "Стіни:", new_x="LMARGIN", new_y="NEXT")
    pdf.label_value("Очікуваний ступінь захисту (Аз):", str(az))
    pdf.label_value("Розрахований ступінь захисту (Азф):", str(azf_wall))

    if az > azf_wall:
        pdf.set_font("DejaVu", "B", 10)
        pdf.set_text_color(220, 53, 69)
        pdf.cell(0, 6, "Ступінь захисту стін НЕ відповідає нормі!", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
    else:
        pdf.set_font("DejaVu", "B", 10)
        pdf.set_text_color(25, 135, 84)
        pdf.cell(0, 6, "Ступінь захисту стін відповідає нормі.", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)

    pdf.ln(3)

    # Roof result
    pdf.set_font("DejaVu", "B", 10)
    pdf.cell(0, 7, "Стеля:", new_x="LMARGIN", new_y="NEXT")
    pdf.label_value("Очікуваний ступінь захисту (Аз):", str(az))
    pdf.label_value("Розрахований ступінь захисту (Азф):", str(azf_roof))

    if az > azf_roof:
        pdf.set_font("DejaVu", "B", 10)
        pdf.set_text_color(220, 53, 69)
        pdf.cell(0, 6, "Ступінь захисту стелі НЕ відповідає нормі!", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
    else:
        pdf.set_font("DejaVu", "B", 10)
        pdf.set_text_color(25, 135, 84)
        pdf.cell(0, 6, "Ступінь захисту стелі відповідає нормі.", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)

    pdf.ln(6)

    # Section 3: Detailed calculations
    pdf.section_title("3. Детальні розрахунки")

    pdf.set_font("DejaVu", "B", 10)
    pdf.cell(0, 7, "Формула:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, "Аз \u2264 Азф = 1,18 \u00d7 (Ky,i \u00d7 Kn,i) \u00d7 (Кзаб / Кбуд) \u00d7 KN / (Ky,i + Kn,i)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    kzab = _round3(data["kzab"])
    coef_bud_wall = _round3(data["coefficient_bud_wall"])
    coef_bud_roof = _round3(data["coefficient_bud_roof"])
    ky_wall = _round3(data["ky_wall"])
    kn_wall = _round3(data["kn_wall"])
    ky_roof = _round3(data["ky_roof"])
    kn_roof = _round3(data["kn_roof"])
    kn_wall_val = _round3(data["KN_WALL"])
    kn_roof_val = _round3(data["KN_ROOF"])

    # Wall calculation
    pdf.set_font("DejaVu", "B", 10)
    pdf.cell(0, 7, "Розрахунок для стін:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 9)
    wall_calc = (
        f"{az} \u2264 {azf_wall} = 1.18 \u00d7 ({ky_wall} \u00d7 {kn_wall}) "
        f"\u00d7 ({kzab} / {coef_bud_wall}) \u00d7 {kn_wall_val} / ({ky_wall} + {kn_wall})"
    )
    pdf.multi_cell(0, 6, wall_calc, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Roof calculation
    pdf.set_font("DejaVu", "B", 10)
    pdf.cell(0, 7, "Розрахунок для стелі:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 9)
    roof_calc = (
        f"{az} \u2264 {azf_roof} = 1.18 \u00d7 ({ky_roof} \u00d7 {kn_roof}) "
        f"\u00d7 ({kzab} / {coef_bud_roof}) \u00d7 {kn_roof_val} / ({ky_roof} + {kn_roof})"
    )
    pdf.multi_cell(0, 6, roof_calc, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Coefficients summary
    pdf.set_font("DejaVu", "B", 10)
    pdf.cell(0, 7, "Значення коефіцієнтів:", new_x="LMARGIN", new_y="NEXT")

    coefficients = [
        ("Кзаб (коефіцієнт забудови):", str(kzab)),
        ("Кбуд стін:", str(coef_bud_wall)),
        ("Кбуд стелі:", str(coef_bud_roof)),
        ("Ky стін (гамма-випромінювання):", str(ky_wall)),
        ("Kn стін (нейтронне випромінювання):", str(kn_wall)),
        ("Ky стелі (гамма-випромінювання):", str(ky_roof)),
        ("Kn стелі (нейтронне випромінювання):", str(kn_roof)),
        ("KN стін (товщина матеріалу):", str(kn_wall_val)),
        ("KN стелі (товщина матеріалу):", str(kn_roof_val)),
    ]

    for label, value in coefficients:
        pdf.label_value(label, value)

    buf = BytesIO()
    pdf.output(buf)
    return buf.getvalue()
