# latter extend to handle multiple prompts
def getPrompts(prompt_name):
    match prompt_name:
        case "system":
            file_name = "system_instruction"
        case _:
            file_name = "default"

    with (open(f"src/prompts/{file_name}.txt", "r")) as file:
        prompt = file.read()
        file.close()
        return prompt