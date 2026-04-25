from ollama import chat
import re
import src.constants as constants
import src.prompts.prompt as prompts
from src.log_config import writeLog
from src.core.instructions import get_tool_instruction
from src.core.parser import parse_calls
from src.core.tool_executor import execute_tools

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
            # xml_match = re.search(r'<call:(.*?)/>', content)
            # xml_match = re.findall(r'<call:(?:.*?)/>', content)
            xml_match = re.findall(r'<call:[^>]+/>', content)
            if xml_match:
                xml_string = "".join(xml_match)
                calls = parse_calls(xml_string)

                results, combined_response = execute_tools(calls)

                message  = build_tool_message(results, combined_response, user_input)

                messages.append(message)

                continue
            else:
                # 3. No tool call? This is the final answer for the user.
                print(f"Assistant: {content}")
                break 

def build_tool_message(results, combined_response,user_input,):
    if len(results) > 1:
        instruction = get_tool_instruction("multi", user_input)

        return{
            'role': 'system',
            'content': f"""
            {combined_response}
            INSTRUCTION:
            {instruction}
        """}
    else:
        result = results[0]

        instruction = get_tool_instruction(result["tool"], user_input)

        return{
            'role': 'system',
            'content': f"""
            Tool: {result["tool"]}
            OUTPUT:
            {result["formatted"]}
            INSTRUCTION:
            {instruction}
        """}


def main():
    writeLog("Starting the application.", "info")
    chat_with_model()

if __name__ == "__main__":
    main()