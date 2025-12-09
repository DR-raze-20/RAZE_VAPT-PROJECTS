from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from datetime import datetime
import os

def format_result(result):
    if isinstance(result, dict):
        return "<br/>".join([f"{k}: {v}" for k, v in result.items()])
    if isinstance(result, list):
        return "<br/>".join([str(item) for item in result])
    return str(result)

def generate_report(results, target):

    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename = f"reports/VAPT_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Raze-Vuln-Tool — VAPT Report</b>", styles['Title']))
    story.append(Paragraph(f"Target: {target}", styles['Normal']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 15))

    for title, result in results.items():
        story.append(Paragraph(f"<b>{title}</b>", styles['Heading2']))
        story.append(Paragraph(format_result(result), styles['Normal']))
        story.append(Spacer(1, 12))

    doc.build(story)

    print(f"[+] Report saved: {filename}")
    return filename
