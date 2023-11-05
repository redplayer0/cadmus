# import logging
import unicodedata
import warnings
from io import BytesIO

from jinja2 import Environment, FileSystemLoader
from weasyprint import CSS, HTML

warnings.simplefilter("ignore")

# logging.basicConfig(
#     format="%(asctime)s %(levelname)s %(message)s",
#     datefmt="%Y/%m/%d %I:%M:%S",
#     handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
#     level=0,
# )
# logging.getLogger("fontTools").setLevel(logging.WARNING)


greek_letters = [
    "α",
    "β",
    "γ",
    "δ",
    "ε",
    "στ",
    "ζ",
    "η",
    "θ",
    "ι",
    "ια",
    "ιβ",
    "ιγ",
    "ιδ",
    "ιε",
    "ιστ",
    "ιζ",
    "ιη",
    "ιθ",
    "κ",
    "κα",
]


def create_indexes():
    ids = {}
    for x in range(1, 50):
        ids[str(x) + "."] = 1
    for x in greek_letters:
        ids[str(x) + "."] = 2
    for x in range(1, 50):
        ids["(" + str(x) + ")"] = 3
    for x in greek_letters:
        ids["(" + str(x) + ")"] = 4
    for x in range(1, 50):
        ids[str(x) + "/"] = 5
    for x in greek_letters:
        ids[str(x) + "/"] = 6

    return ids


ids = create_indexes()


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def parse_body(txt):
    blocks = []

    for line in txt.split("\n"):
        line = line.strip()
        if len(line) == 0:
            continue
        tokens = line.split()
        index = tokens.pop(0)
        content = " ".join(tokens)
        if index in ids:
            indentation = ids[index]
        else:
            indentation = 0

        blocks.append((indentation, index, content))

    return blocks


def post_process(doc):
    if doc["refs"]:
        doc["has_refs"] = True
    else:
        doc["has_refs"] = False
    doc["refs"] = zip(greek_letters, doc["refs"])


def generate_from_template(template_path, obj):
    env = Environment(loader=FileSystemLoader("./"))
    template = env.get_template(template_path)
    rendered_content = template.render(obj)
    return rendered_content


def generate_pdf_from_html(html_content, css_content, output_path):
    css = CSS(string=css_content)
    return HTML(string=html_content, base_url=(".")).render(
        font_config=None, stylesheets=[css]
    )


def generate_personal_report(doc):
    doc["blocks"] = parse_body(doc["body"])
    post_process(doc)
    env = Environment(loader=FileSystemLoader("./libs"))
    template = env.get_template("personal_report.html")
    html = template.render({"doc": doc})
    pdf = HTML(string=html, base_url=(".")).render(font_config=None)

    buffer = BytesIO()
    pdf.write_pdf(buffer)
    # pdf.write_pdf("report.pdf")
    buffer.seek(0)
    return buffer


if __name__ == "__main__":
    doc = {
        "sendto": "104 Α/Κ ΜΜΠ",
        "report": "ΜΗ ΥΠΗΡΕΣΙΑΚΗ",
        "rank": "Υπλγός (ΠΒ)",
        "fullname": "Ιωάννης Λόλας",
        "father_am": "του Ηλία (ΑΜ: 69074)",
        "duties": "Αξκός 2ου Γρ",
        "location": "Πολύκαστρο",
        "date": "13 Οκτ 23",
        "attachments": "Ένας (1) φάκελος",
        "topic": "Αναφορά Παραίτησης",
        "refs": ["ΣΚ 20-1", "ΣΚ 20-2"],
        "body": "1. test test test test test test test test test test",
    }

    generate_personal_report(doc)
