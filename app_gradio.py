import gradio as gr
from travel_ai import generate_travel_plan

CURRENCIES = ["EUR", "USD", "KWD", "GBP", "TRY"]
TOUR_TYPES = ["City break", "Nature", "Adventure", "Beach", "Cultural", "Shopping", "Mixed"]
ACCOM = ["Hostel", "Budget hotel", "Mid-range hotel", "Luxury hotel", "Apartment/Airbnb"]
GUIDE = ["Without guide (self-guided)", "With guide (some days)", "Fully guided"]
PURPOSE = ["Leisure", "Honeymoon", "Family trip", "Business + leisure", "Religious/Spiritual", "Study/Conference"]

def gradio_plan(country, days, budget_amount, currency, tour_type, travelers, accommodation, guided, purpose, halal_mode, other_restrictions, side_budget, notes):
    restrictions = "Halal-friendly: no alcohol; family-friendly." if halal_mode else "None"
    if other_restrictions and other_restrictions.strip():
        restrictions = f"{restrictions} | {other_restrictions.strip()}"

    return generate_travel_plan(
        country=country,
        days=int(days),
        budget_amount=float(budget_amount),
        budget_currency=currency,
        tour_type=tour_type,
        travelers=int(travelers),
        accommodation=accommodation,
        guided=guided,
        purpose=purpose,
        side_budget_amount=float(side_budget),
        restrictions=restrictions,
        notes=notes or ""
    )

with gr.Blocks(title="AI Travel Planner") as demo:
    gr.Markdown("# AI Travel Planner\nShort, budget-aware itineraries powered by an LLM.")

    country = gr.Textbox(label="Country", placeholder="e.g., Italy, Turkey, Japan")
    days = gr.Slider(1, 30, value=7, step=1, label="Number of days")

    with gr.Row():
        budget_amount = gr.Number(label="Main budget", value=300)
        currency = gr.Dropdown(CURRENCIES, value="EUR", label="Currency")

    side_budget = gr.Number(label="Extra/side budget", value=0)
    travelers = gr.Slider(1, 10, value=2, step=1, label="Number of travelers")

    with gr.Row():
        tour_type = gr.Dropdown(TOUR_TYPES, value="Mixed", label="Tour type")
        accommodation = gr.Dropdown(ACCOM, value="Mid-range hotel", label="Accommodation")

    with gr.Row():
        guided = gr.Dropdown(GUIDE, value=GUIDE[0], label="Guide option")
        purpose = gr.Dropdown(PURPOSE, value="Leisure", label="Purpose")

    halal_mode = gr.Checkbox(value=False, label="Halal-friendly (no alcohol, family-friendly)")
    other_restrictions = gr.Textbox(label="Other restrictions", placeholder="e.g., avoid long walks, wheelchair access")
    notes = gr.Textbox(label="Extra notes", placeholder="e.g., prefer museums, local food, day trips")

    btn = gr.Button("Generate Plan")
    output = gr.Markdown()

    btn.click(
        fn=gradio_plan,
        inputs=[country, days, budget_amount, currency, tour_type, travelers, accommodation, guided, purpose, halal_mode, other_restrictions, side_budget, notes],
        outputs=[output],
    )

if __name__ == "__main__":
    demo.launch(server_port=7860)
