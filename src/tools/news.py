import src.constants as constants
import requests
import src.log_config as logging

#NIU 
def get_news_data(topic): 
    logging.writeLog(f"Fetching news for topic: {topic}", "info")
    url =  f"{constants.NEWS_DATA_BASE_URL}?"
    url += f"apikey={constants.NEWS_DATA_API_KEY}"
    url += f"&q={topic}"
    url += f"&country=in"
    url += f"&category=technology,breaking"
    url += f"&timezone=asia/kolkata"
    url += f"&removeduplicate=1"
    url += f"&size=6" # for size 5, give 6
    
    logging.writeLog(f"Constructed URL for news data API: {url}", "info")
    response = requests.get(url)
    data = response.json()
    logging.writeLog(f"Received news data for topic: {topic}", "info")
    logging.writeLog(f"News data JSON: {data}", "info")
    return process_news_data(data,"newsdata")

def process_news_data(response,source):
    results = []
    match source:
        case "newsapi":
            articles = response.get("articles", [])
            for article in articles:
                result = {
                    "source": article.get("source", {}).get("name"),
                    "author": article.get("author"),
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url")
                }
                results.append(result)
            return results

        case "newsdata":
            data = response.get("results", [])
            for item in data:
                result = {
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "url": item.get("link"),
                    "author": item.get("creator"),
                    "source": item.get("source_name")
                }
                results.append(result)
            return results
        case _:
            return results

def get_news(topic):
    logging.writeLog(f"Fetching news for topic: {topic}", "info")
    url = f"{constants.NEWS_API_BASE_URL}?q={topic}&apiKey={constants.NEWS_API_KEY}&pageSize=5"
    logging.writeLog(f"Constructed URL for news API: {url}", "info")
    response = requests.get(url)
    data = response.json()
    logging.writeLog(f"Received news data for topic: {topic}", "info")
    news_data = process_news_data(data,"newsapi")    
    logging.writeLog(f"News api data: {news_data}", "info")
    return news_data