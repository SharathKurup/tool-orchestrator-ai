import src.constants as constants
import requests
import pandas as pd
import json
from src.log_config import writeLog

def get_weather(city):
    writeLog(f"Fetching weather data for {city}...","info")
    url = f"{constants.TOMORROW_BASE_URL}?location={city}&timesteps=1h&apikey={constants.TOMORROW_API_KEY}"
    headers = {
        "accept-encoding": "deflate, gzip, br",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        writeLog("Weather data fetched successfully.","info")
        response = process_weather(response.json())
        # prompt = f"The weather data for {city} is:\n{response}\n\n This weather is for one week. Please summarize this for the user in a friendly way."
        return response
    else:
        writeLog(f"Failed to fetch weather data. Status code: {response.status_code}", "error")
        return f"Failed to fetch weather data. Status code: {response.status_code}"

def process_weather(response):
    writeLog("Formatting weather data...","info")
    data = response["timelines"]["hourly"]
    rows = []
    for item in data:
        row = {
            "time": item["time"],
            **item["values"]
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df["time"] = pd.to_datetime(df["time"])
    df["time"] = df["time"].dt.tz_convert("Asia/Kolkata")
    df["date"] = df["time"].dt.date
    df["hour"] = df["time"].dt.hour
    writeLog("Weather data formatted into DataFrame.","info")
    group_df =df.groupby("date").agg({
        "temperature": ["min", "max", "mean"],
        "rainAccumulation": "sum",
        "humidity": "mean"
    })

    #flatten
    group_df.columns = ["_".join(col) for col in group_df.columns]

    #rename columns
    group_df.rename(columns={
        "rainAccumulation_sum": "total_rain",
        "humidity_mean": "avg_humidity"
    }, inplace=True)
    # print(json.dumps(group_df.reset_index().to_dict(orient="records"), indent=2, default=str))
    writeLog("Final weather data prepared.","info")
    writeLog(f"Weather data JSON: {group_df}", "info")
    json_result = json.dumps(group_df.reset_index().to_dict(orient="records"), indent=2, default=str)
    return json_result