# update_college_data.py
# Run from D:\college_chatbot\: python update_college_data.py

import os, json, numpy as np

files = {
"academics.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
SECTION: ACADEMICS

The B.E Information Technology program consists of 8 semesters.
Minimum attendance required per semester is 75 percent.
Total credits required to complete B.E IT is 160 credits.
Internal assessments are conducted twice per semester.
Each internal exam carries 50 marks.
CGPA is calculated on a 10-point grading scale.
Elective subjects are offered from 5th semester onwards.
Students must complete mini project in 6th semester.
Final year project is conducted in 8th semester.

DEPARTMENTS:
B.E. Computer Science and Engineering CSE
B.E. Electronics and Communication Engineering ECE
B.E. Mechanical Engineering MECH
B.E. Civil Engineering CIVIL
B.E. Electrical and Electronics Engineering EEE
M.E. Computer Science and Engineering
MBA Master of Business Administration

CLASS TIMINGS:
Morning Session 9:30 AM to 12:15 PM
Afternoon Session 1:00 PM to 4:45 PM

INTERNAL ASSESSMENT:
3 internal tests per semester.
Internal marks 20 percent of total marks.
University exam 80 percent of total marks.""",

"exams.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
SECTION: EXAMS

End semester examinations are conducted in December and May.
Hall tickets can be downloaded from student portal one week before exams.
Minimum pass mark is 50 percent in each subject.
Students can apply for supplementary exams if they fail.
Revaluation must be applied within 5 days after results.
Results are published within 30 days after exam completion.
Malpractice during exams leads to disciplinary action.

INTERNAL EXAMS 2026:
Internal Test 1 February 2026
Internal Test 2 March 2026
Internal Test 3 April 2026
Model Exam May 2026

EXAM RULES:
Hall ticket mandatory for all exams.
No mobile phones allowed in exam hall.
Students must arrive 15 minutes before exam.
Blue or black pen only for writing.

ARREAR EXAMS:
Arrear exam fee it be single paper means Rs. 350 or it be Blender like core paper with praatical paper means it be RS.450 to 550 per subject.
Maximum 3 attempts allowed per subject.""",

"fees.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
SECTION: FEES

Annual tuition fee for B.E IT is Rs. 95,000.
Hostel fee per year is Rs. 60,000.
Last date for fee payment is July 31st.
Late payment penalty is Rs. 1,000.
Fees can be paid via online portal or bank transfer.
Installment payment option is available upon request.

TUITION FEES PER YEAR:
B.E. CSE fee Rs. 95,000 per year
B.E. ECE fee Rs. 90,000 per year
B.E. Mechanical fee Rs. 65,000 per year
B.E. Civil fee Rs. 65,000 per year
B.E. EEE fee Rs. 68,000 per year
B.E. IT fee Rs. 95,000 per year
M.E. CSE fee Rs. 55,000 per year
MBA fee Rs. 50,000 per year

OTHER FEES:
Admission fee one time Rs. 5,000
Laboratory fee per semester Rs. 3,000
Library fee per year Rs. 1,500
Exam fee per semester Rs. 850
Late fee fine Rs. 100 per day after due date""",

"placement.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
SECTION: PLACEMENT

Minimum eligibility for campus placement is 7.0 CGPA with no active arrears.
Placement training starts from 3rd year.
Top recruiters include TCS, Infosys, Wipro, Accenture.
Highest package offered last year was Rs. 8 LPA.
Average package is Rs. 4 LPA.
Students with arrears are not eligible for placements.

COMPANIES VISITED:
TCS Tata Consultancy Services, Infosys, Wipro, HCL Technologies, Cognizant, Capgemini, L&T Technology Services, Zoho Corporation, Amazon, Accenture

PLACEMENT STATISTICS:
Average CTC Rs. 3.5 LPA
Highest CTC Rs. 12 LPA
Placement percentage 85 percent

ELIGIBILITY FOR PLACEMENT:
Minimum 60 percent aggregate in all semesters.
No active backlogs at time of placement.
Minimum 75 percent attendance required.""",

"scholarships.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
SECTION: SCHOLARSHIPS

Government scholarships are available for eligible students.
First graduate scholarship is available for first graduate in family.
Merit-based scholarships require CGPA above 8.5.
Scholarship application deadline is October 15th.

GOVERNMENT SCHOLARSHIPS:
BC/MBC Scholarship: BC/MBC students are received 4500 to 1200 per year .
SC/ST Scholarship: Full fee reimbursement plus stipend for SC and ST students.
First Graduate Scholarship: Rs. 25,000 per year.

MERIT SCHOLARSHIPS:
SRET Scholorship - 12th above 175+ cutoff full free. and SC Scholorship are available etc.

PRIVATE SCHOLARSHIPS:
Rotary Club scholarship Rs. 15,000 per year.
Lions Club scholarship Rs. 10,000 per year.

DOCUMENTS REQUIRED:
Community certificate, Income certificate below Rs. 2.5 lakh, Previous marksheets, Bank account details, Aadhaar card.""",

"hostel.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
SECTION: HOSTEL

Separate hostel facilities are available for boys and girls.
Hostel in-time is 8:30 PM.
WiFi facility is available in hostel.
Visitors allowed only during weekends.
Ragging is strictly prohibited in hostel.

BOYS HOSTEL:
Capacity 500 students.
Room types 2-sharing,4 -sharing, and 6 per sharing .
In-time 9:00 PM on weekdays.

GIRLS HOSTEL:
Capacity 400 students.
In-time 8:30 PM on weekdays.
Visitors allowed only on Sundays 10 AM to 5 PM.

HOSTEL FEES PER YEAR:
3-sharing room fee Rs. 45,000 including food.
2-sharing room fee Rs. 55,000 including food.
Hostel fee per year is Rs. 60,000.
Food includes Breakfast Lunch and Dinner.

HOSTEL FACILITIES:
24-hour security, CCTV surveillance, Wi-Fi, RO drinking water, Generator backup.

HOSTEL DAY:
Hostel Day for Boys 7-Feb-2026.
Hostel Day for Girls 28-Feb-2026.""",

"rules.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
SECTION: RULES

Students must wear formal dress on working days.
Mobile phones are not allowed in classrooms.
ID card must be carried at all times.
Violation of rules may result in suspension.
Ragging is strictly prohibited and leads to expulsion.

DRESS CODE:
Boys must wear formal shirt with dark trousers.
Girls must wear churidar with dupatta or saree.
No jeans T-shirts or casual wear allowed in college.

MOBILE PHONE POLICY:
Mobile phones not allowed in classrooms.
Phones must be in silent mode inside college.
Violation results in phone confiscated for 1 week.

LIBRARY RULES:
Library timing 9 AM to 5 PM.
Maximum 2 books per student at a time.
Books must be returned within 14 days.
Fine for late return Rs. 2 per day per book.

ANTI-RAGGING:
Ragging is strictly prohibited.
Anti-ragging helpline 1800-180-5522.""",

"events.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
SECTION: EVENTS

Annual cultural fest is conducted every February.
Technical symposium is conducted once per year.
Workshops are organized every semester.
Students can register for events through the college portal.
Faculty coordinators manage all events.

TECHNICAL EVENTS:
Excellenta 2026 on 7-Mar-2026 National Level Technical Symposium.
TART 2026 on 28-Mar-2026 Technical And Research Talks.
Entrepreneurship Submit on 27-Mar-2026.

CULTURAL EVENTS:
Freshers Day August 2026.
Founders Day 30-Mar-2026.
College Day February 2026.

SPORTS EVENTS:
Sports Day January 2026.
Inter-department Cricket Tournament February 2026.
Volleyball Tournament March 2026.

SPECIAL EVENTS:
HR Summit and HR Conclave 12-Feb-2026.
Industry Visit March 2026.
Alumni Meet April 2026.
Graduation Ceremony May 2026.

CLUBS:
NSS National Service Scheme, NCC National Cadet Corps, Rotaract Club, IEEE Student Chapter, CSI Student Chapter.""",

"college_calendar.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
SEMESTER SCHEDULE 2026

JANUARY 2026 HOLIDAYS:
1-Jan-2026 Thursday New Year Day Holiday
10-Jan-2026 Saturday Pongal Celebration
15-Jan-2026 Thursday Pongal Holiday
16-Jan-2026 Friday Thiruvalluvar Day Holiday
17-Jan-2026 Saturday Uzhavar Thirunal Holiday
26-Jan-2026 Monday Republic Day Holiday
12-Jan-2026 to 14-Jan-2026 Holiday for Students

FEBRUARY 2026:
7-Feb-2026 Saturday Hostel Day for Boys
12-Feb-2026 Thursday HR Summit and HR Conclave
20-Feb-2026 Friday Holiday for Students
21-Feb-2026 Saturday Holiday for Students and Staff
28-Feb-2026 Saturday Hostel Day for Girls

MARCH 2026:
7-Mar-2026 Saturday Excellenta 2026 Event
19-Mar-2026 Thursday Telugu New Years Day Holiday
21-Mar-2026 Saturday Ramzan Idul Fitr Holiday
27-Mar-2026 Friday Entrepreneurship Submit
28-Mar-2026 Saturday TART 2026 Holiday for Students
30-Mar-2026 Monday Founders Day
31-Mar-2026 Tuesday Mahaveer Jayanthi

APRIL 2026:
3-Apr-2026 Friday Good Friday Holiday
13-Apr-2026 Monday Holiday for Students
14-Apr-2026 Tuesday Tamil New Years Day and Ambedkars Birthday Holiday

MAY 2026:
1-May-2026 Friday May Day Holiday
28-May-2026 Thursday Bakrid Idul Azha Holiday"""
}

# Write all files to college_data folder
os.makedirs("college_data", exist_ok=True)
for filename, content in files.items():
    with open(os.path.join("college_data", filename), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: college_data/{filename}")

print("\nIndexing all files into FAISS...")

from sentence_transformers import SentenceTransformer
import faiss

all_chunks = []
chunk_id = 0

for filename, content in files.items():
    sections = [s.strip() for s in content.split("\n\n") if s.strip() and len(s.strip()) > 30]
    for section in sections:
        all_chunks.append({"text": section, "source": filename, "chunk_id": chunk_id})
        chunk_id += 1

print(f"Total chunks to index: {len(all_chunks)}")

model = SentenceTransformer("all-MiniLM-L6-v2")
emb   = model.encode([c["text"] for c in all_chunks], convert_to_numpy=True, show_progress_bar=True).astype("float32")

index = faiss.IndexFlatL2(384)
index.add(emb)

os.makedirs(os.path.join("backend","data","vectordb"), exist_ok=True)
faiss.write_index(index, os.path.join("backend","data","vectordb","faiss.index"))
with open(os.path.join("backend","data","vectordb","metadata.json"), "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print(f"\nSUCCESS! Indexed {index.ntotal} chunks from {len(files)} files!")
print("\nNow run: python run.py")
print("\nTest these questions:")
print("  What is the fee for B.E. IT?")
print("  What is the minimum CGPA for placement?")
print("  What is the scholarship deadline?")
print("  When is Excellenta 2026?")
print("  What are hostel rules?")
print("  What is the dress code?")
print("  When is pongal celebration?")
