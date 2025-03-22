import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# File path for local storage
excel_file = ""

# Helper function to calculate time in months
def calculate_months(start_date, end_date):
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

# Load existing data or create a new DataFrame
def load_data():
    if os.path.exists(excel_file):
        return pd.read_excel(excel_file)
    else:
        return pd.DataFrame(columns=[
            "MRN", "Date_of_Birth", "Age", "Date_of_Last_Radiotherapy", "Follow_up_date", "Follow_up_time",
            "Histology", "ISUP", "Perineural_Invasion", "LVI", "High_Grade_PIN", "Clinical Stage", "Biopsy_date", "IPSS", "iPSA",
            "Androgen_Deprivation_Therapy", "ADT_type", "ADT_first_date", "ADT_last_date",
            "Use_of_ARATs_or_CYP17A1_inhibitor", "ARATs_first_date", "ARATs_last_date",
            "Chemotherapy", "Chemotherapy_first_date", "Chemotherapy_last_date",
            "Radioligant_Therapy", "Radioligant_Therapy_first_date", "Radioligant_Therapy_last_date",
            "Dose", "Volume", 
            "Fatigue", "Dysuria", "Cystitis", "Bladder_Perforation", "Bladder_Spasms", "Hematuria", "Urinary_Fistula", "Urinary_Frequency", "Urinary_Incontinence", "Urinary_Retention", "Urinary_Obstruction", "Urinary_Urgency",
            "Diarrhea", "Nausea", "Proctitis", "Rectal_Fistula", "Rectal_Hemorrhage", "Rectal_Pain", "Rectal_perforation", "Rectal_Stenosis",
            "Erectile_Dysfunction", "Gynecomastia", "Ejaculation_Disorder", "Testosterone_deficiency", "Overal_tolerance",
            "biochemical_recurrence", "local_recurrence", "regional_recurrence", "distant_recurrence", "death", "Cancer_related_death",
            "time_to_biochemical_recurrence", "time_to_local_recurrence", "time_to_regional_recurrence", "time_to_distant_recurrence", "time_to_death"
        ])

# Function to safely retrieve data, handling NaN values
def safe_get(data, key, default=""):
    value = data.get(key, default)
    return value if pd.notna(value) else default

# Function to safely retrieve a list from stored string values
def safe_get_list(data, key):
    value = data.get(key, "")
    if pd.isna(value) or not isinstance(value, str):
        return []
    return [item.strip() for item in value.replace("[", "").replace("]", "").replace("'", "").split(",") if item]


# Function to fetch existing patient data by MRN
def get_patient_data(mrn):
    df = load_data()
    df["MRN"] = df["MRN"].astype(str).str.strip()
    mrn = str(mrn).strip()
    if mrn in df["MRN"].values:
        return df[df["MRN"] == mrn].iloc[0].to_dict()
    return None

# Function to save patient data (Appending Instead of Overwriting)
def save_data(data):
    df = load_data()
    df["MRN"] = df["MRN"].astype(str).str.strip()
    data["MRN"] = str(data["MRN"]).strip()

    # Append new data as a separate row instead of replacing the existing one
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    # Save the updated DataFrame
    df.to_excel(excel_file, index=False)


# Streamlit app layout
st.title("Patient Information Database - Prostate Prospective Registry")

# Input for MRN
mrn = st.text_input("Enter MRN (Medical Record Number) and press Enter", key="mrn")

# Fetch existing patient data
patient_data = get_patient_data(mrn) if mrn else None

# Start the form
with st.form("patient_form", clear_on_submit=False):
    st.subheader("Patient Details")

    date_of_birth = st.date_input("Date of Birth",
        value=datetime.strptime(safe_get(patient_data, "Date_of_Birth", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today(), min_value=datetime(1900, 1, 1).date(), max_value=datetime.today().date()
    )

    mrn = st.text_input("MRN (Medical Record Number)", value=mrn)

    last_radiotherapy_date = st.date_input("Date of Last Radiotherapy",
        value=datetime.strptime(safe_get(patient_data, "Date_of_Last_Radiotherapy", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    follow_up_date = st.date_input("Date of Follow-up",
        value=datetime.strptime(safe_get(patient_data, "Follow_up_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    Histology = st.multiselect("Histology", ["Acinar Adenocarcinoma", "Adenoid Cystic Carcinoma", "Adenosquamous Carcinoma", "Apocrine Carcinoma", "Cribriform Carcinoma", "Ductal Carcinoma", "Invasive Lobular Carcinoma", "Medullary Carcinoma", "Metaplastic Carcinoma", "Mucinous Carcinoma", "Neuroendocrine Carcinoma", "Papillary Carcinoma", "Squamous Cell Carcinoma", "Tubular Carcinoma", "Others"],
       default=safe_get_list(patient_data, "Histology") if patient_data else []
    )

    ISUP = st.radio("ISUP", ["1", "2", "3", "4", "5", "Not Reported"],
        index=["1", "2", "3", "4", "5", "Not Reported"].index(safe_get(patient_data, "ISUP", "Not Reported")) if patient_data else 5
    )
    with st.expander("ISUP Classification"):
        st.write("ISUP 1 = Gleason 3+3")
        st.write("ISUP 2 = Gleason 3+4")
        st.write("ISUP 3 = Gleason 4+3")
        st.write("ISUP 4 = Gleason 4+4, 3+5, 5+3")
        st.write("ISUP 5 = Gleason 4+5, 5+4, 5+5")
        

    Perineural_Invasion = st.radio("Perineural_Invasion", ["Negative", "Positive", "Not Reported"],
        index=["Negative", "Positive", "Not Reported"].index(safe_get(patient_data, "Perineural_Invasion", "Not Reported")) if patient_data else 0
    )

    LVI = st.radio("LVI", ["Negative", "Positive"],
        index=["Negative", "Positive"].index(safe_get(patient_data, "PR", "Negative")) if patient_data else 0
    )

    High_Grade_PIN = st.radio("PIN", ["Absent", "Present", "Not Reported"],
        index=["Absent", "Present", "Not Reported"].index(safe_get(patient_data, "High_Grade_PIN", "Not Reported")) if patient_data else 0
    )
    st.warning("High-grade prostatic intraepithelial neoplasia (PIN)")

    Clinical_Stage = st.multiselect("Clinical Stage", ["cT1a", "cT1b", "cT1c", "cT2a", "cT2b", "cT2c", "cT3a", "cT3b", "cT4", "cN0", "cN1", "M0", "M1"],
        default=safe_get_list(patient_data, "Clinical Stage") if patient_data else []
    )

    Biopsy_date = st.date_input("Date of Biopsy",
        value=datetime.strptime(safe_get(patient_data, "Surgery_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    IPSS = st.number_input("IPSS", min_value=0, max_value=35, step=1, value=int(safe_get(patient_data, "IPSS", 0)) if patient_data else 0
    )

    st.warning("Not sure how to calculate the IPSS? Click [here](https://www.mdcalc.com/calc/10462/american-urological-association-symptom-index-aua-si#why-use) to use the official AUA Symptom Index calculator.")


    iPSA = st.number_input("iPSA",min_value=0, max_value=10000, step=1, value=int(safe_get(patient_data, "iPSA", 0)) if patient_data else 0
    )


    # Systemic Treatment
    st.subheader("Systemic Treatment")
    Androgen_Deprivation_Therapy = st.multiselect("Androgen_Deprivation_Therapy", ["LHRH Agonist", "LHRH Antagonist", "Orchiectomy", "Antiandrogen", "Combination Therapy", "None"]),
    if Androgen_Deprivation_Therapy : ("LHRH Agonist", "LHRH Antagonist", "Orchiectomy", "Antiandrogen", "Combination Therapy"),
    ADT_first_date = st.date_input("First Date of ADT",
            value=datetime.strptime(safe_get(patient_data, "ADT_first_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    ADT_last_date = st.date_input("Last Date of ADT",
            value=datetime.strptime(safe_get(patient_data, "ADT_last_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )

    Use_of_ARATs_or_CYP17A1_inhibitor = st.multiselect("ARATs or CYP17A1 Inhibitor", ["None","Abiraterone", "Enzalutamide", "Apalutamide", "Darolutamide"]),
    if Use_of_ARATs_or_CYP17A1_inhibitor  : ("Abiraterone", "Enzalutamide", "Apalutamide", "Darolutamide"),
    ARATs_first_date = st.date_input("First Date of ARATs",
            value=datetime.strptime(safe_get(patient_data, "ARATs_first_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    ARATs_last_date = st.date_input("Last Date of ARATs",
            value=datetime.strptime(safe_get(patient_data, "ARATs_last_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    
    Chemotherapy = st.multiselect("Chemotherapy", ["None", "Docetaxel", "Cabazitaxel", "Mitoxantrone", "Carboplatin", "Cisplatin", "Vinblastine", "Vinorelbine", "Paclitaxel", "Docetaxel", "Etoposide", "Gemcitabine", "Ifosfamide", "Methotrexate", "Mitomycin", "Pemetrexed", "Topotecan", "Vincristine", "Vinorelbine", "Others"]),
    if Chemotherapy : ("Docetaxel", "Cabazitaxel", "Mitoxantrone", "Carboplatin", "Cisplatin", "Vinblastine", "Vinorelbine", "Paclitaxel", "Docetaxel", "Etoposide", "Gemcitabine", "Ifosfamide", "Methotrexate", "Mitomycin", "Pemetrexed", "Topotecan", "Vincristine", "Vinorelbine", "Others"),
    Chemotherapy_first_date = st.date_input("First Date of Chemotherapy",   
            value=datetime.strptime(safe_get(patient_data, "Chemotherapy_first_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    Chemotherapy_last_date = st.date_input("Last Date of Chemotherapy",
            value=datetime.strptime(safe_get(patient_data, "Chemotherapy_last_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    default=safe_get_list(patient_data, "Chemotherapy") if patient_data else []

    Radioligant_Therapy = st.multiselect("Radioligant Therapy", ["None","Radium-223", "Lu-177", "Ac-225", "Others"]),
    if Radioligant_Therapy : ("Radium-223", "Lu-177", "Ac-225", "Others"),
    Radioligant_Therapy_first_date = st.date_input("First Date of Radioligant Therapy",
            value=datetime.strptime(safe_get(patient_data, "Radioligant_Therapy_first_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    Radioligant_Therapy_last_date = st.date_input("Last Date of Radioligant Therapy",
            value=datetime.strptime(safe_get(patient_data, "Radioligant_Therapy_last_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    default=safe_get_list(patient_data, "Radioligant_Therapy") if patient_data else []

    # Treatment Details
    st.subheader("Treatment Details")
    Dose = st.multiselect("Dose", ["35Gy", "36.25Gy", "25Gy", "40Gy", "Others"],
    default=safe_get_list(patient_data, "Dose") if patient_data else []
    )
    
    Volume = st.multiselect("Volume", ["Partial Prostate", "Whole Prostate", "Proximal SV", "Whole SV", "Nodal Elective", "Nodal Boost", "Bony boost", "Others"],
    default=safe_get_list(patient_data, "Volume") if patient_data else []
    )

    st.markdown("<hr style='border: 2px solid #666; margin: 20px 0;'>", unsafe_allow_html=True)

    # Side effects
    st.subheader("Urinary Side Effects")

    Fatigue = st.radio("Fatigue", ["None", "I", "II", "III"])
    with st.expander("Fatigue Classification"):
        st.write("Grade 0: No fatigue")
        st.write("Grade I: Mild fatigue; no change in activity")
        st.write("Grade II: Moderate fatigue; limiting instrumental ADL")
        st.write("Grade III: Severe fatigue; limiting self care ADL")

    Dysuria = st.radio("Dysuria (CTCAE v5)", ["Present", "Absent"])
    
    Cystitis = st.radio("Cystitis (CTCAE v5)", ["None", "I", "II", "III", "IV", "V"])
    with st.expander("Cystitis Classification"):
        st.write("Grade 0: No change")
        st.write("Grade I: Microscopic hematuria; minimal increase in frequency, urgency, dysuria, or nocturia; new onset of incontinence ")
        st.write("Grade II: Moderate hematuria; moderate increase in frequency, urgency, dysuria, nocturia or incontinence; urinary catheter placement or bladder irrigation indicated; limiting instrumental ADL ")     
        st.write("Grade III: Gross hematuria; transfusion, IV medications, or hospitalization indicated; elective invasive intervention indicated ")
        st.write("Grade IV: Life-threatening consequences; urgent invasive intervention indicated ")
        st.write("Grade V: Death")

    Bladder_Perforation = st.radio("Bladder Perforation (CTCAE v5)", ["Absent", "II", "III", "IV", "V"])
    with st.expander("Bladder Perforation Classification"):
        st.write("Absent: No change")
        st.write("Grade II: Invasive intervention not indicated ")
        st.write("Grade III: Symptomatic; medical intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Bladder_Spasms = st.radio("Bladder Spasms (CTCAE v5)", ["Absent", "I", "II", "III"])
    with st.expander("Bladder Spasms Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Intervention not indicated")
        st.write("Grade II: Antispasmodics indicated")
        st.write("Grade III: Hospitalization indicated ")

    Hematuria = st.radio("Hematuria (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Hematuria Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic; urinary catheter or bladder irrigation indicated; limiting instrumental ADL")
        st.write("Grade III: Gross hematuria; transfusion, IV medications, or hospitalization indicated; elective invasive intervention indicated; limiting self care ADL")
        st.write("Grade IV: Life-threatening consequences; urgent invasive intervention indicated")
        st.write("Grade V: Death")

    Urinary_Fistula = st.radio("Urinary Fistula (CTCAE v5)", ["Absent", "II", "III", "IV", "V"])
    with st.expander("Urinary Fistula Classification"):
        st.write("Absent: No change")
        st.write("Grade II: Invasive intervention not indicated ")
        st.write("Grade III: Symptomatic; medical intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Urinary_Frequency = st.radio("Urinary Frequency (CTCAE v5)", ["Absent", "I", "II"])
    with st.expander("Urinary Frequency Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Mild increase in frequency; intervention not indicated")
        st.write("Grade II: Moderate increase in frequency; limiting instrumental ADL")

    Urinary_Incontinence = st.radio("Urinary Incontinence (CTCAE v5)", ["Absent", "I", "II", "III"])
    with st.expander("Urinary Incontinence Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Occasional, pads not indicated")
        st.write("Grade II: Spontaneous; pads indicated; limiting instrumental ADL ")
        st.write("Grade III: Intervention indicated (e.g., clamp, collagen injections); operative intervention indicated; limiting self care ADL ")

    Urinary_Retention = st.radio("Urinary Retention (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Urinary Retention Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Urinary, suprapubic or intermittent catheter placement not indicated; able to void with some residual")
        st.write("Grade II: Placement of urinary, suprapubic or intermittent catheter placement indicated; medication indicated")
        st.write("Grade III: Elective invasive intervention indicated; substantial loss of affected kidney function or mass")
        st.write("Grade IV: Life-threatening consequences; organ failure; urgent operative intervention indicated")
        st.write("Grade V: Death")

    Urinary_Obstruction = st.radio("Urinary Obstruction (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Urinary Obstruction Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic but no hydronephrosis, sepsis, or renal dysfunction; urethral dilation, urinary or suprapubic catheter indicated")
        st.write("Grade III: Altered organ function (e.g., hydronephrosis or renal dysfunction); invasive intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Urinary_Urgency = st.radio("Urinary Urgency (CTCAE v5)", ["Absent", "I", "II"])
    with st.expander("Urinary Urgency Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Mild increase in frequency; intervention not indicated")
        st.write("Grade II: Moderate increase in frequency; limiting instrumental ADL")

    # Side Effects - Gastrointestinal
    st.subheader("Gastrointestinal Side Effects")

    Diarrhea = st.radio("Diarrhea (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Diarrhea Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Increase of <4 stools/day over baseline; mild increase in ostomy output compared to baseline")
        st.write("Grade II: Increase of 4-6 stools/day over baseline; moderate increase in ostomy output compared to baseline; limiting instrumental ADL")
        st.write("Grade III: Increase of ≥7 stools/day over baseline; incontinence; limiting self care ADL")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")
    
    Nausea = st.radio("Nausea (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Nausea Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Loss of appetite without alteration in eating habits")
        st.write("Grade II: Oral intake decreased without significant weight loss, dehydration, or malnutrition; IV fluids indicated <24 hrs")
        st.write("Grade III: Inadequate oral caloric or fluid intake; tube feeding or TPN indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")
    
    Proctitis = st.radio("Proctitis (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Proctitis Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic (e.g., rectal discomfort, passing blood or mucus); medical intervention indicated; limiting instrumental ADL ")
        st.write("Grade III: Severe symptoms; fecal urgency or stool incontinence; limiting self care ADL ")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Rectal_Fistula = st.radio("Rectal Fistula (CTCAE v5)", ["Absent", "I" "II", "III", "IV", "V"])
    with st.expander("Rectal Fistula Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic, Invasive intervention not indicated ")
        st.write("Grade III: Symptomatic; medical intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Rectal_Hemorrhage = st.radio("Rectal Hemorrhage (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Rectal Hemorrhage Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Minimal bleeding identified on imaging; intervention not indicated")
        st.write("Grade II: Moderate bleeding; medical intervention indicated")
        st.write("Grade III: Transfusion, radiologic, endoscopic or elective operative intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")
    
    Rectal_Pain = st.radio("Rectal Pain (CTCAE v5)", ["Absent", "I", "II", "III"])
    with st.expander("Rectal Pain Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Mild discomfort; analgesics not indicated")
        st.write("Grade II: Moderate pain; analgesics indicated; limiting instrumental ADL")
        st.write("Grade III: Severe pain; limiting self care ADL")

    Rectal_perforation = st.radio("Rectal Perforation (CTCAE v5)", ["Absent", "II", "III", "IV", "V"])
    with st.expander("Rectal Perforation Classification"):
        st.write("Absent: No change")
        st.write("Grade II: Invasive intervention not indicated ")
        st.write("Grade III: Symptomatic; medical intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")
    
    Rectal_Stenosis = st.radio("Rectal Stenosis (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Rectal Stenosis Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic; medical intervention indicated")
        st.write("Grade III: Severe symptoms; limiting self care ADL ")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    #Sexual Side Effects
    st.subheader("Sexual Side Effects")

    Erectile_Dysfunction = st.radio("Erectile Dysfunction (CTCAE v5)", ["Absent", "I", "II", "III"])
    with st.expander("Erectile Dysfunction Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Decrease in erectile function (frequency or rigidity of erections) but intervention not indicated (e.g., medication or use of mechanical device, penile pump)")
        st.write("Grade II: Decrease in erectile function (frequency/rigidity of erections), erectile intervention indicated, (e.g., medication or mechanical devices such as penile pump)")
        st.write("Grade III: Decrease in erectile function (frequency/rigidity of erections) but erectile intervention not helpful (e.g., medication or mechanical devices such as penile pump); placement of a permanent penile prosthesis indicated (not previously present)")

    Gynecomastia = st.radio("Gynecomastia (CTCAE v5)", ["Absent", "I", "II", "III"])
    with st.expander("Gynecomastia Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Mild; asymptomatic or mild symptoms; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Moderate; minimal, local or noninvasive intervention indicated; limiting instrumental ADL")
        st.write("Grade III: Severe symptoms; elective operative intervention indicated")

    Ejaculation_Disorder = st.radio("Ejaculation Disorder (CTCAE v5)", ["Absent", "I", "II"])
    with st.expander("Ejaculation Disorder Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Diminished ejaculation ")
        st.write("Grade II: Anejaculation or retrograde ejaculation")
    
    Testosterone_deficiency = st.radio("Testosterone deficiency (CTCAE v5)", ["Absent", "I", "II"])
    with st.expander("Testosterone deficiency Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic; medical intervention indicated")

    Overal_tolerance = st.radio("Overall Tolerance", ["Excellent", "Good", "Fair", "Poor"])

    # Recurrence details
    st.subheader("Recurrence Details")
    biochemical_recurrence = st.radio("Biochemical Recurrence", ["No", "Yes"])
    local_recurrence = st.radio("Local Recurrence", ["No", "Yes"])
    regional_recurrence = st.radio("Regional Recurrence", ["No", "Yes"])
    distant_recurrence = st.radio("Distant Recurrence", ["No", "Yes"])
    death = st.radio("Death", ["No", "Yes"])

    time_to_biochemical_recurrence = None
    if biochemical_recurrence == "Yes":
        time_to_biochemical_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Biochemical Recurrence"))

    time_to_local_recurrence = None
    if local_recurrence == "Yes":
        time_to_local_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Local Recurrence"))

    time_to_regional_recurrence = None
    if regional_recurrence == "Yes":
        time_to_regional_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Regional Recurrence"))

    time_to_distant_recurrence = None
    if distant_recurrence == "Yes":
        time_to_distant_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Distant Recurrence"))

    death_date = None
    if death == "Yes":
        Cancer_related_death = st.radio("Cancer Related Death", ["No", "Yes"])
        time_to_death = calculate_months(last_radiotherapy_date, st.date_input("Date of Death"))

    # Submit button to trigger calculation
    submitted = st.form_submit_button("Calculate")

    if submitted:
        st.session_state.age = datetime.today().year - date_of_birth.year - (
            (datetime.today().month, datetime.today().day) < (date_of_birth.month, date_of_birth.day)
        )
        st.session_state.time_since_treatment = calculate_months(last_radiotherapy_date, follow_up_date)
        st.session_state.time_to_biochemical_recurrence = time_to_biochemical_recurrence if biochemical_recurrence == "Yes" else "N/A"
        st.session_state.time_to_local_recurrence = time_to_local_recurrence if local_recurrence == "Yes" else "N/A"
        st.session_state.time_to_regional_recurrence = time_to_regional_recurrence if regional_recurrence == "Yes" else "N/A"
        st.session_state.time_to_distant_recurrence = time_to_distant_recurrence if distant_recurrence == "Yes" else "N/A"
        st.session_state.time_to_death = time_to_death if death == "Yes" else "N/A"

        st.subheader("Calculated Results:")
        st.write(f"**Calculated Age**: {st.session_state.age} years")
        st.write(f"**Time since last radiotherapy**: {st.session_state.time_since_treatment} months")
        if biochemical_recurrence == "Yes":
            st.write(f"**Time to biochemical recurrence**: {st.session_state.time_to_biochemical_recurrence} months")
        if local_recurrence == "Yes":
            st.write(f"**Time to local recurrence**: {st.session_state.time_to_local_recurrence} months")
        if regional_recurrence == "Yes":
            st.write(f"**Time to regional recurrence**: {st.session_state.time_to_regional_recurrence} months")
        if distant_recurrence == "Yes":
            st.write(f"**Time to distant recurrence**: {st.session_state.time_to_distant_recurrence} months")
        if death == "Yes":
            st.write(f"**Time to death**: {st.session_state.time_to_death} months")

# Save button is placed outside the form so it persists after submission
if st.button("Save Information"):
    if st.session_state.age is None or st.session_state.time_since_treatment is None:
        st.error("Please calculate the age and treatment times before saving.")
    else:
        data = {
            # Patient details
            "MRN": mrn if mrn else "N/A",
            "Date_of_Birth": date_of_birth.strftime("%Y-%m-%d"),
            "Age": st.session_state.age,
            "Date_of_Last_Radiotherapy": last_radiotherapy_date.strftime("%Y-%m-%d"),
            "Follow_up_date": follow_up_date.strftime("%Y-%m-%d"),
            "Follow_up_time": st.session_state.time_since_treatment,
            "Histology": Histology,
            "ISUP": ISUP,
            "Perineural_Invasion": Perineural_Invasion,
            "LVI": LVI,
            "High_Grade_PIN": High_Grade_PIN,
            "Clinical_Stage": Clinical_Stage,
            "Biopsy_date": Biopsy_date.strftime("%Y-%m-%d"),
            "IPSS": IPSS,
            "iPSA": iPSA,
            # Systemic Treatment
            "Androgen_Deprivation_Therapy": Androgen_Deprivation_Therapy,
            "ADT_first_date": ADT_first_date.strftime("%Y-%m-%d"),
            "ADT_last_date": ADT_last_date.strftime("%Y-%m-%d"),
            "Use_of_ARATs_or_CYP17A1_inhibitor": Use_of_ARATs_or_CYP17A1_inhibitor,
            "ARATs_first_date": ARATs_first_date.strftime("%Y-%m-%d"),
            "ARATs_last_date": ARATs_last_date.strftime("%Y-%m-%d"),
            "Chemotherapy": Chemotherapy,
            "Chemotherapy_first_date": Chemotherapy_first_date.strftime("%Y-%m-%d"),
            "Chemotherapy_last_date": Chemotherapy_last_date.strftime("%Y-%m-%d"),
            "Radioligant_Therapy": Radioligant_Therapy,
            "Radioligant_Therapy_first_date": Radioligant_Therapy_first_date.strftime("%Y-%m-%d"),
            "Radioligant_Therapy_last_date": Radioligant_Therapy_last_date.strftime("%Y-%m-%d"),
            # Treatment Details
            "Dose": Dose,
            "Volume": Volume,
            # Side Effects
            "Fatigue": Fatigue,
            "Dysuria": Dysuria,
            "Cystitis": Cystitis,
            "Bladder_Perforation": Bladder_Perforation,
            "Bladder_Spasms": Bladder_Spasms,
            "Hematuria": Hematuria,
            "Urinary_Fistula": Urinary_Fistula,
            "Urinary_Frequency": Urinary_Frequency,
            "Urinary_Incontinence": Urinary_Incontinence,
            "Urinary_Retention": Urinary_Retention,
            "Urinary_Obstruction": Urinary_Obstruction,
            "Urinary_Urgency": Urinary_Urgency,
            "Diarrhea": Diarrhea,
            "Nausea": Nausea,
            "Proctitis": Proctitis,
            "Rectal_Fistula": Rectal_Fistula,
            "Rectal_Hemorrhage": Rectal_Hemorrhage,
            "Rectal_Pain": Rectal_Pain,
            "Rectal_perforation": Rectal_perforation,
            "Rectal_Stenosis": Rectal_Stenosis,
            "Erectile_Dysfunction": Erectile_Dysfunction,
            "Gynecomastia": Gynecomastia,
            "Ejaculation_Disorder": Ejaculation_Disorder,
            "Testosterone_deficiency": Testosterone_deficiency,
            "Overal_tolerance": Overal_tolerance,
            # Recurrence Details
            "Biochemical_recurrence": biochemical_recurrence,
            "Time_to_biochemical_recurrence": st.session_state.time_to_biochemical_recurrence if biochemical_recurrence == "Yes" else "N/A",
            "Local_recurrence": local_recurrence,
            "Time_to_local_recurrence": st.session_state.time_to_local_recurrence if local_recurrence == "Yes" else "N/A",
            "Regional_recurrence": regional_recurrence,
            "Time_to_regional_recurrence": st.session_state.time_to_regional_recurrence if regional_recurrence == "Yes" else "N/A",
            "Distant_recurrence": distant_recurrence,
            "Time_to_distant_recurrence": st.session_state.time_to_distant_recurrence if distant_recurrence == "Yes" else "N/A",
            "Cancer Related Death": Cancer_related_death if death == "Yes" else "N/A",
            "Death": death,
            "time_to_death": st.session_state.time_to_death if death == "Yes" else "N/A",
        }
        save_data(data)
        st.success("Patient data has been successfully saved!")
