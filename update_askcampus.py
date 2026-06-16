# update_askcampus.py
# Run from D:\college_chatbot\: python update_askcampus.py

import os, json, numpy as np

# ── FACULTY DATA FROM PDF ──────────────────
faculty_data = """EXCEL ENGINEERING COLLEGE - FACULTY LIST

DEPARTMENT OF IT (Information Technology):
Mr.M.Vadivel joined 24.06.2019 designation ASST. PROF and HEAD of IT department.
Dr.N.Sundhararajalu joined 26.10.2022 designation PROFESSOR in IT.
Mr.Naveen.N joined 01.07.2013 designation Asst. Prof in IT.
Ms.S.Kiruthika joined 24.06.2019 designation Asst. Prof in IT.
Ms.E.Annal Sheeba Rani joined 13.08.2019 designation Asst. Prof in IT.
Mr.B.Shanmugaraja joined 06.01.2020 designation Asst. Prof in IT.
Mr.P.Dineshkumar joined 06.01.2020 designation Asst. Prof in IT.
Mr.K.Jegadeesan joined 06.01.2020 designation Asst. Prof in IT.
Mr.J.Balachander joined 07.08.2020 designation Asst. Prof in IT.
Ms.H.Nithasha Banu joined 01.09.2021 designation Asst. Prof in IT.
Mr.G.Prakash joined 01.09.2021 designation Asst. Prof in IT.
Ms.Mouna.S joined 11.11.2021 designation Asst. Prof in IT.
Ms.P.Subitleen Sheeja joined 13.12.2021 designation Asst. Prof in IT.
Mr.Gokul.A joined 25.07.2022 designation Asst. Prof in IT.
Mr.Ganesh shanker.S joined 02.05.2022 designation Asst. Prof in IT.
Mr.Ashok kumar.K joined 11.08.2022 designation Asst. Prof in IT.
Ms.R.Vadivu joined 09.05.2022 designation Asst. Prof in IT.

DEPARTMENT OF CSE (Computer Science and Engineering):
Dr.P.C.Senthil Mahesh joined 16.12.2021 designation Asso. Prof in CSE.
Dr.T.P.Andamuthu joined 05.09.2019 designation Professor in CSE.
Dr.K.Geetha joined 01.03.2010 designation Professor in CSE.
Dr.R.Nedunchelian joined 02.08.2021 designation Professor in CSE.
Dr.A.T.Ravi joined 20.09.2021 designation Professor in CSE.
Dr.S.Sasikala joined 13.05.2020 designation Asst. Prof in CSE.
Ms.P.Kumari joined 02.06.2014 designation Asso. Prof in CSE.
Mr.K.G.Arunkumar joined 01.06.2009 designation Asst. Prof in CSE.
Mr.P.Mohanraj joined 27.05.2011 designation Asst. Prof in CSE.
Mr.V.Surendhiran joined 02.06.2014 designation Asst. Prof in CSE.
Mr.B.Praveenkumar joined 19.06.2017 designation Asst. Prof in CSE.
Dr.L.Ashokkumar joined 13.05.2020 designation Professor in M.E. CSE.

DEPARTMENT OF ECE (Electronics and Communication Engineering):
Dr.S.Anbukaruppusamy joined 15.05.2015 designation PROFESSOR in ECE.
Dr.G.Jagajothi joined 01.07.2022 designation PROFESSOR in ECE.
Dr.G.Prakash joined 03.07.2017 designation PROFESSOR in ECE.
Dr.S.Jayapoorani joined 13.08.2018 designation PROFESSOR in ECE.
Dr.A.Vasantharaj joined 30.06.2014 designation Asso. Prof in ECE.
Mrs.A.Anitharani joined 01.07.2013 designation Asso. Prof in ECE.
Dr.C.Karthikeyini joined 10.10.2019 designation PROFESSOR in M.E. Applied Electronics ECE.

DEPARTMENT OF MECH (Mechanical Engineering):
Dr.E.R.Sivakumar joined 25.07.2022 designation Asso. Prof in MECH.
Dr.M.Venkatesan joined 25.07.2022 designation Asst. Prof in MECH.
Dr.N.Venkatachalam joined 23.06.2014 designation Asso. Prof in MECH.
Dr.K.Boopathy joined 01.08.2014 designation Asso. Prof in MECH.
Mr.S.S.Jayaraman joined 14.06.2010 designation Asst. Prof in MECH.
Dr.N.Natarajan joined 03.06.2020 designation Professor in PG Thermal Engineering MECH.

DEPARTMENT OF CIVIL (Civil Engineering):
Dr.S.Shanmugasundaram joined 17.05.2017 designation Professor and HOD in Civil PG Structural Engineering.
Dr.N.Sengottaian joined 01.03.2007 designation Professor in Civil Environmental Engineering.
Dr.P.Loganathan joined 25.07.2022 designation Asst. Prof in UG Civil Engineering.
Dr.K.P.Vishalakchi joined 25.07.2022 designation Asso. Prof in UG Civil Engineering.

DEPARTMENT OF EEE (Electrical and Electronics Engineering):
Dr.R.Yuvaraj joined 20.10.2021 designation Asst. Prof in EEE.
Dr.V.S.Arulmurugan joined 10.09.2021 designation Prof and Head in PG Power Electronics EEE.
Dr.M.R.Mohanraj joined 10.09.2021 designation ASP in EEE EST.

DEPARTMENT OF AI AND DS (Artificial Intelligence and Data Science):
Mr.Moses.K joined 04.01.2021 designation Asst. Prof in AI and DS.
Ms.Geetha.M joined 04.01.2022 designation Asst. Prof in AI and DS.
Ms.Keruthika.P joined 04.01.2021 designation Asst. Prof in AI and DS.
Ms.Nafisa parveen.N joined 04.01.2021 designation Asst. Prof in AI and DS.
Ms.Pavithra.C joined 06.09.2021 designation Asst. Prof in AI and DS.
Mr.Kalyana krishnan.K joined 04.04.2022 designation Asst. Prof in AI and DS.
Mr.N.Nandakumar joined 06.06.2022 designation Asst. Prof in AI and DS.
Mrs.Eben Exceline joined 06.06.2022 designation Asst. Prof in AI and DS.
Mrs.M.Kannukkiniyal joined 16.03.2021 designation Asst. Prof in AI and DS.

DEPARTMENT OF AERO (Aeronautical Engineering):
Dr.S.P.Venkatesan joined 04.07.2011 designation Asso. Prof in Aero.
Dr.A.Karthikeyan joined 06.07.2010 designation Asso. Prof in Aero.
Dr.M.Gowtham joined 03.03.2022 designation Asst. Prof in Aero.
Dr.P.Karunakaran joined 12.06.2017 designation Professor in M.E. Aeronautical Engineering.
Dr.Sivakumar.C joined 10.09.2021 designation Professor in M.E. Industrial Safety and Engineering Aero.

DEPARTMENT OF BME (Biomedical Engineering):
Dr.K.Bommanna Raja joined 10.10.2019 designation Professor in BME.
Dr.B.Balasubramanian joined 18.02.2021 designation Prof and HOD in BME.
Dr.Saroj Kumar Sah joined 07.03.2022 designation Asst. Prof in BME.
Dr.Sateesh Reddy Avutu joined 21.04.2022 designation Asst. Prof in BME.

DEPARTMENT OF MBA (Master of Business Administration):
Dr.K.Elamvazhuthi joined 01.09.2022 designation Prof and HOD in MBA.
Dr.A.K.Natesan joined 16.09.2021 designation Professor in MBA.
Mr.V.K.Maheskumar joined 17.09.2021 designation Asso. Prof in MBA.
Dr.M.Balasubramanian joined 16.09.2021 designation Professor in MBA Integrated.

DEPARTMENT OF MCA:
Dr.R.Geetha joined 05.01.2022 designation Asso. Prof in MCA.
Mr.Nageswaran.MK joined 31.08.2011 designation Asst. Prof in MCA.
Dr.Gomathi.M joined 24.09.2021 designation Asst. Prof in MCA.
Dr.Gunasekaran.S joined 04.08.2021 designation Asst. Prof in MCA.

DEPARTMENT OF FOOD TECHNOLOGY (FT):
Dr.M.Karuppaiya joined 11.08.2022 designation Professor and HOD in Food Technology.
Dr.M.P.Murugesan joined 01.12.2021 designation Asso. Prof in Food Technology.
Dr.M.Indumathi joined 20.09.2021 designation Asst. Prof in Food Technology.

DEPARTMENT OF CSBS (Computer Science and Business Systems):
Mr.Mathi.V joined 06.09.2021 designation Asst. Prof in CSBS.
Mrs.Ramya Ravi.J joined 06.09.2021 designation Asst. Prof in CSBS.
Mr.Nagaraj.S joined 06.09.2021 designation Asst. Prof in CSBS.
Ms.Nadhiya.S joined 06.09.2021 designation Asst. Prof in CSBS.

DEPARTMENT OF S&H (Science and Humanities):
Dr.K.Sakthivel joined 28.12.2016 designation Prof in Maths.
Dr.S.Mohan Kumar joined 15.04.2021 designation Prof in Maths.
Dr.T.Rameshkumar joined 25.07.2022 designation Asst. Prof in Maths.
Dr.Thomas Mathew joined 18.01.2021 designation Asso Prof in English.
Dr.K.Saravanan joined 25.07.2022 designation Asso Prof in English.
Dr.S.V.Ashokkumar joined 01.08.2022 designation Prof in English.
Dr.R.Rajan joined 18.04.2022 designation Asso Prof in Chemistry.
Dr.N.Prabhu joined 04.11.2020 designation Prof in Physics.
Dr.G.Ganesh joined 04.09.2019 designation Prof in Physics."""

# Write faculty file
os.makedirs('college_data', exist_ok=True)
with open('college_data/faculty.txt', 'w', encoding='utf-8') as f:
    f.write(faculty_data)
print("Created: college_data/faculty.txt")

# Load all existing files
existing_files = [
    'college_data/academics.txt',
    'college_data/exams.txt',
    'college_data/fees.txt',
    'college_data/placement.txt',
    'college_data/scholarships.txt',
    'college_data/hostel.txt',
    'college_data/rules.txt',
    'college_data/events.txt',
    'college_calendar.txt',
    'college_data/faculty.txt'
]

all_chunks = []
chunk_id = 0

for filepath in existing_files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        filename = os.path.basename(filepath)
        sections = [s.strip() for s in content.split('\n\n') if s.strip() and len(s.strip()) > 30]
        for section in sections:
            all_chunks.append({'text': section, 'source': filename, 'chunk_id': chunk_id})
            chunk_id += 1
        print(f"Loaded: {filename} ({len(sections)} chunks)")

print(f"\nTotal chunks: {len(all_chunks)}")
print("Indexing...")

from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer('all-MiniLM-L6-v2')
emb   = model.encode([c['text'] for c in all_chunks], convert_to_numpy=True, show_progress_bar=True).astype('float32')

index = faiss.IndexFlatL2(384)
index.add(emb)

os.makedirs('backend/data/vectordb', exist_ok=True)
faiss.write_index(index, 'backend/data/vectordb/faiss.index')
with open('backend/data/vectordb/metadata.json', 'w', encoding='utf-8') as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print(f"\nSUCCESS! Indexed {index.ntotal} chunks from {len(existing_files)} files!")
print("Now run: python run.py")
print("\nYou can now ask:")
print("  Who is the HOD of IT department?")
print("  Who are the professors in CSE?")
print("  Who joined ECE in 2022?")
print("  List faculty in AI and DS department")
