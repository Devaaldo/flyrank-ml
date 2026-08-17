import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def generate_identity_pdf():
    output_pdf = Path("docs/portfolio_visual_identity.pdf")
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
    story.append(Paragraph("Visual Identity & Design Rationale: Portfolio System", title_style))
    story.append(Paragraph("Assignment: Week 3 (Foundations) | Author: Muhammad Akbar Pradana (ML Intern @ FlyRank AI)<br/>Target System: akbarprdna.my.id / akbarpradana.netlify.app", subtitle_style))

    # Section 1
    story.append(Paragraph("1. Executive Summary & Design Philosophy", h2_style))
    story.append(Paragraph("This document establishes the visual identity and design judgment principles for my applied Machine Learning and Data Science portfolio. Rather than relying on decorative artistic talent or flashy animations, the design strictly adheres to the principle of <b>'Frame, Not Upstage'</b> — the interface acts as a minimalist frame that puts real empirical evidence, code artifacts, and ML benchmark metrics at the center of the user's attention.", body_style))

    # Section 2
    story.append(Paragraph("2. Core Design Principle 1: Consistency, Not Talent", h2_style))
    story.append(Paragraph("Professional visual perception is created through strict typographic and spatial consistency:", body_style))
    story.append(Paragraph("• <b>Typography Pairing:</b> Standard, highly legible sans-serif / serif hierarchy for prose coupled with monospace font for numerical metrics, code snippets, and dataset columns.", bullet_style))
    story.append(Paragraph("• <b>Color Palette (60-30-10 Rule):</b> 60% monochrome background surface, 30% slate text ensuring WCAG AAA contrast, and 10% deep focal accent reserved strictly for interactive links and buttons.", bullet_style))
    story.append(Paragraph("• <b>Uniform Spacing Grid:</b> Consistent 8px baseline grid across card paddings, margins, and column layouts.", bullet_style))

    # Section 3
    story.append(Paragraph("3. Core Design Principle 2: Frame, Not Upstage", h2_style))
    story.append(Paragraph("A technical portfolio exists to prove engineering competence, not to showcase visual gimmicks:", body_style))
    story.append(Paragraph("• <b>Zero Decorative Fluff:</b> No distracting animated particle meshes, spinning 3D globes, or rainbow gradient headline fills that obscure technical copy.", bullet_style))
    story.append(Paragraph("• <b>Scannable Hierarchy:</b> Key metrics (e.g., Precision@50 = 76.0%, 30k rows evaluated, Client-Holdout validation) are surfaced immediately in clean summary callouts.", bullet_style))
    story.append(Paragraph("• <b>Subdued Containers:</b> Cards and tables use simple 0.5px solid borders rather than heavy nested boxes or glowing outlines.", bullet_style))

    # Section 4
    story.append(Paragraph("4. Core Design Principle 3: Real Proof Over AI Fluff", h2_style))
    story.append(Paragraph("When selecting imagery for project case studies, empirical artifacts always supersede generic AI-generated imagery:", body_style))
    story.append(Paragraph("• <b>Avoided:</b> Generic AI-generated stock illustrations (e.g., glowing robotic brains, neon neural net spheres) which signal amateurish filler.", bullet_style))
    story.append(Paragraph("• <b>Prioritized Real Artifacts:</b> Real terminal run logs, structured model benchmark comparison tables, ReAct agent architecture flowcharts, and distribution percentile tables.", bullet_style))

    doc.build(story)
    print(f"Generated clean B&W Times-Roman PDF successfully: {output_pdf}")

if __name__ == "__main__":
    generate_identity_pdf()
