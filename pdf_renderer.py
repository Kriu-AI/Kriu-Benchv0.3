"""
Kriu-Bench-v0.3 PDF Renderer
==============================
Renders realistic, publication-quality .pdf resume files across 4 structural layouts:
1. single_col_standard: Classic chronological corporate format.
2. two_col_sidebar: Modern tech layout with left-hand contact/skills sidebar table.
3. tabular_skills_matrix: Structured tables for skills matrix and project deliverables.
4. nonstandard_headers: Alternative section headers to stress-test RSSE segmentation.
"""

import os
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def build_styles():
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#111827'),
        alignment=TA_CENTER,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'ContactSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#4B5563'),
        alignment=TA_CENTER,
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=7,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'JobHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#1F2937'),
        spaceBefore=3,
        spaceAfter=1
    ))
    styles.add(ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1F2937'),
        alignment=TA_LEFT,
        spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        'BulletItem',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1F2937'),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=1.5
    ))
    styles.add(ParagraphStyle(
        'SidebarHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=6,
        spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        'SidebarBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#374151'),
        spaceAfter=1
    ))
    return styles

def render_pdf_single_col_standard(candidate: Dict[str, Any], output_path: str):
    """Layout 1: Single-column standard corporate layout."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36
    )
    styles = build_styles()
    story = []

    # Header
    story.append(Paragraph(candidate["name"], styles['MainTitle']))
    c_info = f"{candidate['email']} • {candidate['phone']} • {candidate['location']}"
    if candidate.get("github"):
        c_info += f" • {candidate['github']}"
    if candidate.get("linkedin"):
        c_info += f" • {candidate['linkedin']}"
    story.append(Paragraph(c_info, styles['ContactSub']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6))

    # Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", styles['SectionHeader']))
    story.append(Paragraph(candidate["summary"], styles['BodyDark']))
    story.append(Spacer(1, 4))

    # Core Skills
    story.append(Paragraph("CORE SKILLS & TECHNOLOGIES", styles['SectionHeader']))
    skills_text = " • ".join(candidate["skills_list"])
    story.append(Paragraph(skills_text, styles['BodyDark']))
    story.append(Spacer(1, 4))

    # Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles['SectionHeader']))
    for job in candidate["experience"]:
        j_head = f"{job['title']} — {job['company']} <i><font color='#6B7280'>({job['dates']})</font></i>"
        story.append(Paragraph(j_head, styles['JobHeader']))
        for b in job["bullets"]:
            story.append(Paragraph(f"• {b}", styles['BulletItem']))
        story.append(Spacer(1, 2))

    # Projects
    if candidate.get("projects"):
        story.append(Paragraph("KEY PROJECTS & DELIVERABLES", styles['SectionHeader']))
        for proj in candidate["projects"]:
            p_head = f"<b>{proj['name']}</b> | <i>{proj['tech']}</i>"
            story.append(Paragraph(p_head, styles['JobHeader']))
            story.append(Paragraph(f"• {proj['description']}", styles['BulletItem']))
            story.append(Spacer(1, 2))

    # Education
    story.append(Paragraph("EDUCATION & CREDENTIALS", styles['SectionHeader']))
    story.append(Paragraph(candidate["education"], styles['BodyDark']))

    doc.build(story)

def render_pdf_two_col_sidebar(candidate: Dict[str, Any], output_path: str):
    """Layout 2: 2-column sidebar layout using ReportLab Table."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=30,
        rightMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    styles = build_styles()

    # Left Column Elements
    left_story = []
    left_name_style = ParagraphStyle(
        'SideName', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=colors.HexColor('#111827'), spaceAfter=4
    )
    left_story.append(Paragraph(candidate["name"], left_name_style))
    c_text = f"<b>Email:</b><br/>{candidate['email']}<br/><br/><b>Phone:</b><br/>{candidate['phone']}<br/><br/><b>Location:</b><br/>{candidate['location']}"
    if candidate.get("github"):
        c_text += f"<br/><br/><b>GitHub:</b><br/>{candidate['github']}"
    if candidate.get("linkedin"):
        c_text += f"<br/><br/><b>LinkedIn:</b><br/>{candidate['linkedin']}"
    left_story.append(Paragraph(c_text, styles['SidebarBody']))
    left_story.append(Spacer(1, 6))

    left_story.append(Paragraph("CORE SKILLS", styles['SidebarHeader']))
    for s in candidate["skills_list"]:
        left_story.append(Paragraph(f"• {s}", styles['SidebarBody']))
    left_story.append(Spacer(1, 6))

    left_story.append(Paragraph("EDUCATION", styles['SidebarHeader']))
    left_story.append(Paragraph(candidate["education"], styles['SidebarBody']))

    # Right Column Elements
    right_story = []
    right_story.append(Paragraph("EXECUTIVE SUMMARY", styles['SectionHeader']))
    right_story.append(Paragraph(candidate["summary"], styles['BodyDark']))
    right_story.append(Spacer(1, 4))

    right_story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles['SectionHeader']))
    for job in candidate["experience"]:
        j_head = f"{job['title']} — {job['company']} <i><font color='#6B7280'>({job['dates']})</font></i>"
        right_story.append(Paragraph(j_head, styles['JobHeader']))
        for b in job["bullets"]:
            right_story.append(Paragraph(f"• {b}", styles['BulletItem']))
        right_story.append(Spacer(1, 2))

    if candidate.get("projects"):
        right_story.append(Paragraph("PROJECTS", styles['SectionHeader']))
        for proj in candidate["projects"]:
            p_head = f"<b>{proj['name']}</b> | <i>{proj['tech']}</i>"
            right_story.append(Paragraph(p_head, styles['JobHeader']))
            right_story.append(Paragraph(f"• {proj['description']}", styles['BulletItem']))
            right_story.append(Spacer(1, 2))

    # Wrap in 2-column table
    table_data = [[left_story, right_story]]
    t = Table(table_data, colWidths=[180, 370])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#F8FAFC')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 10),
        ('RIGHTPADDING', (0, 0), (0, 0), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBEFORE', (1, 0), (1, 0), 1, colors.HexColor('#E2E8F0')),
        ('LEFTPADDING', (1, 0), (1, 0), 14),
        ('RIGHTPADDING', (1, 0), (1, 0), 8),
    ]))

    doc.build([t])

def render_pdf_tabular_skills_matrix(candidate: Dict[str, Any], output_path: str):
    """Layout 3: Structured tabular layout with competencies and deliverables table."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = build_styles()
    story = []

    # Header
    story.append(Paragraph(candidate["name"], styles['MainTitle']))
    c_info = f"{candidate['email']} • {candidate['phone']} • {candidate['location']}"
    if candidate.get("github"):
        c_info += f" • {candidate['github']}"
    if candidate.get("linkedin"):
        c_info += f" • {candidate['linkedin']}"
    story.append(Paragraph(c_info, styles['ContactSub']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5))

    story.append(Paragraph("CAREER SUMMARY", styles['SectionHeader']))
    story.append(Paragraph(candidate["summary"], styles['BodyDark']))
    story.append(Spacer(1, 4))

    # Skills Matrix Table
    story.append(Paragraph("TECHNICAL COMPETENCY MATRIX", styles['SectionHeader']))
    skills = candidate["skills_list"]
    rows = []
    curr_row = []
    for s in skills:
        curr_row.append(Paragraph(f"• {s}", styles['SidebarBody']))
        if len(curr_row) == 3:
            rows.append(curr_row)
            curr_row = []
    if curr_row:
        while len(curr_row) < 3:
            curr_row.append(Paragraph("", styles['SidebarBody']))
        rows.append(curr_row)

    sk_table = Table(rows, colWidths=[180, 180, 180])
    sk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(sk_table)
    story.append(Spacer(1, 6))

    # Experience
    story.append(Paragraph("WORK EXPERIENCE", styles['SectionHeader']))
    for job in candidate["experience"]:
        j_head = f"{job['title']} — {job['company']} <i><font color='#6B7280'>({job['dates']})</font></i>"
        story.append(Paragraph(j_head, styles['JobHeader']))
        for b in job["bullets"]:
            story.append(Paragraph(f"• {b}", styles['BulletItem']))
        story.append(Spacer(1, 2))

    # Projects
    if candidate.get("projects"):
        story.append(Paragraph("PROJECT DELIVERABLES", styles['SectionHeader']))
        for proj in candidate["projects"]:
            p_head = f"<b>{proj['name']}</b> | <i>{proj['tech']}</i>"
            story.append(Paragraph(p_head, styles['JobHeader']))
            story.append(Paragraph(f"• {proj['description']}", styles['BulletItem']))
            story.append(Spacer(1, 2))

    story.append(Paragraph("EDUCATION", styles['SectionHeader']))
    story.append(Paragraph(candidate["education"], styles['BodyDark']))

    doc.build(story)

def render_pdf_nonstandard_headers(candidate: Dict[str, Any], output_path: str):
    """Layout 4: Nonstandard section headers."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=38,
        rightMargin=38,
        topMargin=36,
        bottomMargin=36
    )
    styles = build_styles()
    story = []

    # Title
    t_style = ParagraphStyle(
        'NSTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=17, leading=20, textColor=colors.HexColor('#0F172A'),
        alignment=TA_LEFT, spaceAfter=2
    )
    story.append(Paragraph(candidate["name"].upper(), t_style))
    c_info = f"{candidate['location']} • {candidate['email']} • {candidate['phone']}"
    if candidate.get("github"):
        c_info += f" • {candidate['github']}"
    if candidate.get("linkedin"):
        c_info += f" • {candidate['linkedin']}"
    c_style = ParagraphStyle(
        'NSContact', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor('#475569'),
        alignment=TA_LEFT, spaceAfter=6
    )
    story.append(Paragraph(c_info, c_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0F172A'), spaceAfter=6))

    h_style = ParagraphStyle(
        'NSHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=colors.HexColor('#0F172A'),
        spaceBefore=6, spaceAfter=3
    )

    story.append(Paragraph("CAREER OVERVIEW & PROFILE", h_style))
    story.append(Paragraph(candidate["summary"], styles['BodyDark']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("TECHNICAL EXPERTISE & ARSENAL", h_style))
    story.append(Paragraph(" | ".join(candidate["skills_list"]), styles['BodyDark']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("WORK HISTORY & ACHIEVEMENTS", h_style))
    for job in candidate["experience"]:
        j_head = f"<b>Position:</b> {job['title']} | <b>Organization:</b> {job['company']} ({job['dates']})"
        story.append(Paragraph(j_head, styles['JobHeader']))
        for b in job["bullets"]:
            story.append(Paragraph(f"• {b}", styles['BulletItem']))
        story.append(Spacer(1, 2))

    if candidate.get("projects"):
        story.append(Paragraph("PORTFOLIO & VENTURES", h_style))
        for proj in candidate["projects"]:
            p_head = f"<b>Initiative:</b> {proj['name']} — <i>Stack: {proj['tech']}</i>"
            story.append(Paragraph(p_head, styles['JobHeader']))
            story.append(Paragraph(f"• {proj['description']}", styles['BulletItem']))
            story.append(Spacer(1, 2))

    story.append(Paragraph("ACADEMIC BACKGROUND & CREDENTIALS", h_style))
    story.append(Paragraph(candidate["education"], styles['BodyDark']))

    doc.build(story)

print("PDF Renderer Loaded Successfully.")
