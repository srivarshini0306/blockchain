import streamlit as st
import hashlib
import json

# Function to generate a hash for data integrity
def generate_hash(patient_name, treatment, cost, date_of_visit):
    hash_input = f"{patient_name}{treatment}{cost}{date_of_visit}"
    return hashlib.sha256(hash_input.encode()).hexdigest()

# Initialize the hospital ledger
if "hospital_ledger" not in st.session_state:
    st.session_state.hospital_ledger = {}

st.title("🏥 Advanced Hospital Ledger")

# Add patient visit
st.header("Add or Update Patient Visit")
patient_name = st.text_input("Enter Patient's Name")
treatment = st.text_input("Enter Treatment Received")
cost = st.number_input("Enter Cost of Treatment ($)", min_value=0.0, format="%.2f")
date_of_visit = st.date_input("Enter Date of Visit")

if st.button("Add Visit"):
    if patient_name and treatment and cost and date_of_visit:
        visit_hash = generate_hash(patient_name, treatment, cost, str(date_of_visit))
        visit = {
            "treatment": treatment,
            "cost": cost,
            "date_of_visit": str(date_of_visit),
            "visit_hash": visit_hash
        }

        if patient_name not in st.session_state.hospital_ledger:
            st.session_state.hospital_ledger[patient_name] = []

        st.session_state.hospital_ledger[patient_name].append(visit)
        st.success(f"Visit added for {patient_name} on {date_of_visit}.")
        st.json(visit)  # Show visit details
    else:
        st.error("Please enter all details correctly.")

# Search patient visits
st.header("Search Patient Visit Records")
search_patient = st.text_input("Enter Patient Name to Search")

if st.button("Search"):
    if search_patient in st.session_state.hospital_ledger:
        st.write(f"### Visit records for {search_patient}:")
        for visit in st.session_state.hospital_ledger[search_patient]:
            st.json(visit)
    else:
        st.warning(f"No records found for {search_patient}.")

# Display complete ledger
st.header("📜 Full Hospital Ledger")
st.json(st.session_state.hospital_ledger)
