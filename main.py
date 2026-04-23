from ollama import chat
import xml.etree.ElementTree as ET
import re
import src.constants as constants
import src.tools.weather as weather_tool
import src.tools.news as news_tool
import src.tools.datetime as datetime_tool
import src.tools.location as location_tool
import src.prompts.prompt as prompts

def chat_with_model():
    system_instruction =  prompts.getPrompts("system")

    messages = [{'role': 'system', 'content': system_instruction}]

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']: break
        
        messages.append({'role': 'user', 'content': user_input})
        
        # This inner loop handles "Chain of Thought" (Model calls tool -> gets data -> calls tool again or responds)
        while True:
            response = chat(model=constants.MODEL_NAME, messages=messages, options={'temperature': 0.1})
            content = response['message']['content']
            
            # 1. Record the model's response in history
            messages.append({'role': 'assistant', 'content': content})

            # 2. Check if the model wants to use a tool
            xml_match = re.search(r'<call:(.*?)/>', content)
            
            if xml_match:
                # Dispatcher logic
                tag_name, result = handle_tool_call(xml_match.group(0)) 
                
                # Feed result back as a "System/Tool Observation"
                # We use 'user' but label it clearly so the model knows it's data
                messages.append({
                    'role': 'user', 
                    'content': f"[SYSTEM]: Tool {tag_name} output: {result}. Continue your response."
                })
                # Loop continues to 'chat' again with the new data
                continue 
            else:
                # 3. No tool call? This is the final answer for the user.
                print(f"Assistant: {content}")
                break # Exit inner loop, wait for next 'input()'

def handle_tool_call(xml_tag_string):
    """
    Parses the <call:tag /> and executes the corresponding function.
    Returns (tag_name, result_data)
    """
    # 1. Clean the tag for ElementTree
    # Removing 'call:' to avoid the "unbound prefix" error
    clean_xml = xml_tag_string.replace("call:", "")
    
    try:
        root = ET.fromstring(clean_xml)
        tag_name = root.tag  # e.g., 'get_weather'
        
        # 2. Dispatcher Logic
        if tag_name == "get_weather":
            city = root.attrib.get("city", "Unknown")
            # Call your existing function
            result = weather_tool.get_weather(city)
            return tag_name, result
        
        if tag_name == "get_news":
            query = root.attrib.get("query", "technology")
            result = news_tool.get_news(query)
            return tag_name, result
        
        if tag_name == "get_datetime":
            location = root.attrib.get("location", None)
            result = datetime_tool.get_datetime(location)
            return tag_name, result
        
        if tag_name == "get_location":
            location_name = root.attrib.get("place_name", "Unknown")
            result = location_tool.get_location(location_name)
            return tag_name, result

        else:
            return tag_name, f"Error: Tool '{tag_name}' not implemented."

    except Exception as e:
        return "error", f"XML Parsing failed: {str(e)}"

def main():
    print("Welcome to tools demo!")
    chat_with_model()

if __name__ == "__main__":
    print("Starting the AI Tools demo...")
    main()