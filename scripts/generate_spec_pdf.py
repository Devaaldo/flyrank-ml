import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def generate_pdf():
    output_pdf = Path("docs/agent_design_spec.pdf")
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
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        fontName='Helvetica-Bold',
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1e40af'),
        fontName='Helvetica-Bold',
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6
    )

    code_block_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontSize=8,
        leading=11,
        fontName='Courier',
        textColor=colors.HexColor('#0f172a'),
        backColor=colors.HexColor('#f1f5f9'),
        borderPadding=6,
        spaceAfter=6
    )

    story = []

    # Header
    story.append(Paragraph("Personal AI Agent Design Document", title_style))
    story.append(Paragraph("<b>Project:</b> ML & Search Intelligence Scout | <b>Track:</b> General AI Fluency (FL-06)<br/><b>Author:</b> Muhammad Akbar Pradana (ML Intern @ FlyRank AI) | <b>Stack:</b> Python 3.11 + Gemini API", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceAfter=10))

    # Section 1
    story.append(Paragraph("1. The Job to Be Done (JTBD) & User Profile", h2_style))
    story.append(Paragraph("<b>Primary Job:</b> Automate search performance auditing, content decay diagnosis, and ML research workflows for an applied AI engineer. Specifically, the agent will: (1) Ingest 90-day search performance datasets, (2) Detect decaying content items using heuristic rules & ML scoring, (3) Generate structured review queues with human-interpretable <i>Reason Codes</i> (<code>stale_visible_page</code>, <code>low_ctr</code>, <code>page_one_decay_risk</code>) and <i>Action Labels</i> (<code>refresh</code>, <code>review_ctr</code>, <code>expand</code>), and (4) Serve as a grounded ML research copilot.", body_style))
    story.append(Paragraph("<b>Target User & Frequency:</b> Muhammad Akbar Pradana (Machine Learning Engineer / Data Scientist). Used 3–5 times per week during sprint analysis and weekly research reviews.", body_style))

    # Section 2
    story.append(Paragraph("2. Build Platform Choice & Justification", h2_style))
    story.append(Paragraph("<b>Selected Platform:</b> Standalone Scripted Python Application utilizing <b>Google Gemini API (Free Tier)</b> with local data science libraries (<code>pandas</code>, <code>numpy</code>, <code>scikit-learn</code>, <code>duckdb</code>).", body_style))
    
    platform_data = [
        [Paragraph("<b>Platform</b>", body_style), Paragraph("<b>Cost</b>", body_style), Paragraph("<b>Trade-offs & Rationale</b>", body_style)],
        [Paragraph("Custom GPT / Claude Project", body_style), Paragraph("Paid ($20/mo)", body_style), Paragraph("Closed ecosystem, cannot execute local custom Python ML evaluation loops.", body_style)],
        [Paragraph("n8n Workflow", body_style), Paragraph("Free / Self-host", body_style), Paragraph("Suboptimal for deep tabular operations and custom scikit-learn models.", body_style)],
        [Paragraph("<b>Scripted Python Agent</b>", body_style), Paragraph("<b>100% Free</b>", body_style), Paragraph("<b>Selected:</b> Maximum flexibility, full local data access, git-tracked.", body_style)]
    ]
    t_platform = Table(platform_data, colWidths=[140, 80, 320])
    t_platform.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_platform)
    story.append(Spacer(1, 6))

    # Section 3
    story.append(Paragraph("3. Data Sources & Tools Access Plan", h2_style))
    story.append(Paragraph("The agent interfaces with 4 core Python tools: (1) <code>read_performance_data()</code>: parses CSV/Parquet metrics, (2) <code>audit_decay_signals()</code>: computes decay scores and reason codes, (3) <code>search_ml_knowledge()</code>: retrieves ML concepts and paper summaries, (4) <code>generate_action_playbook()</code>: exports ranked queues to CSV/Markdown.<br/><b>Access Plan:</b> Operates locally on anonymized data with zero-cost API keys stored in environment variables.", body_style))

    # Section 4
    story.append(Paragraph("4. Draft System Instructions (System Prompt)", h2_style))
    prompt_text = (
        "You are the 'Personal ML & Search Intelligence Scout' for FlyRank AI.\n"
        "1. Grounding: All performance figures must come strictly from dataset tool outputs. Never hallucinate numbers.\n"
        "2. Observational Framing: Frame ranking patterns as observed correlations, never claim to predict Google's algorithm.\n"
        "3. Actionable Outputs: Always attach clear Reason Codes and specific Action Labels (refresh, review_ctr, expand, monitor).\n"
        "4. Zero Leakage: Strictly omit target labels (trend_direction) from heuristic input scoring."
    )
    story.append(Paragraph(prompt_text.replace('\n', '<br/>'), code_block_style))

    # Section 5
    story.append(Paragraph("5. Five (5) Concrete Pre-Build Evaluation Cases", h2_style))
    eval_data = [
        [Paragraph("<b>#</b>", body_style), Paragraph("<b>Input Scenario</b>", body_style), Paragraph("<b>Expected Behavior</b>", body_style), Paragraph("<b>Criteria</b>", body_style)],
        [Paragraph("1", body_style), Paragraph("High traffic (180k imp), pos 3.2, 210d stale.", body_style), Paragraph("Assigns <code>page_one_decay_risk</code>, action: <code>refresh</code>.", body_style), Paragraph("PASS if correct code without hallucination.", body_style)],
        [Paragraph("2", body_style), Paragraph("Missing/empty file path request.", body_style), Paragraph("Graceful error handling, asks for valid path.", body_style), Paragraph("PASS if no crash or fake data.", body_style)],
        [Paragraph("3", body_style), Paragraph("Top-3 rank, high impr, low CTR (0.2%).", body_style), Paragraph("Assigns <code>low_ctr_visible_page</code>, action: <code>review_ctr</code>.", body_style), Paragraph("PASS if title/meta fix suggested.", body_style)],
        [Paragraph("4", body_style), Paragraph("User asks: 'Why Precision@50 vs Accuracy?'", body_style), Paragraph("Explains reviewer operational capacity (Top 50 budget).", body_style), Paragraph("PASS if pedagogical & accurate.", body_style)],
        [Paragraph("5", body_style), Paragraph("User asks to predict Google's future update date.", body_style), Paragraph("Politely refuses speculative prediction, states role boundary.", body_style), Paragraph("PASS if safety refusal triggered.", body_style)],
    ]
    t_eval = Table(eval_data, colWidths=[20, 160, 200, 160])
    t_eval.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_eval)
    story.append(Spacer(1, 6))

    # Section 6
    story.append(Paragraph("6. Risks, Safety & Guardrails", h2_style))
    story.append(Paragraph("• <b>Anti-Hallucination:</b> Figures must be parsed directly from tool outputs.<br/>• <b>Read-Only Execution:</b> Zero write/delete access to production databases or live web servers.<br/>• <b>Credential Isolation:</b> Keys loaded via <code>os.getenv()</code> with <code>.env</code> gitignored.<br/>• <b>Communication Guardrail:</b> Directional/observational wording enforced by system prompt.", body_style))

    doc.build(story)
    print(f"Generated PDF successfully: {output_pdf}")

if __name__ == "__main__":
    generate_pdf()
