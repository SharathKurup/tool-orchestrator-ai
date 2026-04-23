import src.constants as constants
import requests
import pandas as pd
import json
import src.logging as logging

def get_weather(cityName):
    logging.writeLog(f"Fetching weather data for {cityName}...")
    url = f"{constants.TOMORROW_BASE_URL}?location={cityName}&timesteps=1h&apikey={constants.TOMORROW_API_KEY}"
    headers = {
        "accept-encoding": "deflate, gzip, br",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logging.writeLog("Weather data fetched successfully.")
        response = process_weather(response.json())
        prompt = f"The weather data for {cityName} is:\n{response}\n\n This weather is for one week. Please summarize this for the user in a friendly way."
        return prompt
    else:
        logging.writeLog(f"Failed to fetch weather data. Status code: {response.status_code}", "error")
        return None

def process_weather(response):
    logging.writeLog("Formatting weather data...")
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
    logging.writeLog("Weather data formatted into DataFrame.")
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
    logging.writeLog("Final weather data prepared.")    
    logging.writeLog(f"Weather data JSON: {group_df}", "info")
    json_result = json.dumps(group_df.reset_index().to_dict(orient="records"), indent=2, default=str)
    return json_result