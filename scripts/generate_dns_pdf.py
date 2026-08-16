import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def generate_dns_pdf():
    output_pdf = Path("docs/dns_walkthrough.pdf")
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
    story.append(Paragraph("DNS & Infrastructure Walkthrough: Personal Domain", title_style))
    story.append(Paragraph("<b>Assignment:</b> PF-04 | <b>Track:</b> General AI Fluency | <b>Author:</b> Muhammad Akbar Pradana<br/><b>Live Host:</b> akbarprdna.my.id / akbarpradana.netlify.app | <b>Target Subdomain:</b> akbar.flyrank.ai", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceAfter=8))

    # Section 1
    story.append(Paragraph("1. Executive Summary & Core DNS Concept", h2_style))
    story.append(Paragraph("The Domain Name System (DNS) functions as the phonebook of the internet, translating human-friendly names (e.g., <code>akbar.flyrank.ai</code>) into machine-readable IP addresses (e.g., <code>104.21.45.12</code>). This document outlines how custom subdomains and CNAME records route web traffic securely over HTTPS.", body_style))

    # Section 2
    story.append(Paragraph("2. What is a CNAME Record?", h2_style))
    story.append(Paragraph("A <b>CNAME (Canonical Name) Record</b> maps one domain name (an alias) to another domain name (the canonical host). Unlike an A Record (which points directly to a fixed IP), a CNAME points to a destination domain, allowing the underlying hosting infrastructure to change IP addresses without breaking domain links.", body_style))
    
    cname_box = "Host / Subdomain : akbar.flyrank.ai<br/>Record Type      : CNAME<br/>Points To / Value: akbarprdna.my.id (or akbarpradana.netlify.app)<br/>TTL              : 3600 seconds (1 hour)"
    story.append(Paragraph(cname_box, code_style))

    # Section 3
    story.append(Paragraph("3. The 4-Step DNS Resolution Lifecycle", h2_style))
    story.append(Paragraph("When a user types <code>https://akbar.flyrank.ai</code> into their browser, the following sequence occurs within milliseconds:", body_style))

    dns_steps = [
        [Paragraph("<b>Step</b>", body_style), Paragraph("<b>Component</b>", body_style), Paragraph("<b>Action & Resolution Detail</b>", body_style)],
        [Paragraph("1", body_style), Paragraph("Local Browser & Resolver", body_style), Paragraph("Browser checks local cache; if missing, queries Recursive Resolver (ISP/Cloudflare 1.1.1.1).", body_style)],
        [Paragraph("2", body_style), Paragraph("Root & TLD Nameservers", body_style), Paragraph("Resolver queries Root server (<code>.</code>) -> referred to <code>.ai</code> TLD server -> referred to FlyRank DNS.", body_style)],
        [Paragraph("3", body_style), Paragraph("Authoritative Server", body_style), Paragraph("FlyRank authoritative DNS returns: <code>akbar.flyrank.ai CNAME akbarprdna.my.id</code>.", body_style)],
        [Paragraph("4", body_style), Paragraph("TLS Handshake (HTTPS)", body_style), Paragraph("Browser connects to host IP over port 443, validates SSL certificate (padlock 🔒), and loads page.", body_style)]
    ]
    t_dns = Table(dns_steps, colWidths=[24, 150, 360])
    t_dns.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_dns)
    story.append(Spacer(1, 6))

    # Section 4
    story.append(Paragraph("4. Capstone Subdomain Deployment Checklist", h2_style))
    story.append(Paragraph("• <b>Live Verification:</b> Personal portfolio confirmed live and serving over HTTPS on clean domain.<br/>• <b>Essential Links:</b> Profile positioning, LinkedIn, GitHub, CV download, and booking link verified.<br/>• <b>Ops CNAME Provisioning:</b> FlyRank Ops provisions <code>CNAME akbar -> host.domain</code> upon capstone approval.<br/>• <b>Host Binding:</b> Custom domain added in host settings with automated Let's Encrypt SSL padlock.", body_style))

    doc.build(story)
    print(f"Generated PDF successfully: {output_pdf}")

if __name__ == "__main__":
    generate_dns_pdf()
