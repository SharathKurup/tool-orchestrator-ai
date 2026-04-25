import src.tools.weather as weather_tool
import src.tools.news as news_tool
import src.tools.date_time as datetime_tool
import src.tools.location as location_tool
import src.tools.web_search as websearch_tool

TOOL_REGISTRY = {
    "get_weather": weather_tool.get_weather,
    "get_news": news_tool.get_news,
    "get_datetime": datetime_tool.get_datetime,
    "get_location": location_tool.get_location,
    "get_websearch": websearch_tool.get_websearch
}

def execute_tools(calls):
    tool_outputs = []
    results = []

    for call in calls:
        tag_name = call["tool"]
        attrs = call["args"]

        result = handle_tool_call(tag_name, **attrs)
        formatted_result = format_tool_output(tag_name, result)

        results.append({
                        "tool": tag_name,
                        "raw": result,
                        "formatted": formatted_result
                    })

        tool_outputs.append(f"""Tool: {tag_name}
                        OUTPUT:
                        {formatted_result}""")

                # 🔥 combine AFTER loop
    combined_response = "\n---\n".join(tool_outputs)
    return results,combined_response# Exit inner loop, wait for next 'input()'

def handle_tool_call(tag_name, **attrs):
    try:
        func = TOOL_REGISTRY[tag_name]
        return func(**attrs)
    except Exception as e:
        return f"error: {str(e)}"
    
def format_tool_output(tool_name, result):
    if tool_name == "get_news":
        formatted = ""
        for item in result[:5]:
            formatted += f"- {item.get('title')}\n"
        return formatted

    if tool_name == "get_weather":
        return result  # already string

    if tool_name == "get_datetime":
        return f"Current datetime: {result}"

    if tool_name == "get_location":
        lat, lon = result
        return f"Latitude: {lat}, Longitude: {lon}"

    if tool_name == "get_websearch":
        return result

    return str(result)
