# supervisor_agent.py
PROMPT_TEMPLATE = """
You are a routing agent.

Classify the user query into ONE of these:
1. greeting → simple conversation (hi, hello, thanks) 
                 OR questions about the iHealth and Wellness Foundation (who you are, what the company does, its services, programs)
2. doctor_search → user mentions symptoms, health issues, or asks about specialists
3. rag → user asks questions about documents, PDFs, or knowledge base

Return ONLY one word: greeting / doctor_search / rag

User query: {input}
"""

def route_query(user_input, client):
    """
    Routes the user input to: greeting / doctor_search / rag
    client: Groq client instance (from app.py)
    """
    prompt = PROMPT_TEMPLATE.format(input=user_input)
    completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}])

    response_text = completion.choices[0].message.content.strip().lower()
    
    if response_text not in ["greeting", "doctor_search", "rag"]:
        response_text = "rag"
    return response_text