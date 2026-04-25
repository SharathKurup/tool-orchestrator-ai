# tool-orchestrator-ai

A local LLM-powered tool orchestrator that enables offline AI models to dynamically call external tools such as weather, news, datetime, location, and web search using a structured agent loop.

This project is built as an experimental system to understand and implement tool-using AI agents, with a focus on local models, privacy, and extensibility.

---

## Overview

This project implements a ReAct-style loop where the language model can:

1. Interpret user input
2. Decide when a tool is required
3. Generate a structured tool call
4. Execute one or multiple tools
5. Receive tool output
6. Produce a final response

The system works with local LLMs (via Ollama), keeping everything private except external API calls used by tools.

---

## Features

* ReAct-style agent loop (model → tool → result → model)
* Multi-tool orchestration (single + chained tool calls)
* Supported tools:

  * Weather (Tomorrow.io)
  * News (NewsAPI)
  * Date & Time (timezone-aware)
  * Location (geocoding)
  * Web Search (SearXNG - self-hosted)
* Prompt-driven tool selection
* Modular architecture for easy extension
* Debug logging support
* Designed for local LLM usage (Ollama)
* Works across both lightweight and more capable local models (e.g., Gemma 3 for lower-end setups and Gemma 4 for higher-end setups)

---

## Architecture

```
User Input
   ↓
LLM (Ollama)
   ↓
Tool Call (XML format)
   ↓
Parser
   ↓
Tool Executor
   ↓
Tool Output
   ↓
LLM (Final Response)
```

---

## Project Structure

```
tool-orchestrator-ai/
│
├── main.py
├── docker-compose.yml
├── .env
├── requirements.txt
├── README.md
│
├── src/
│   ├── constants.py
│   ├── log_config.py
│   │
│   ├── core/
│   │   ├── instructions.py
│   │   ├── parser.py
│   │   └── tool_executor.py
│   │
│   ├── tools/
│   │   ├── weather.py
│   │   ├── news.py
│   │   ├── date_time.py
│   │   ├── location.py
│   │   └── web_search.py
│   │
│   └── prompts/
│       ├── prompt.py
│       ├── default.txt
│       └── system_instruction.txt
```

---

## Setup Guide

### 1. Clone the repository

```bash
git clone https://github.com/SharathKurup/tool-orchestrator-ai.git
cd tool-orchestrator-ai
```

---

### 2. Setup Environment Variables

Create a `.env` file in the root directory:

```
# Model (keep flexible based on your system)
MODEL_NAME=gemma4:e2b

# Tomorrow.io (Weather)
TOMORROW_API_KEY=your_api_key
TOMORROW_BASE_URL=https://api.tomorrow.io/v4/timelines

# News API
NEWS_API_KEY=your_api_key
NEWS_API_BASE_URL=https://newsapi.org/v2/everything

# SearXNG (Web Search)
SEARXNG_BASE_URL=http://localhost:8080

# Debug
DEBUG=True
```

Note:

* `MODEL_NAME` is configurable to support both lightweight and powerful local models
* NewsData API is currently not in use (NIU)

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup SearXNG (Local Web Search)

SearXNG is used for privacy-friendly web search and runs locally using Docker.

#### Create `docker-compose.yml`

```yaml
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - ./searxng:/etc/searxng:rw
    environment:
      - SEARXNG_BASE_URL=http://localhost:8080/
      - INSTANCE_NAME=tool-orchestrator-ai
```

#### Run SearXNG

```bash
docker compose up
```

Run in background:

```bash
docker compose up -d
```

---

### 5. Enable JSON Output (Important)

After first run:

1. Open `searxng/settings.yml`
2. Update:

```yaml
search:
  formats:
    - html
    - json
```

3. Restart container:

```bash
docker compose restart
```

4. Open in browser:

```
http://localhost:8080
```

---

### 6. Optional: Fix Engine Errors

You may see errors like:

* Ahmia
* Torch
* Wikidata

These are non-critical. SearXNG will continue working.

To disable them, update `settings.yml`:

```yaml
engines:
  - name: wikidata
    engine: wikidata
    disabled: True

  - name: ahmia
    engine: ahmia
    disabled: True
```

---

### 7. Run the Application

```bash
python main.py
```

---

## Example Queries

```
weather in Mumbai
news about AI
what time is it in New York
coordinates of Taj Mahal
who is APJ Abdul Kalam
who was JC Bose and get news about him
```

---

## Tool Calling Format

The model generates tool calls in XML format:

```
<call:get_weather city="Mumbai"/>
```

For multiple tools:

```
<call:get_websearch query="JC Bose biography"/>
<call:get_news topic="JC Bose"/>
```

---

## APIs Used

### Weather (Tomorrow.io)

* Simple and reliable weather API
* Provides hourly forecast data
* Aggregated into daily insights in the tool

### News API

* Used to fetch latest headlines and articles
* Note: NewsData API integration exists in code but is currently not used (NIU)

### Web Search (SearXNG)

* Self-hosted meta search engine
* Privacy-friendly (no tracking)
* Aggregates results from multiple engines
* Used with scraping fallback for better summaries

Docs: [https://docs.searxng.org/](https://docs.searxng.org/)

---

## Limitations

* XML-based tool calling is fragile
* No strict schema validation
* Limited retry/error handling
* Tight coupling between tools and executor
* Web scraping may fail for some sites

---

## Roadmap

* Move from XML → JSON tool calling
* Add tool schema validation
* Introduce memory layer
* Add FastAPI backend
* Build ChatGPT-like UI (OpenWebUI style)
* Improve multi-step reasoning
* Add more tools (finance, coding, etc.)

---

## Purpose

This project is intended as a learning and experimentation platform for:

* Tool-using AI agents
* Local LLM integration
* Agent orchestration patterns
* Building blocks for AI systems

---

## License

MIT License

---

## Author

Sharath Kurup

Exploring AI systems, local LLMs, and real-world agent architectures.
