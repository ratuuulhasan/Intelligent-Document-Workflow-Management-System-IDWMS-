from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
from services.analytics_service import get_dashboard_stats


def generate_dashboard_report(filename="IDWMS_Analytics_Report.pdf"):
    stats = get_dashboard_stats()

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    elements = []

    elements.append(Paragraph("Enterprise IDWMS Analytics Report", title_style))
    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"]
        )
    )
    elements.append(Spacer(1, 20))

    data = [
        ["Metric", "Value"],
        ["Total Documents", stats["total_documents"]],
        ["Pending Workflows", stats["pending_workflows"]],
        ["Approved Workflows", stats["approved_workflows"]],
        ["Rejected Workflows", stats["rejected_workflows"]],
    ]

    table = Table(data, colWidths=[250, 150])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ]
        )
    )

    elements.append(table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Category Statistics", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    cat_data = [["Category", "Documents"]]
    for c in stats["categories"]:
        cat_data.append([c["category"], c["count"]])

    cat_table = Table(cat_data, colWidths=[250, 150])
    cat_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16A34A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )

    elements.append(cat_table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Recent Documents", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    recent_data = [["Title", "Category", "Upload Date"]]
    for d in stats["recent_documents"]:
        recent_data.append([
            d["title"],
            d["category"],
            str(d["upload_date"])[:19]
        ])

    recent_table = Table(recent_data, colWidths=[220, 120, 120])
    recent_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F59E0B")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )

    elements.append(recent_table)

    doc.build(elements)

    return filename