# utils.py (updated)

import pandas as pd
import textwrap
import json

def extract_keywords(user_query, keyword_map):
    query = user_query.lower()
    found_keywords = []
    matched_specialties = set()

    for specialty, keywords in keyword_map.items():
        for keyword in keywords:
            if keyword in query:
                found_keywords.append(keyword)
                matched_specialties.add(specialty)

    return found_keywords, list(matched_specialties)


def filter_doctors_by_specialty(df, specialties):
    if not specialties:
        # No specialties found → return empty
        return pd.DataFrame()
    filtered = df[df['Specialty'].isin(specialties)]
    return filtered


def search_doctors_private(user_query, df, client):
    """
    Calls the LLM/GROQ to rank/filter doctors for the user query.
    Expects df to already be filtered by specialty.
    Returns DataFrame with 'Reasoning' column added.
    """
    if df.empty:
        return pd.DataFrame()  # no doctors available

    # 1️⃣ Create a small summary for the LLM
    llama_summary = ""
    for idx, row in df.iterrows():
        llama_summary += f"ID {idx}: {row['Specialty']} ({row['Experience (Years)']} yrs)\n"

    # 2️⃣ Prompt the LLM to rank doctors and provide reasoning
    prompt = f"""
A patient reports: "{user_query}"

Available doctors:
{llama_summary}

STRICT OUTPUT RULES:
Return a valid JSON ONLY with format:
{{
  "results": [
    {{"id": "ID_NUMBER", "reasoning": "..." }}
  ]
}}
Each reasoning should be 1-2 concise sentences explaining why this doctor is a match.
Do NOT include any extra text outside JSON.
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    # 3️⃣ Parse the response safely
    raw_text = completion.choices[0].message.content.strip()

    try:
        ai_response = json.loads(raw_text)
        top_picks = ai_response.get("results", [])
    except json.JSONDecodeError:
        # fallback if LLM failed → just pick all doctors with generic reasoning
        top_picks = [{"id": idx, "reasoning": "Recommended based on specialty."} for idx in df.index]

    # 4️⃣ Build final DataFrame
    final_output = []
    for pick in top_picks:
        raw_id = str(pick['id']).upper().replace("ID", "").strip()
        doc_id = int(raw_id)  # match DataFrame index
        row = df.loc[doc_id].to_dict()
        row['Reasoning'] = pick.get('reasoning', "Recommended based on specialty.")
        final_output.append(row)

    return pd.DataFrame(final_output)


def doctor_search_pipeline(user_query, df, keyword_map, client):
    """
    Full pipeline:
    - Extract keywords
    - Filter doctors
    - Ask LLM for reasoning
    """
    keywords, specialties = extract_keywords(user_query, keyword_map)
    # print("Detected Keywords:", keywords)
    # print("Possible Specialists:", specialties)

    filtered_doctors = filter_doctors_by_specialty(df, specialties)

    results = search_doctors_private(user_query, filtered_doctors, client)
    return results


def doctor_agent(user_query, df, keyword_map, client):
    """
    Main entry for the CLI chatbot.
    Returns:
    - message (str) → what agent prints first
    - results (DataFrame) → doctor info (or None)
    """
    # 1️⃣ Run pipeline
    results = doctor_search_pipeline(user_query, df, keyword_map, client)

    # 2️⃣ Handle empty results politely
    if results.empty:
        return (
            "Sorry, I couldn’t find suitable specialists for your symptoms. "
            "Could you describe them in more detail?",
            None
        )

    # 3️⃣ Generate concise message for user
    specialties = results["Specialty"].unique()
    message = f"🤖 Based on your symptoms, you may need a {', '.join(specialties)} specialist.\nHere are the best matches I found:"
    return message, results