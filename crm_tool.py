import streamlit as st

st.set_page_config(page_title="Pharmacist CRM Tool", layout="centered")
st.title("🩺 Pharmacist CRM Tool")

st.markdown("#### Step 1: Universal Intake")

with st.form("intake_form"):
    age = st.number_input("Patient age", min_value=0, max_value=120)
    sex = st.radio("Sex at birth", ["Female", "Male", "Other"])
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
    skin_condition = st.selectbox("Suspected skin condition (if any):", [
        "None", "Impetigo", "Dermatitis", "Plaque Psoriasis", "Herpes Zoster"
    ])
    submit = st.form_submit_button("Check Eligibility")

if submit:
    st.markdown("---")
    st.subheader("Step 2: Eligibility Summary")

    eligible_uti = (sex == "Female" and 18 <= age <= 65 and len(uti_symptoms) >= 2 
                    and not pregnant and not immunocompromised)
    eligible_oc = (sex == "Female" and on_oc and age >= 16 and gp_reviewed 
                   and bp_safe and not smoker_over_35 
                   and not migraine_aura and not vte_history and not cancer_history)
    eligible_derm = (skin_condition != "None")

    st.markdown("#### 🔍 Eligibility:")
    if eligible_uti:
        st.success("✅ Eligible for UTI screening")
    else:
        st.warning("🚫 Not eligible for UTI screening")

    if eligible_oc:
        st.success("✅ Eligible for OC resupply")
    else:
        st.warning("🚫 Not eligible for OC resupply")

    if eligible_derm:
        st.success(f"✅ Eligible for Dermatology – {skin_condition}")
    else:
        st.warning("🚫 No dermatology condition selected")

    st.markdown("---")
    st.subheader("Step 3: Choose Triage Module")

    module = st.radio("Select service to continue:", 
                      options=[m for m, ok in {
                          "UTI": eligible_uti, 
                          "OC Resupply": eligible_oc, 
                          skin_condition: eligible_derm
                      }.items() if ok and m != "None"])

    summary = ""

    # --- UTI ---
    if module == "UTI":
        st.markdown("### 💊 UTI Screening")
        antibiotic = st.selectbox("Recommended treatment:", [
            "Trimethoprim 300mg (1 at night for 3 nights)",
            "Nitrofurantoin 100mg (QID for 5 days)",
            "Cefalexin 500mg (BD for 5 days)"
        ])
        st.markdown("**Patient should:**")
        st.markdown("- Start antibiotics now")
        st.markdown("- Keep a urine sample refrigerated before first dose")
        st.markdown("- Follow up with GP if not improved in 48 hrs")
        st.success(f"✅ Treat with: {antibiotic}")

        summary = f"""Pharmacist Consultation Summary
--------------------------------
Service: UTI Screening
Age: {age}
Sex: {sex}
Symptoms: {', '.join(uti_symptoms)}
Exclusions: None flagged
Treatment: {antibiotic}
Notes:
- Urine sample before first dose
- GP review in 48 hrs if not improved
"""

    # --- OC Resupply ---
    elif module == "OC Resupply":
        st.markdown("### 💊 Oral Contraceptive Resupply")
        st.success("✅ Patient eligible for 12-month resupply.")
        summary = f"""Pharmacist Consultation Summary
--------------------------------
Service: OC Resupply
Age: {age}
Sex: {sex}
BP Safe: Yes
GP Review: Yes
Contraindications: None flagged
Treatment: Continue current oral contraceptive (max 12-month supply)
Notes:
- Document BP, BMI, counselling
- Upload to dispensing system / My Health Record
"""

# CONTINUED IN PART 2 BELOW ↓↓↓
    # --- Dermatology Modules ---
    elif module == "Impetigo":
        st.markdown("### 🩹 Impetigo Triage")
        severe = st.checkbox("Is the infection spreading or systemic?")
        if severe:
            advice = "Refer to GP for systemic antibiotics."
        else:
            advice = "Treat with topical mupirocin. Educate on hygiene and crust removal."
        st.success(advice)
        summary = f"""Pharmacist Consultation Summary
--------------------------------
Service: Dermatology – Impetigo
Age: {age}
Sex: {sex}
Treatment Plan:
- {advice}
"""

    elif module == "Dermatitis":
        st.markdown("### 🩹 Dermatitis Triage")
        area = st.selectbox("Severity area involved:", ["Localised", "Widespread"])
        infected = st.checkbox("Signs of secondary infection (oozing, crusts)?")
        if infected or area == "Widespread":
            advice = "Refer to GP for further assessment."
        else:
            advice = "Recommend emollients and low-potency topical corticosteroids."
        st.success(advice)
        summary = f"""Pharmacist Consultation Summary
--------------------------------
Service: Dermatology – Dermatitis
Age: {age}
Sex: {sex}
Treatment Plan:
- {advice}
"""

    elif module == "Plaque Psoriasis":
        st.markdown("### 🩹 Psoriasis Triage")
        areas = st.slider("Estimated body area involved (%)", 0, 100, 5)
        has_joint_pain = st.checkbox("Associated joint pain or nail involvement?")
        if areas >= 10 or has_joint_pain:
            advice = "Refer to GP or dermatologist. Moderate–severe case."
        else:
            advice = "Manage with topical corticosteroids. Recommend moisturiser + trigger avoidance."
        st.success(advice)
        summary = f"""Pharmacist Consultation Summary
--------------------------------
Service: Dermatology – Plaque Psoriasis
Age: {age}
Sex: {sex}
Severity: {areas}% BSA
Treatment Plan:
- {advice}
"""

    elif module == "Herpes Zoster":
        st.markdown("### 🩹 Herpes Zoster Triage")
        onset_72 = st.checkbox("Onset <72 hrs ago?")
        immune_safe = not immunocompromised
        if onset_72 and immune_safe:
            advice = "Start antivirals. Educate on pain and post-herpetic neuralgia."
        else:
            advice = "Refer to GP – outside treatment window or high-risk patient."
        st.success(advice)
        summary = f"""Pharmacist Consultation Summary
--------------------------------
Service: Dermatology – Herpes Zoster
Age: {age}
Sex: {sex}
Onset <72 hrs: {'Yes' if onset_72 else 'No'}
Treatment Plan:
- {advice}
"""

    # --- Step 4: Report Generator ---
    st.markdown("---")
    st.subheader("Step 4: Generate Report")

    if summary:
        st.code(summary, language="text")
        st.download_button("📄 Download Summary", summary, file_name="pharmacist_summary.txt")
        st.markdown("### 💬 Submit to WellnessVC:")
        st.markdown("[Open Contact Form](https://www.wellnessvc.com.au/contact)")
        st.markdown("Paste this report into the message box for pharmacist consultation logging.")
