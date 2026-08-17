import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def generate_explain_pdf():
    output_pdf = Path("docs/explain_it_like_you_built_it.pdf")
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
    
    # Clean, black & white styles with Times-Roman
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

    # Title & Metadata (Simple Black & White)
    story.append(Paragraph("Explain It Like You Built It: ReAct Tool Calling & Anti-Hallucination", title_style))
    story.append(Paragraph("Assignment: Week 6 (General AI Fluency) | Author: Muhammad Akbar Pradana (ML Intern @ FlyRank AI)<br/>System Analyzed: Personal ML & Search Intelligence Scout Agent (agent/search_scout_agent.py & agent/tools.py)", subtitle_style))

    # Section 1
    story.append(Paragraph("1. What Part of the Build I Am Explaining", h2_style))
    story.append(Paragraph("When building the Personal ML & Search Intelligence Scout Agent in Week 5 (FL-07), the mechanism I found most critical and interesting is the ReAct (Reasoning + Acting) Tool Calling Loop that allows a Language Model to query private tabular datasets without hallucinating numbers.", body_style))

    # Section 2
    story.append(Paragraph("2. The Core Problem: Why Standard Chatbots Fail in Data Science", h2_style))
    story.append(Paragraph("If you prompt a standard conversational LLM (like vanilla ChatGPT) with: 'What are the 90-day search impressions and SERP rank for content_9532f197bbc8?', the model will usually fabricate plausible-sounding, fake numbers. Because the model has no direct connection to private company datasets, its generative objective forces it to predict the most statistically probable sequence of tokens rather than factual truth.", body_style))

    # Section 3
    story.append(Paragraph("3. How We Solved It: The 3-Step ReAct Tool Calling Architecture", h2_style))
    story.append(Paragraph("In our implementation, we decoupled natural language comprehension from factual data retrieval into three clear operational stages:", body_style))

    steps_data = [
        [Paragraph("<b>Stage</b>", body_style), Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technical Operation</b>", body_style)],
        [Paragraph("1. Reasoning", body_style), Paragraph("Intent & Entity Parser", body_style), Paragraph("Regex parses content ID (content_9532f197bbc8) and maps intent to decay audit.", body_style)],
        [Paragraph("2. Acting", body_style), Paragraph("Local Python Tool Dispatcher", body_style), Paragraph("Executes tool_audit_decay() on the 30k-row dataset, retrieving 309k impressions, position 2.0, and 104 days staleness.", body_style)],
        [Paragraph("3. Observing", body_style), Paragraph("Grounded Formatter", body_style), Paragraph("Returns structured JSON, assigns Reason Code 'page_one_decay_risk' and Action Label '[REFRESH]'.", body_style)]
    ]
    t_steps = Table(steps_data, colWidths=[80, 130, 290])
    t_steps.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_steps)
    story.append(Spacer(1, 8))

    # Section 4
    story.append(Paragraph("4. Key Takeaways & Lessons Learned", h2_style))
    story.append(Paragraph("• <b>Separation of Concerns:</b> LLMs excel at natural language parsing and explanation, but Python functions excel at arithmetic, indexing, and tabular filtering.", bullet_style))
    story.append(Paragraph("• <b>Human-in-the-Loop Ownership:</b> By writing custom tools with explicit error handling (e.g., handling missing position values and cross-platform terminal compatibility), we ensure the system is production-safe and fully explainable.", bullet_style))

    doc.build(story)
    print(f"Generated clean B&W Times-Roman PDF successfully: {output_pdf}")

if __name__ == "__main__":
    generate_explain_pdf()
