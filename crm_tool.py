import streamlit as st

st.set_page_config(page_title="Pharmacist CRM Tool", layout="centered")
st.title("🩺 Pharmacist CRM Tool")

st.markdown("#### Step 1: Universal Intake")

# --- Universal Patient Intake ---
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
    submit = st.form_submit_button("Check Eligibility")

# --- Eligibility Engine ---
if submit:
    st.markdown("---")
    st.subheader("Step 2: Eligibility Summary")

    eligible_uti = (sex == "Female" and 18 <= age <= 65 and len(uti_symptoms) >= 2 
                    and not pregnant and not immunocompromised)
    eligible_oc = (sex == "Female" and on_oc and age >= 16 and gp_reviewed 
                   and bp_safe and not smoker_over_35 
                   and not migraine_aura and not vte_history and not cancer_history)
    eligible_derm = True  # Always allow derm triage

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
        st.success("✅ Eligible for Dermatology triage")

    # --- Triage Module Selector ---
    st.markdown("---")
    st.subheader("Step 3: Choose Triage Module")

    module = st.radio("Select available service to proceed:", 
                      options=[m for m, ok in {
                          "UTI": eligible_uti, 
                          "OC Resupply": eligible_oc, 
                          "Dermatology": eligible_derm
                      }.items() if ok])

    # --- UTI Module ---
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

    # --- OC Module Placeholder ---
    elif module == "OC Resupply":
        st.markdown("### 💊 OC Resupply Summary")
        st.success("✅ Patient eligible for 12-month resupply. Ensure documentation, record in dispensing software, and upload to My Health Record if applicable.")

    # --- Dermatology Module Placeholder ---
    elif module == "Dermatology":
        st.markdown("### 🩹 Dermatology Triage")
        condition = st.selectbox("Select condition:", [
            "Impetigo", "Dermatitis", "Plaque Psoriasis", "Herpes Zoster"
        ])

        if condition == "Impetigo":
            st.success("✅ Treat with topical mupirocin. Refer if widespread/systemic.")
        elif condition == "Dermatitis":
            st.success("✅ Recommend emollients + low-mid corticosteroid. Refer if uncontrolled.")
        elif condition == "Plaque Psoriasis":
            st.warning("⚠️ Mild can be managed with topicals. Moderate-severe = refer to GP/dermatologist.")
        elif condition == "Herpes Zoster":
            within_72 = st.checkbox("Onset <72 hrs ago?")
            if within_72:
                st.success("✅ Start antivirals. Educate about pain and post-herpetic neuralgia.")
            else:
                st.warning("⚠️ Refer to GP for symptom control (too late for antivirals).")

