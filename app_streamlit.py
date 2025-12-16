import streamlit as st
from travel_ai import generate_travel_plan

st.set_page_config(page_title="AI Travel Planner", layout="wide")
st.title("AI Travel Planner")
st.write("Generate a short, budget-aware travel plan using an LLM.")

with st.sidebar:
    st.header("Trip Inputs")
    country = st.text_input("Country", placeholder="e.g., Italy, Turkey, Japan")
    days = st.slider("Number of days", 1, 30, 7, 1)

    colA, colB = st.columns(2)
    with colA:
        budget_amount = st.number_input("Main budget", min_value=0.0, value=300.0, step=50.0)
    with colB:
        budget_currency = st.selectbox("Currency", ["EUR", "USD", "KWD", "GBP", "TRY"], index=0)

    side_budget_amount = st.number_input("Extra/side budget", min_value=0.0, value=0.0, step=25.0)
    travelers = st.slider("Travelers (friends/family)", 1, 10, 2, 1)

    tour_type = st.selectbox("Tour type", ["City break", "Nature", "Adventure", "Beach", "Cultural", "Shopping", "Mixed"], index=6)
    accommodation = st.selectbox("Accommodation", ["Hostel", "Budget hotel", "Mid-range hotel", "Luxury hotel", "Apartment/Airbnb"], index=2)
    guided = st.selectbox("Guide option", ["Without guide (self-guided)", "With guide (some days)", "Fully guided"], index=0)
    purpose = st.selectbox("Purpose", ["Leisure", "Honeymoon", "Family trip", "Business + leisure", "Religious/Spiritual", "Study/Conference"], index=0)

    halal_mode = st.checkbox("Halal-friendly (no alcohol, family-friendly)", value=False)
    restrictions_extra = st.text_input("Other restrictions", placeholder="e.g., no nightlife, wheelchair access, avoid long walks")
    notes = st.text_area("Extra notes", placeholder="e.g., prefer museums, day trips, local markets, low walking, etc.")

restrictions = "Halal-friendly: no alcohol; family-friendly spots." if halal_mode else "None"
if restrictions_extra.strip():
    restrictions = f"{restrictions} | {restrictions_extra.strip()}"

if st.button("Generate Travel Plan", type="primary"):
    with st.spinner("Generating..."):
        result = generate_travel_plan(
            country=country,
            days=int(days),
            budget_amount=float(budget_amount),
            budget_currency=budget_currency,
            tour_type=tour_type,
            travelers=int(travelers),
            accommodation=accommodation,
            guided=guided,
            purpose=purpose,
            side_budget_amount=float(side_budget_amount),
            restrictions=restrictions,
            notes=notes or ""
        )
    st.markdown(result)
