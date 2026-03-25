# app.py
import pandas as pd
import json
from dotenv import load_dotenv
import os
from groq import Groq

from utils import doctor_agent
from agents.greetings import *
from agents.rag_agent import *
from agents.supervisor_agent import route_query


# ------------------------------
# Load datasets and config
# ------------------------------

df = pd.read_excel('sample_data.xlsx')

with open("config.json", "r") as file:
    config = json.load(file)

SPECIALTY_KEYWORDS = config["SPECIALTY_KEYWORDS"]

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

print("🤖 iHealthwellness Chatbot (type 'exit' to quit)\n")

while True:
    user_input = input("User: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Agent: Goodbye! Take care and stay healthy! 🌿")
        break

    try:
        intent = route_query(user_input, client)

        if intent == "greeting":
            response = greeting_agent(user_input, client) 
            print(f"\nAgent: {response}\n")

        # ---------------- Doctor Search ----------------
        elif intent == "doctor_search":
            message, results = doctor_agent(user_input, df, SPECIALTY_KEYWORDS, client)

            if results is None or results.empty:
                print("\nAgent: Sure! Please tell me your main symptom or health concern so I can find the right specialist.\n")
            else:
                # Only take top 2 matches
                top_results = results.head(2)
                print(f"\nAgent: {message}\n")
                for idx, row in top_results.iterrows():
                    print(f"Doctor {idx+1}:")
                    print(f"Name: {row['Name']}")
                    print(f"Specialty: {row['Specialty']}")
                    print(f"Degree: {row['Degree']}")
                    print(f"Experience: {row['Experience (Years)']} years")
                    print(f"Hospital: {row['Hospital']}")
                    print(f"Address: {row['Address']}")
                    print(f"Phone: {row['Phone']}")
                    
                    # Shorten reasoning to 2–3 lines
                    reasoning = row['Reasoning'].replace("\n", " ")
                    if len(reasoning) > 200:
                        reasoning = reasoning[:197] + "..."
                    print(f"Reasoning: {reasoning}\n")
        

        elif intent == "rag":
            response = rag_agent(user_input)
            print(f"\nAgent: {response}\n")

        else:
            print("\nAgent: Sorry, I couldn’t understand that. Could you rephrase?\n")

    except Exception as e:
        print(f"Agent: ⚠️ Error: {str(e)}\n")
        
# professional, consie, comopact

# basic info + experience + reasoning

# what is healywellness
# areas 