import streamlit as st

st.set_page_config(page_title="Pharmacy CRM Tool", layout="centered")
st.title("🩺 Pharmacist CRM Tool")

option = st.sidebar.selectbox("Choose Service", ["UTI Screening", "OC Resupply", "Dermatology Triage"])

st.markdown("---")

if option == "UTI Screening":
    st.header("Urinary Tract Infection (UTI) Screening")

    age = st.number_input("Age", min_value=0, max_value=120)
    sex = st.radio("Sex", ["Female", "Other"])
    symptoms = st.multiselect("Select all that apply", ["Dysuria", "Urgency", "Frequency", "Suprapubic Pain"])
    exclusions = st.checkbox("Any of the following apply?", help="e.g. Pregnancy, fever, recurrent UTI, renal issues, diabetes, immunosuppressed")

    if sex != "Female" or not (18 <= age <= 65):
        result = "❌ Not eligible: Must be female aged 18–65."
    elif len(symptoms) < 2:
        result = "⚠️ One symptom only. Recommend conservative management and GP review if worsens."
    elif exclusions:
        result = "❌ Exclusion criteria met. Refer to GP for assessment."
    else:
        antibiotic = st.selectbox("Choose treatment", ["Trimethoprim (1 tab nightly x 3)", "Nitrofurantoin (1 tab q6h x 5)", "Cefalexin (1 tab BD x 5)"])
        result = f"✅ Treat with {antibiotic}. Provide urine jar + advise GP follow-up in 48hrs."

    st.markdown("### Summary:")
    st.info(result)

elif option == "OC Resupply":
    st.header("Oral Contraceptive Resupply")

    age = st.number_input("Age", min_value=0, max_value=120)
    reviewed = st.checkbox("Reviewed by GP in last 2 years for contraception?")
    bp_ok = st.checkbox("Blood Pressure within safe range?")
    bmi = st.number_input("BMI")
    issues = st.checkbox("Any of the following?", help="Smoking over 35, migraines with aura, VTE risk, breast cancer history")

    if not reviewed:
        result = "❌ Not eligible: GP review >2 years ago. Refer to GP."
    elif not bp_ok:
        result = "❌ BP not in safe range. Refer to GP."
    elif issues:
        result = "❌ Exclusion criteria met. Refer to GP."
    else:
        result = "✅ Eligible for resupply. Up to 12 months of current OCP. Ensure documentation and counselling."

    st.markdown("### Summary:")
    st.info(result)

elif option == "Dermatology Triage":
    st.header("Dermatology Triage")

    condition = st.selectbox("Choose Condition", ["Impetigo", "Dermatitis", "Plaque Psoriasis", "Herpes Zoster"])

    if condition == "Impetigo":
        result = "✅ Treat with mupirocin (topical). Refer to GP if systemic signs or spreading."
    elif condition == "Dermatitis":
        result = "✅ Recommend emollients and mild corticosteroids. Refer if uncontrolled or widespread."
    elif condition == "Plaque Psoriasis":
        result = "⚠️ Manage mild with topical corticosteroids. Refer moderate–severe to GP/dermatologist."
    elif condition == "Herpes Zoster":
        within_72 = st.checkbox("Is patient within 72 hrs of rash onset?")
        if within_72:
            result = "✅ Start antiviral treatment (e.g. valaciclovir). Educate + monitor for neuralgia."
        else:
            result = "⚠️ Too late for antivirals. Refer to GP for pain management and follow-up."

    st.markdown("### Summary:")
    st.info(result)
