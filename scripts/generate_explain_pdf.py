import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def generate_explain_pdf():
    output_pdf = Path("docs/explain_it_like_you_built_it.pdf")
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        fontName='Helvetica-Bold',
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#475569'),
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1e40af'),
        fontName='Helvetica-Bold',
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=5
    )

    code_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontSize=8,
        leading=11,
        fontName='Courier',
        textColor=colors.HexColor('#0f172a'),
        backColor=colors.HexColor('#f1f5f9'),
        borderPadding=5,
        spaceAfter=5
    )

    story = []

    # Title & Header
    story.append(Paragraph("Explain It Like You Built It: ReAct Tool Calling & Anti-Hallucination", title_style))
    story.append(Paragraph("<b>Assignment:</b> Week 6 (General AI Fluency) | <b>Author:</b> Muhammad Akbar Pradana (ML Intern @ FlyRank AI)<br/><b>System Analyzed:</b> Personal ML & Search Intelligence Scout Agent (<code>agent/search_scout_agent.py</code> & <code>tools.py</code>)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceAfter=8))

    # Section 1
    story.append(Paragraph("1. What Part of the Build I Am Explaining", h2_style))
    story.append(Paragraph("When building the <b>Personal ML & Search Intelligence Scout Agent</b> in Week 5 (FL-07), the mechanism I found most critical and interesting is the <b>ReAct (Reasoning + Acting) Tool Calling Loop</b> that allows a Language Model to query private tabular datasets without hallucinating numbers.", body_style))

    # Section 2
    story.append(Paragraph("2. The Core Problem: Why Standard Chatbots Fail in Data Science", h2_style))
    story.append(Paragraph("If you prompt a standard conversational LLM (like vanilla ChatGPT) with: <i>'What are the 90-day search impressions and SERP rank for content_9532f197bbc8?'</i>, the model will usually fabricate plausible-sounding, fake numbers. Because the model has no direct connection to private company datasets, its generative objective forces it to predict the most statistically probable sequence of tokens rather than factual truth.", body_style))

    # Section 3
    story.append(Paragraph("3. How We Solved It: The 3-Step ReAct Tool Calling Architecture", h2_style))
    story.append(Paragraph("In our implementation, we decoupled natural language comprehension from factual data retrieval:", body_style))

    steps_data = [
        [Paragraph("<b>Stage</b>", body_style), Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technical Operation</b>", body_style)],
        [Paragraph("1. Reasoning", body_style), Paragraph("Intent & Entity Parser", body_style), Paragraph("Regex parses content ID (<code>content_9532f197bbc8</code>) and maps intent to decay audit.", body_style)],
        [Paragraph("2. Acting", body_style), Paragraph("Local Python Tool Dispatcher", body_style), Paragraph("Executes <code>tool_audit_decay()</code> on 30k-row CSV, retrieving 309k impr, pos 2.0, 104d stale.", body_style)],
        [Paragraph("3. Observing", body_style), Paragraph("Grounded Formatter", body_style), Paragraph("Returns structured JSON, assigns Reason Code <code>page_one_decay_risk</code> & Action <code>[REFRESH]</code>.", body_style)]
    ]
    t_steps = Table(steps_data, colWidths=[80, 150, 310])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_steps)
    story.append(Spacer(1, 6))

    # Section 4
    story.append(Paragraph("4. Key Takeaways & Lessons Learned", h2_style))
    story.append(Paragraph("• <b>Separation of Concerns:</b> LLMs are superior at natural language parsing and summarization, but Python functions are superior at arithmetic, indexing, and tabular filtering.<br/>• <b>Human-in-the-Loop Ownership:</b> By writing custom tools with explicit error handling (e.g., handling <code>avg_position == 0</code> missing values and Windows UTF-8 terminal encoding), we ensure the system is production-safe and fully explainable.", body_style))

    doc.build(story)
    print(f"Generated PDF successfully: {output_pdf}")

if __name__ == "__main__":
    generate_explain_pdf()
