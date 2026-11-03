"""Handle Vault Invoice core: form data -> invoice PDF. No network, no storage."""
import io
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image

def num(x, default=0.0):
    try:
        return float(str(x).replace(",", "").strip() or default)
    except ValueError:
        return default

def txt(s):
    return escape(s or "").replace("\n", "<br/>")

def compute(items, discount_pct, tax_pct, shipping, paid):
    sub = sum(i["qty"] * i["rate"] for i in items)
    disc = sub * discount_pct / 100
    tax = (sub - disc) * tax_pct / 100
    total = sub - disc + tax + shipping
    return dict(sub=sub, disc=disc, tax=tax, ship=shipping, total=total, paid=paid, due=total - paid)

def build_invoice(d, logo=None):
    cur = d["currency"]
    money = lambda v: f"{cur} {v:,.2f}"
    acc = colors.HexColor(d["accent"])
    items = d["items"]
    t = compute(items, d["discount"], d["tax"], d["shipping"], d["paid"])

    S = lambda name, **k: ParagraphStyle(name, fontName=k.pop("font", "Helvetica"), fontSize=k.pop("size", 9.5),
                                         leading=k.pop("lead", 13), **k)
    body, small = S("b"), S("s", size=8, textColor=colors.grey)
    bold, right = S("bo", font="Helvetica-Bold"), S("r", alignment=2)
    label = S("l", font="Helvetica-Bold", size=8, textColor=acc)
    title = S("t", font="Helvetica-Bold", size=28, lead=32, textColor=acc, alignment=2)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=50,
                            title=f"Invoice {d['number']}")
    W = A4[0] - 80
    story = []

    left = Paragraph(f"<b>{txt(d['biz_name'])}</b>", S("bn", font="Helvetica-Bold", size=16, lead=20))
    if logo:
        try:
            w, h = ImageReader(io.BytesIO(logo)).getSize()
            s = min(150 / w, 60 / h)
            left = Image(io.BytesIO(logo), w * s, h * s, hAlign="LEFT")
        except Exception:
            pass
    head = Table([[left, Paragraph("INVOICE", title)]], colWidths=[W * .55, W * .45])
    head.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    story += [head, Spacer(1, 6), Paragraph(txt(d["biz_name"]) if logo else "", bold)]

    meta = [[Paragraph("INVOICE #", label), Paragraph("ISSUE DATE", label), Paragraph("DUE DATE", label)],
            [Paragraph(txt(d["number"]), body), Paragraph(txt(d["issue"]), body), Paragraph(txt(d["due_date"]), body)]]
    mt = Table(meta, colWidths=[W / 3] * 3)
    mt.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("LINEBELOW", (0, 1), (-1, 1), .5, colors.lightgrey),
                            ("BOTTOMPADDING", (0, 1), (-1, 1), 8)]))
    story += [Spacer(1, 8), mt, Spacer(1, 14)]

    parties = Table([[Paragraph("FROM", label), Paragraph("BILL TO", label)],
                     [Paragraph(f"<b>{txt(d['biz_name'])}</b><br/>{txt(d['biz_info'])}", body),
                      Paragraph(f"<b>{txt(d['client_name'])}</b><br/>{txt(d['client_info'])}", body)]],
                    colWidths=[W / 2, W / 2])
    parties.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story += [parties, Spacer(1, 18)]

    rows = [[Paragraph("<font color='white'><b>DESCRIPTION</b></font>", body),
             Paragraph("<font color='white'><b>QTY</b></font>", right),
             Paragraph("<font color='white'><b>RATE</b></font>", right),
             Paragraph("<font color='white'><b>AMOUNT</b></font>", right)]]
    for i in items:
        rows.append([Paragraph(txt(i["desc"]), body), Paragraph(f"{i['qty']:g}", right),
                     Paragraph(money(i["rate"]), right), Paragraph(money(i["qty"] * i["rate"]), right)])
    it = Table(rows, colWidths=[W * .46, W * .12, W * .20, W * .22], repeatRows=1)
    it.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), acc), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LINEBELOW", (0, 1), (-1, -1), .4, colors.lightgrey),
                            ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story += [it, Spacer(1, 10)]

    tr = [["Subtotal", money(t["sub"])]]
    if t["disc"]: tr.append([f"Discount ({d['discount']:g}%)", "-" + money(t["disc"])])
    if t["tax"]: tr.append([f"{d['tax_label']} ({d['tax']:g}%)", money(t["tax"])])
    if t["ship"]: tr.append(["Shipping / fees", money(t["ship"])])
    tr.append(["Total", money(t["total"])])
    if t["paid"]: tr.append(["Amount paid", "-" + money(t["paid"])])
    tr.append(["BALANCE DUE", money(t["due"])])
    tt = Table([[Paragraph(a, right), Paragraph(b, right)] for a, b in tr], colWidths=[W * .22, W * .24], hAlign="RIGHT")
    tt.setStyle(TableStyle([("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f2f2f2")),
                            ("LINEABOVE", (0, -1), (-1, -1), 1, acc),
                            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold")]))
    tt._cellvalues[-1] = [Paragraph(f"<b>{a}</b>", right) for a in (tr[-1][0], tr[-1][1])]
    story += [tt, Spacer(1, 20)]

    for head_, key in (("PAYMENT DETAILS", "payment"), ("NOTES / TERMS", "notes")):
        if d[key].strip():
            story += [Paragraph(head_, label), Spacer(1, 3), Paragraph(txt(d[key]), body), Spacer(1, 12)]

    def footer(c, doc_):
        c.setFont("Helvetica", 8); c.setFillColor(colors.grey)
        c.drawString(40, 28, f"Invoice {d['number']}  -  {d['biz_name']}")
        c.drawRightString(A4[0] - 40, 28, f"Page {doc_.page}")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return buf.getvalue()
