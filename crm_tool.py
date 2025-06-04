import streamlit as st
from datetime import date
from PIL import Image

# --- Load Logos ---
pharma_logo = Image.open("pharmaprograms_logo.png")
wellness_logo = Image.open("wellnessvc_logo.png")

# --- Page Setup ---
st.set_page_config(page_title="Pharmacist CRM Tool", layout="centered")

col1, col2 = st.columns([1, 6])
with col1:
    st.image(pharma_logo, width=100)
with col2:
    st.title("Pharmacist CRM Tool")

st.markdown("#### Step 1: Patient & Pharmacist Intake")

# --- Intake Form ---
with st.form("intake_form"):
    st.markdown("##### 🧍 Patient Information")
    fname = st.text_input("First name*")
    lname = st.text_input("Surname*")
    dob = st.date_input("Date of Birth*", max_value=date.today())
    sex = st.selectbox("Sex*", ["Female", "Male", "Other"])
    street = st.text_input("Street")
    suburb = st.text_input("Suburb")
    postcode = st.text_input("Postcode")
    state = st.text_input("State")
    mobile = st.text_input("Mobile number")
    phone = st.text_input("Phone number (optional)")
    email = st.text_input("Email address")
    medicare = st.text_input("Medicare number (optional)")
    medicare_expiry = st.text_input("Medicare expiry (MM/YY)")
    dva = st.text_input("DVA (optional)")

    st.markdown("##### 👩‍⚕️ Pharmacist Details")
    consult_date = st.date_input("Consultation date*", value=date.today())
    pharmacist_name = st.text_input("Pharmacist full name*", value="Your Name")
    ahpra = st.text_input("AHPRA No.", value="PHA000XXXX")

    st.markdown("##### 🧾 Clinical Screening")
    pregnant = st.checkbox("Pregnant or <6 weeks postpartum")
    smoker_over_35 = st.checkbox("Smoker or vapes (age >35)?")
    on_oc = st.checkbox("Currently using oral contraception?")
    bp_safe = st.checkbox("Blood pressure within safe range?")
    gp_reviewed = st.checkbox("Reviewed by GP for contraception in past 2 years?")
    migraine_aura = st.checkbox("History of migraine with aura?")
    vte_history = st.checkbox("History of VTE or high clotting risk?")
    cancer_history = st.checkbox("Breast cancer history?")
    immunocompromised = st.checkbox("Immunocompromised or on immunosuppressants?")
    travel_recent = st.checkbox("Recent overseas travel (past 6 months)?")
    uti_symptoms = st.multiselect("UTI symptoms (select all that apply):", 
                                  ["Dysuria", "Urgency", "Frequency", "Suprapubic Pain"])
    skin_condition = st.selectbox("Suspected skin condition:", [
        "None", "Impetigo", "Dermatitis", "Plaque Psoriasis", "Herpes Zoster"
    ])
    submit = st.form_submit_button("Check Eligibility")

# --- Logic Engine ---
if submit:
    st.markdown("---")
    st.subheader("Step 2: Eligibility Summary")

    age = date.today().year - dob.year
    eligible_uti = (sex == "Female" and 18 <= age <= 65 and len(uti_symptoms) >= 2 
                    and not pregnant and not immunocompromised)
    eligible_oc = (sex == "Female" and on_oc and age >= 16 and gp_reviewed 
                   and bp_safe and not smoker_over_35 
                   and not migraine_aura and not vte_history and not cancer_history)
    eligible_derm = (skin_condition != "None")

    if eligible_uti:
        st.success("✅ Eligible for UTI screening")
    else:
        st.warning("🚫 Not eligible for UTI")

    if eligible_oc:
        st.success("✅ Eligible for OC resupply")
    else:
        st.warning("🚫 Not eligible for OC resupply")

    if eligible_derm:
        st.success(f"✅ Eligible for Dermatology – {skin_condition}")
    else:
        st.warning("🚫 No dermatology condition selected")

    st.subheader("Step 3: Choose Module")
    module = st.radio("Proceed to:", [
        m for m, ok in {
            "UTI": eligible_uti, 
            "OC Resupply": eligible_oc, 
            skin_condition: eligible_derm
        }.items() if ok and m != "None"
    ])

    # --- Clinical Triage Logic ---
    summary = ""

    if module == "UTI":
        antibiotic = st.selectbox("Recommended treatment:", [
            "Trimethoprim 300mg (1 at night for 3 nights)",
            "Nitrofurantoin 100mg (QID for 5 days)",
            "Cefalexin 500mg (BD for 5 days)"
        ])
        st.success("Start treatment. Advise urine sample + GP review in 48 hrs.")
        summary = f"""UTI Consultation Summary
Patient: {fname} {lname}, {age} y/o {sex}
Symptoms: {', '.join(uti_symptoms)}
Treatment: {antibiotic}
Notes: Urine sample advised. GP review in 48 hrs if not improved."""

    elif module == "OC Resupply":
        st.success("Eligible for 12-month continuation of current OC.")
        summary = f"""OC Resupply Summary
Patient: {fname} {lname}, {age} y/o {sex}
No UKMEC contraindications.
Recommendation: Resupply up to 12 months. Document BP, BMI, counselling."""

    elif module == "Impetigo":
        severe = st.checkbox("Spreading/systemic?")
        if severe:
            advice = "Refer to GP for oral antibiotics."
        else:
            advice = "Topical mupirocin recommended."
        st.success(advice)
        summary = f"Dermatology – Impetigo\nAdvice: {advice}"

    elif module == "Dermatitis":
        infected = st.checkbox("Signs of infection?")
        area = st.selectbox("Severity:", ["Localised", "Widespread"])
        if infected or area == "Widespread":
            advice = "Refer to GP."
        else:
            advice = "Emollients + mild topical corticosteroids."
        st.success(advice)
        summary = f"Dermatology – Dermatitis\nAdvice: {advice}"

    elif module == "Plaque Psoriasis":
        bsa = st.slider("Body area affected (%)", 0, 100, 5)
        pain = st.checkbox("Joint/nail involvement?")
        if bsa > 10 or pain:
            advice = "Refer for systemic management."
        else:
            advice = "Topical corticosteroids + moisturiser."
        st.success(advice)
        summary = f"Dermatology – Psoriasis\nBSA: {bsa}%\nAdvice: {advice}"

    elif module == "Herpes Zoster":
        onset = st.checkbox("Onset <72 hours ago?")
        if onset and not immunocompromised:
            advice = "Start antivirals. Educate re: pain."
        else:
            advice = "Refer to GP for management."
        st.success(advice)
        summary = f"Dermatology – Shingles\nAdvice: {advice}"

    # --- Step 4: Summary + WellnessVC Contact ---
    st.markdown("---")
    st.subheader("Step 4: Summary + Referral")

    full_summary = f"""Pharmacist Consultation Summary
----------------------------
Patient: {fname} {lname}
DOB: {dob}, Sex: {sex}
Pharmacist: {pharmacist_name}, AHPRA: {ahpra}
Consultation Date: {consult_date}

{summary}
"""

    st.text_area("📋 Summary", value=full_summary, height=200)
    st.download_button("📄 Download Summary", full_summary, file_name="consultation_summary.txt")

    # --- Always Show WellnessVC Contact ---
    st.markdown("---")
    st.markdown("### 🩺 Telehealth Referral Option (WellnessVC)")
    colA, colB = st.columns([1, 5])
    with colA:
        st.image(wellness_logo, width=80)
    with colB:
        st.markdown("If the patient is ineligible or prefers telehealth, refer to:")
        st.markdown("[📩 Contact WellnessVC Telehealth](https://www.wellnessvc.com.au/contact)")

