"""
======================================================
create_sample_pdf.py — Generate Test Data
======================================================
This script creates a sample college FAQ PDF that you
can upload to the chatbot to test it immediately.

Run ONCE before testing:
    python create_sample_pdf.py

Then upload the generated "sample_college_faq.pdf"
through the Admin Panel at http://localhost:5000/admin
"""

import os

def create_sample_pdf():
    """Create a sample college FAQ PDF using reportlab."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import cm
        from reportlab.lib import colors
    except ImportError:
        print("ReportLab not installed. Install with: pip install reportlab")
        print("\nAlternatively, create your own PDF manually and upload it.")
        print("The PDF should contain college information like fees, admissions, courses, etc.")
        return

    output_path = "sample_college_faq.pdf"
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'],
                                  fontSize=20, spaceAfter=20, textColor=colors.darkblue)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
                               fontSize=14, spaceAfter=10, textColor=colors.blue)
    body_style = styles['Normal']
    body_style.fontSize = 11
    body_style.leading = 18

    content = []

    # ── Cover ────────────────────────────────────────
    content.append(Paragraph("Greenfield Institute of Technology", title_style))
    content.append(Paragraph("Student Information & FAQ Guide 2024–25", styles['Heading2']))
    content.append(Spacer(1, 0.5*cm))
    content.append(Paragraph(
        "This document contains official information about admissions, fees, "
        "courses, hostel facilities, and college policies.",
        body_style
    ))
    content.append(Spacer(1, 1*cm))

    # ── Admissions ───────────────────────────────────
    content.append(Paragraph("1. Admissions & Eligibility", h2_style))
    content.append(Paragraph(
        "Admission to B.E. programs is based on merit in the State Common Entrance Test (CET). "
        "Students must have completed 10+2 (HSC) with Physics, Chemistry, and Mathematics as "
        "mandatory subjects with a minimum aggregate of 45% marks (40% for reserved categories).",
        body_style
    ))
    content.append(Spacer(1, 0.3*cm))
    content.append(Paragraph(
        "Admission Process: Apply online at www.greenfield.ac.in/admissions. "
        "Upload required documents (mark sheets, caste certificate if applicable, Aadhaar card). "
        "Pay application fee of ₹500 online. Merit list will be published on 15th June 2024.",
        body_style
    ))
    content.append(Spacer(1, 0.5*cm))

    # ── Courses ──────────────────────────────────────
    content.append(Paragraph("2. Available B.E. Programs", h2_style))
    programs = [
        ("Computer Engineering", "120 seats", "4 years"),
        ("Information Technology", "180 seats", "4 years"),
        ("Electronics & Telecommunication", "60 seats", "4 years"),
        ("Mechanical Engineering", "60 seats", "4 years"),
        ("Civil Engineering", "60 seats", "4 years"),
        ("Artificial Intelligence & Data Science", "60  seats", "4 years"),
    ]
    for name, seats, duration in programs:
        content.append(Paragraph(
            f"• {name} — {seats}, {duration}, affiliated to Mumbai University",
            body_style
        ))
    content.append(Spacer(1, 0.5*cm))

    # ── Fees ─────────────────────────────────────────
    content.append(Paragraph("3. Fee Structure 2026–27", h2_style))
    content.append(Paragraph(
        "Tuition Fee: ₹95,000 per year for all B.E. programs. "
        "Placement  Fee: ₹5,000 per year. "
        "Examination Fee: ₹5,000 per semester. "
        "Total Annual Fee: ₹1,05,000 approximately.",
        body_style
    ))
    content.append(Spacer(1, 0.3*cm))
    content.append(Paragraph(
        "Fee Payment: Fees can be paid online via the student portal or at the accounts office. "
        "Fees are due before 30th July each year. Late payment attracts a fine of ₹500 per month. "
        "Demand Draft should be drawn in favor of 'Greenfield Institute of Technology'.",
        body_style
    ))
    content.append(Spacer(1, 0.5*cm))

    # ── Scholarships ─────────────────────────────────
    content.append(Paragraph("4. Scholarships & Financial Aid", h2_style))
    content.append(Paragraph(
        "Government Scholarships: OBC, SC, ST, NT category students are eligible for state "
        "government EBC/Freeship scholarship. Apply at mahadbt.maharashtra.gov.in before 31st August.",
        body_style
    ))
    content.append(Paragraph(
        "Merit Scholarship:SRET 12th above 175+ cutoff totally free and  Students scoring above 90% in CET receive 25% tuition fee waiver. "
        ,
        body_style
    ))
    content.append(Paragraph(
        "Institute Scholarship:SRET 12th above 175+ cutoff total  freE Students maintaining CGPA above 8.5 in each semester receive "
        ,
        body_style
    ))
    content.append(Spacer(1, 0.5*cm))

    # ── Hostel ───────────────────────────────────────
    content.append(Paragraph("5. Hostel & Accommodation", h2_style))
    content.append(Paragraph(
        "Boys Hostel: 200 seats available in 3-sharing and 2-sharing rooms. "
        "Hostel fee: ₹60,000 per year including meals. "
        "Amenities: Wi-Fi, laundry, gym, common room with TV, 24-hour security.",
        body_style
    ))
    content.append(Paragraph(
        "Girls Hostel: 150 seats available in 2-sharing rooms. "
        "Hostel fee: ₹65,000 per year including meals. "
        "Amenities: Wi-Fi, laundry, indoor games room, CCTV surveillance, female warden.",
        body_style
    ))
    content.append(Paragraph(
        "Hostel applications open from 1st June to 30th June. "
        "Priority given to students coming from districts more than 100 km away.",
        body_style
    ))
    content.append(Spacer(1, 0.5*cm))

    # ── Documents ────────────────────────────────────
    content.append(Paragraph("6. Documents Required for Admission", h2_style))
    docs_needed = [
        "SSC (10th) Mark Sheet — Original + 2 Photocopies",
        "HSC (12th) Mark Sheet — Original + 2 Photocopies",
        "CET Score Card — Original + 2 Photocopies",
        "Leaving Certificate from last school/college",
        "Aadhar Card — Original + 2 Photocopies",
        "Passport-size photographs — 6 copies",
        "Caste Certificate (if applicable) — Original + 2 Photocopies",
        "Income Certificate (if applying for scholarship)",
        "Migration Certificate (if from other board)",
    ]
    for doc_item in docs_needed:
        content.append(Paragraph(f"• {doc_item}", body_style))
    content.append(Spacer(1, 0.5*cm))

    # ── Calendar ─────────────────────────────────────
    content.append(Paragraph("7. Important Dates 2024–25", h2_style))
    dates = [
        ("Application Portal Opens", "1st June 2024"),
        ("Last Date to Apply", "15th June 2024"),
        ("First Merit List Published", "20th June 2024"),
        ("Document Verification", "25–30 June 2024"),
        ("Fee Payment Deadline (Round 1)", "5th July 2024"),
        ("Second Merit List (if seats available)", "10th July 2024"),
        ("Academic Year Begins", "22nd July 2024"),
        ("Orientation Program for New Students", "22–23 July 2024"),
    ]
    for event, date in dates:
        content.append(Paragraph(f"• {event}: {date}", body_style))
    content.append(Spacer(1, 0.5*cm))

    # ── Contact ──────────────────────────────────────
    content.append(Paragraph("8. Contact Information", h2_style))
    content.append(Paragraph(
        "Admissions Office: excelinstitutions.com | +91-9842713789 "
        "(Monday–Friday, 9 AM–5 PM)",
        body_style
    ))
    content.append(Paragraph(
        "College Address: NH -544,Salem Main Road, Komarapalayam Namakkal District - 637303",
        body_style
    ))
    content.append(Paragraph(
        "Website: www.greenfield.ac.in | Student Helpline: 1800-XXX-XXXX (Toll Free)",
        body_style
    ))

    # Build the PDF
    doc.build(content)
    print(f"\n✅ Sample PDF created: {output_path}")
    print(f"   Size: {os.path.getsize(output_path) / 1024:.1f} KB")
    print("\nNext steps:")
    print("  1. Start the chatbot: python run.py")
    print("  2. Open Admin Panel: http://localhost:5000/admin")
    print(f"  3. Upload '{output_path}'")
    print("  4. Open Chatbot: http://localhost:5000")
    print("  5. Ask: 'What is the fee structure for B.E. programs?'")


if __name__ == "__main__":
    create_sample_pdf()
