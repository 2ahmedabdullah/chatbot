from utils import doctor_search_pipeline

def tools_agent(user_input, df, keyword_map, client):
    results = doctor_search_pipeline(user_input, df, keyword_map, client)

    if results.empty:
        return "I couldn't find matching doctors.", None

    return "Here are some doctors I recommend:", results