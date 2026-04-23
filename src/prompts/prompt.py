# latter extend to handle multiple prompts
def getPrompts(prompt_name):
    match prompt_name:
        case "system":
            file_name = "system_instruction"

    file = open(f"src/prompts/{file_name}.txt", "r")
    prompt = file.read()
    file.close()
    return prompt