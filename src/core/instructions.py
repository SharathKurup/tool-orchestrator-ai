def get_tool_instruction(tool_name, user_query):
    if tool_name == "get_weather":
        return "Summarize the weather in a friendly way. Highlight temperature trends, rain, and overall comfort. Explain the current and future predictions in a human friendly way."

    if tool_name == "get_news":
        return "Summarize the news concisely and display the link/url in a human friendly way."

    if tool_name == "get_location":
        return "Provide the coordinates clearly (latitude and longitude) in a human friendly way."

    if tool_name == "get_datetime":
        if "time" in user_query.lower() and "date" not in user_query.lower():
            return "Respond with only the current time in a human friendly way."
        
        if "date" in user_query.lower() and "time" not in user_query.lower():
            return "Respond with only today's date in a human friendly way."
        
        return "Respond with both date and time in a human friendly way."

    if tool_name == "get_websearch":  
        # Check if user asked for a specific type of information
        query_lower = user_query.lower()
        
        if "who is" in query_lower or "who was" in query_lower:
            return "Provide a concise biographical summary focusing on key facts: who they are/were, why they're known, and relevant dates."
        
        if "what is" in query_lower or "define" in query_lower:
            return "Provide a clear definition or explanation in simple terms. Include examples if helpful."
        
        if "where is" in query_lower:
            return "Provide the location information clearly. Include country, region, or address as appropriate."
        
        if "history of" in query_lower or "when did" in query_lower:
            return "Summarize the historical information chronologically. Focus on key dates and events."
        
        # Default web search instruction
        return "Extract and summarize the most relevant information from the search results. Be concise and factual. Do not add information not present in the search results."

    if tool_name == "multi":
        return f"Combine the information into a clear, structured response in a very understanable and human friendly way for the query {user_query}."
    
    return "Summarize the data in a human friendly way."
