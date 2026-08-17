import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def generate_feature_pdf():
    output_pdf = Path("docs/make_it_do_something.pdf")
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        textColor=colors.black,
        fontName='Times-Bold',
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.black,
        fontName='Times-Italic',
        spaceAfter=14
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.black,
        fontName='Times-Bold',
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.black,
        fontName='Times-Roman',
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.black,
        fontName='Times-Roman',
        leftIndent=15,
        spaceAfter=4
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("Make It Do Something: Dynamic Contact & Ingestion Feature", title_style))
    story.append(Paragraph("Assignment: Week 6 (General AI Fluency) | Author: Muhammad Akbar Pradana (ML Intern @ FlyRank AI)<br/>Target System: akbarprdna.my.id / akbarpradana.netlify.app", subtitle_style))

    # Section 1
    story.append(Paragraph("1. Feature Selection & Purpose", h2_style))
    story.append(Paragraph("A static portfolio operates merely as a digital poster. To transform the portfolio into an active, functional tool, I implemented a <b>Serverless Contact & Project Collaboration Pipeline</b> operating on a zero-cost tier (Formspree / Netlify Forms API). This enables hiring managers, recruiters, and collaborators to submit direct inquiries that trigger automated real-time email routing to my primary inbox with zero server maintenance overhead.", body_style))

    # Section 2
    story.append(Paragraph("2. Plain-Words Explanation: What is a Backend?", h2_style))
    story.append(Paragraph("In web architecture, the <b>Frontend</b> is what the user sees and interacts with in their web browser (the visual layout, text, buttons, and input fields built with HTML, CSS, and JavaScript).", body_style))
    story.append(Paragraph("The <b>Backend</b> is the invisible engine running on a remote cloud server that performs the heavy lifting the browser cannot do alone: securely handling credentials, validating user inputs to prevent spam, and interfacing with third-party networks (e.g., SMTP email servers or relational databases) to permanently record and dispatch data.", body_style))

    # Section 3
    story.append(Paragraph("3. End-to-End Data Flow Architecture", h2_style))
    story.append(Paragraph("The data lifecycle follows a 5-step asynchronous request-response cycle:", body_style))

    steps_data = [
        [Paragraph("<b>Step</b>", body_style), Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technical Operation</b>", body_style)],
        [Paragraph("1. Input", body_style), Paragraph("Browser Client", body_style), Paragraph("User enters name, email, and inquiry details into the HTML form.", body_style)],
        [Paragraph("2. Dispatch", body_style), Paragraph("HTTP POST (JSON)", body_style), Paragraph("JavaScript intercepts submit, serializes JSON payload, and posts to API endpoint.", body_style)],
        [Paragraph("3. Backend", body_style), Paragraph("Serverless Gateway", body_style), Paragraph("Cloud function validates email syntax, rate limits, and checks anti-bot honeypot.", body_style)],
        [Paragraph("4. Routing", body_style), Paragraph("SMTP Dispatch", body_style), Paragraph("Backend triggers automated email forward directly into primary inbox.", body_style)],
        [Paragraph("5. Feedback", body_style), Paragraph("HTTP 200 Response", body_style), Paragraph("Browser receives confirmation status and renders success banner to user.", body_style)]
    ]
    t_steps = Table(steps_data, colWidths=[60, 120, 320])
    t_steps.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_steps)
    story.append(Spacer(1, 6))

    # Section 4
    story.append(Paragraph("4. Verification & Testing Proof", h2_style))
    story.append(Paragraph("• <b>Live Test Run:</b> Dispatched verified test payload from portfolio interface.", bullet_style))
    story.append(Paragraph("• <b>Delivery Confirmation:</b> Successfully received formatted email alert with correct timestamp, client headers, and sender details.", bullet_style))
    story.append(Paragraph("• <b>Error Handling:</b> Gracefully catches invalid input patterns and offline network states.", bullet_style))

    doc.build(story)
    print(f"Generated clean B&W Times-Roman PDF successfully: {output_pdf}")

if __name__ == "__main__":
    generate_feature_pdf()
