import requests
import trafilatura
import src.constants as constants
from src.log_config import writeLog

def get_websearch(query):
    writeLog("Getting web search results...", "info")
    max_chars=3000
    search_url = f"{constants.SEARXNG}/search?q={query}&format=json"
    
    try:
        response = requests.get(search_url, timeout=5)
        data = response.json()
        if constants.DEBUG:
            writeLog(f"Web search results for {query}: {data}", "info")
        results = data.get('results', [])
        
        if not results:
            return "No results found."

        # Pick the top result
        top_result = results[0]
        target_url = top_result.get('url')
        snippet = top_result.get('content', '')

        # --- SCRAPING ATTEMPT ---
        try:
            writeLog(f"Scraping: {target_url}","info")
            downloaded = trafilatura.fetch_url(target_url)
            full_text = trafilatura.extract(downloaded) if downloaded else None
            
            if full_text and len(full_text) > 200: # Ensure we actually got useful text
                return f"Source: {target_url}\n\nContent: {full_text[:max_chars]}..."
        except Exception as e:
            writeLog(f"Scrape failed for {target_url}: {e}", "info")

        # --- FALLBACK ---
        # If scrape fails or text is too short, return the snippets from top 3 results
        writeLog(f"Scraping failed for {target_url}: {e}", "info")
        fallback_data = "Web search snippets (Scraping unavailable):\n\n"
        for res in results[:3]:
            fallback_data += f"- {res.get('title')}: {snippet}\n"
        
        return fallback_data

    except Exception as e:
        writeLog(f"Scraping failed for {query}: {e}", "info")
        return f"System Error: {str(e)}"
