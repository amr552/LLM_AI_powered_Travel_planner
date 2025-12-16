import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError, AuthenticationError, APIConnectionError, BadRequestError

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY. Put it in your .env file.")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a senior travel planner.

Rules:
- Keep the plan SHORT and actionable.
- No JSON, no tables wider than the page.
- Avoid long explanations.
- Always include: itinerary by day, budget split, key bookings checklist, local transport, safety tips.
- Respect constraints: budget, days, group size, accommodation type, guided/unguided, purpose, and restrictions (e.g., no alcohol, halal-friendly).
- If the user gave no city, propose 1–2 key cities only (not many).
Output format EXACTLY:

Trip Summary:
Assumptions:
Day-by-Day Plan:
Budget Split:
Bookings Checklist:
Transport Notes:
Packing (short):
Safety/Local Tips:
"""

def generate_travel_plan(
    country: str,
    days: int,
    budget_amount: float,
    budget_currency: str,
    tour_type: str,
    travelers: int,
    accommodation: str,
    guided: str,
    purpose: str,
    side_budget_amount: float,
    restrictions: str,
    notes: str
) -> str:
    country = (country or "").strip()
    if not country:
        return "Please enter a country (e.g., Italy, Turkey, Japan)."
    if days < 1:
        return "Days must be at least 1."

    user_prompt = f"""
Country: {country}
Trip length: {days} days
Main budget: {budget_amount} {budget_currency}
Extra/side budget: {side_budget_amount} {budget_currency}
Tour type: {tour_type}
Travelers: {travelers}
Accommodation: {accommodation}
Guide: {guided}
Purpose: {purpose}
Restrictions/preferences: {restrictions}
Extra notes: {notes}

Keep it short.
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.4,
            max_tokens=350,  # token-efficient
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        return (resp.choices[0].message.content or "").strip()

    except RateLimitError:
        return "API quota exceeded (429). Check billing/quota."
    except AuthenticationError:
        return "Invalid API key. Check OPENAI_API_KEY."
    except APIConnectionError:
        return "Network error. Try again."
    except BadRequestError as e:
        return f"Request error: {e}"
