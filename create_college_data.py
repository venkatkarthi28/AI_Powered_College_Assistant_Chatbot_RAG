# create_college_data.py
# Run from D:\college_chatbot\: python create_college_data.py

import os, json, numpy as np

files = {
"academics.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
ACADEMICS INFORMATION

DEPARTMENTS:
B.E. Computer Science and Engineering (CSE)
B.E. Electronics and Communication Engineering (ECE)
B.E. Mechanical Engineering (MECH)
B.E. Civil Engineering (CIVIL)
B.E. Electrical and Electronics Engineering (EEE)
M.E. Computer Science and Engineering
MBA - Master of Business Administration

CLASS TIMINGS:
Morning Session: 9:30 AM to 12:15 PM
Afternoon Session: 1:00 PM to 4:45 PM

ATTENDANCE:
Minimum attendance required is 75 percent.
Students below 75 percent attendance are not eligible for exams.
Medical leave must be submitted within 3 days.

INTERNAL ASSESSMENT:
3 internal tests per semester.
Internal marks: 20 percent of total marks.
University exam: 80 percent of total marks.""",

"exams.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
EXAMINATION INFORMATION

INTERNAL EXAMS 2026:
Internal Test 1: February 2026
Internal Test 2: March 2026
Internal Test 3: April 2026
Model Exam: May 2026

EXAM RULES:
Hall ticket mandatory for all exams.
No mobile phones allowed in exam hall.
Students must arrive 15 minutes before exam.
Blue or black pen only for writing.

ARREAR EXAMS:
Arrear exam particular subject fee: Rs. 300 or blender like (with pratical ) rs. 500 to 650 per subject.

Results published on coe.excel.result""",

"fees.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
FEE STRUCTURE 2025-2026

TUITION FEES PER YEAR:
B.E. CSE fee: Rs. 95,000 per year
B.E. ECE fee: Rs. 70,000 per year
B.E. Mechanical fee: Rs. 65,000 per year
B.E. Civil fee: Rs. 65,000 per year
B.E. EEE fee: Rs. 68,000 per year
M.E. CSE fee: Rs. 55,000 per year
MBA fee: Rs. 50,000 per year

OTHER FEES:
Admission fee one time: Rs. 5,000
Laboratory fee per semester: Rs. 3,000
Library fee per year: Rs. 1,500
Exam fee per semester: Rs. 850
Late fee fine: Rs. 100 per day after due date

FEE PAYMENT:
First installment due in June at time of admission.
Second installment due in December.
Payment modes: DD, Online transfer, Cash.""",

"placement.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
PLACEMENT INFORMATION

COMPANIES VISITED:
TCS, Infosys, Wipro, HCL Technologies, Cognizant, Capgemini, L&T Technology Services, Zoho Corporation, Amazon, Accenture

PLACEMENT STATISTICS:
Average CTC: Rs. 3.5 LPA
Highest CTC: Rs. 12 LPA
Placement percentage: 85 percent

TRAINING PROVIDED:
Aptitude training from 2nd year.
Communication skills training.
Technical skills: Java, Python, Data Structures.
Mock interviews and group discussions.
Resume writing workshops.

ELIGIBILITY FOR PLACEMENT:
Minimum 60 percent aggregate in all semesters.
No active backlogs at time of placement.
Minimum 75 percent attendance required.""",

"scholarships.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
SCHOLARSHIPS AND FINANCIAL AID

GOVERNMENT SCHOLARSHIPS:
BC/MBC Scholarship: Full fee reimbursement for BC and MBC community students.
SC/ST Scholarship: Full fee reimbursement plus stipend for SC and ST students.
First Graduate Scholarship: Rs. 25,000 per year for first graduate in family.

MERIT SCHOLARSHIPS:
SRET 12th above 175+ cutoff total  freE 
State or National level sports achievers get 25 percent fee waiver.

PRIVATE SCHOLARSHIPS:
Rotary Club scholarship: Rs. 15,000 per year.
Lions Club scholarship: Rs. 10,000 per year.

DOCUMENTS REQUIRED FOR SCHOLARSHIP:
Community certificate, Income certificate below Rs. 2.5 lakh, Previous marksheets, Bank account details, Aadhaar card.""",

"hostel.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
HOSTEL INFORMATION

BOYS HOSTEL:
Capacity: 500 students.
Room types: 2-sharing,4-sharing and 6 sharing .
In-time: 9:00 PM on weekdays.

GIRLS HOSTEL:
Capacity: 400 students.
Room types: 2-sharing and 3-sharing.
In-time: 8:30 PM on weekdays.
Visitors allowed only on Sundays 10 AM to 5 PM.

HOSTEL FEES PER YEAR:
3-sharing room fee: Rs. 45,000 including food.
2-sharing room fee: Rs. 55,000 including food.
Food includes Breakfast, Lunch, and Dinner.

HOSTEL FACILITIES:
24-hour security, CCTV surveillance, Wi-Fi, RO drinking water, Generator backup.

HOSTEL RULES:
No ragging strictly prohibited.
No alcohol or smoking.
Mobile phones allowed but no use after 10 PM.

HOSTEL DAY:
Hostel Day for Boys: 7-Feb-2026.
Hostel Day for Girls: 28-Feb-2026.""",

"rules.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
COLLEGE RULES AND REGULATIONS

DRESS CODE:
Boys must wear formal shirt with dark trousers.
Girls must wear churidar with dupatta or saree.
ID card must be worn at all times.
No jeans, T-shirts, or casual wear allowed in college.

MOBILE PHONE POLICY:
Mobile phones not allowed in classrooms.
Phones must be in silent mode inside college.
Violation results in phone confiscated for 1 week.

LIBRARY RULES:
Library timing: 9 AM to 5 PM.
Maximum 2 books per student at a time.
Books must be returned within 14 days.
Fine for late return: Rs. 2 per day per book.

ANTI-RAGGING:
Ragging is strictly prohibited and leads to immediate expulsion.
Anti-ragging helpline: 1800-180-5522.""",

"events.txt": """EXCEL GROUP INSTITUTIONS - KOMARAPALAYAM
EVENTS AND ACTIVITIES 2026

TECHNICAL EVENTS:
Excellenta 2026: 7-Mar-2026 National Level Technical Symposium.
TART 2026: 28-Mar-2026 Technical And Research Talks.
Entrepreneurship Submit: 27-Mar-2026.

CULTURAL EVENTS:
Freshers Day: August 2026.
Founders Day: 30-Mar-2026.
College Day: February 2026.

SPORTS EVENTS:
Sports Day: January 2026.
Inter-department Cricket Tournament: February 2026.
Volleyball Tournament: March 2026.

SPECIAL EVENTS:
HR Summit and HR Conclave: 12-Feb-2026.
Industry Visit: March 2026.
Alumni Meet: April 2026.
Graduation Ceremony: May 2026.

CLUBS:
NSS National Service Scheme, NCC National Cadet Corps, Rotaract Club, IEEE Student Chapter, CSI Student Chapter, Entrepreneurship Development Cell."""
}

# Write all files
os.makedirs("college_data", exist_ok=True)
for filename, content in files.items():
    with open(os.path.join("college_data", filename), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: college_data/{filename}")

# Also load existing calendar data
calendar_path = "college_calendar.txt"
if os.path.exists(calendar_path):
    with open(calendar_path, "r", encoding="utf-8") as f:
        files["college_calendar.txt"] = f.read()
    print("Loaded: college_calendar.txt")

print("\nIndexing all files...")

from sentence_transformers import SentenceTransformer
import faiss

all_chunks = []
chunk_id = 0

for filename, content in files.items():
    sections = [s.strip() for s in content.split("\n\n") if s.strip() and len(s.strip()) > 30]
    for section in sections:
        all_chunks.append({"text": section, "source": filename, "chunk_id": chunk_id})
        chunk_id += 1

print(f"Total chunks: {len(all_chunks)}")

model = SentenceTransformer("all-MiniLM-L6-v2")
emb   = model.encode([c["text"] for c in all_chunks], convert_to_numpy=True, show_progress_bar=True).astype("float32")

index = faiss.IndexFlatL2(384)
index.add(emb)

os.makedirs(os.path.join("backend","data","vectordb"), exist_ok=True)
faiss.write_index(index, os.path.join("backend","data","vectordb","faiss.index"))
with open(os.path.join("backend","data","vectordb","metadata.json"), "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print(f"\nSUCCESS! Indexed {index.ntotal} chunks from {len(files)} files!")
print("Now run: python run.py")
print("\nYou can now ask:")
print("  What is the fee for B.E. CSE?")
print("  What scholarships are available?")
print("  When is Excellenta 2026?")
print("  What are the hostel fees?")
print("  What companies visit for placement?")
print("  What is the dress code?")
print("  When is pongal celebration?")
