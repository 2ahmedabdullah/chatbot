IHEALTHWELLNESS_CONTEXT = """
The iHealth and Wellness Foundation is a 501(c)(3) nonprofit dedicated to supporting patients with complex conditions like Neurofibromatosis, Alzheimer’s, diabetes, and cancer. 
It aims to improve patient care through digital health navigation, community building, and advocacy, offering resources to empower patients and their caregivers. 
Key Aspects of the iHealth and Wellness Foundation
Mission: To create a future where people with complex conditions feel seen, supported, and empowered.
Support & Services: Developing digital health navigation platforms to connect patients with care, reducing the burden of managing complex diseases.
Focus Areas: Improving care for Neurofibromatosis (NF), Alzheimer’s, Diabetes, and Cancer.
Engagement: The foundation actively seeks donations and volunteers to support patient advocacy and enhance healthcare access.
"""

AGENT_CONTEXT = """
I am the iHealthwellness Virtual Assistant. My role is to help users:
- Understand which specialists they may need based on their symptoms.
- Provide general guidance on health queries.
- Offer information about the iHealth and Wellness Foundation, its programs, and services.
- Help navigate resources such as doctor listings, educational material, and RAG-based document answers.

I do not replace medical advice from a qualified physician. My goal is to provide guidance, support, and information in a friendly and empathetic manner.
"""

def greeting_agent(user_input, client):
    prompt = f"""
    Context: {IHEALTHWELLNESS_CONTEXT}
    Agent role: {AGENT_CONTEXT}
    User said: "{user_input}"

    Respond politely and concisely in 1-2 sentences.
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content.strip()