# tool-orchestrator-ai

A local LLM-powered tool orchestrator that enables offline AI models to dynamically call external tools such as weather, news, datetime, and location using a structured agent loop.

This project is built as an experimental system to understand and implement tool-using AI agents, with a focus on local models and extensibility.

---

## Overview

This project implements a ReAct-style loop where the language model can:

1. Interpret user input  
2. Decide when a tool is required  
3. Generate a structured tool call  
4. Receive tool output  
5. Produce a final response  

The system is designed to work with local LLMs (via Ollama), keeping everything private and offline except for external API calls used by tools.

---

## Features

- ReAct-style agent loop (model → tool → result → model)
- Support for multiple tools:
  - Weather (forecast aggregation)
  - News (latest headlines)
  - Date & time (timezone-aware)
  - Location (geocoding)
- Modular tool structure
- Prompt-controlled tool selection
- Logging for debugging and traceability
- Designed for local LLM usage

---

## Architecture

```

User Input
↓
LLM (Ollama)
↓
Tool Call (XML format)
↓
Dispatcher
↓
Tool Execution
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
├── main.py                 # Entry point and agent loop
├── src/
│   ├── constants.py        # Configuration and API keys
│   ├── logging.py          # Logging utility
│   ├── tools/
│   │   ├── weather.py
│   │   ├── news.py
│   │   ├── datetime.py
│   │   └── location.py
│   └── prompts/
│       ├── prompt.py       # Prompt loader/helper
│       └── system_instruction.txt
├── .env                    # Environment variables (not committed)
└── README.md

````

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/SharathKurup/tool-orchestrator-ai.git
cd tool-orchestrator-ai
````

### 2. Create a `.env` file

```env
TOMORROW_API_KEY=your_key
TOMORROW_BASE_URL=https://api.tomorrow.io/v4/timelines

NEWS_API_KEY=your_key
NEWS_API_BASE_URL=https://newsapi.org/v2/everything
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

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
```

---

## How Tool Calling Works

The model generates tool calls in a strict XML format:

```
<call:get_weather city="Mumbai"/>
```

The orchestrator:

* Detects the tool call
* Parses parameters
* Executes the corresponding function
* Feeds the result back to the model
* The model generates the final response

---

## Limitations

* XML-based parsing is fragile
* Tool interfaces are not fully standardized
* Limited error handling
* Tight coupling between agent loop and tools
* No tool schema or validation layer yet

---

## Roadmap

* Introduce tool registry pattern
* Move from XML to structured JSON tool calls
* Standardize tool interfaces
* Add API layer (e.g., FastAPI)
* Build a web-based interface (ChatGPT-style)
* Add memory and multi-step planning
* Expand tool ecosystem

---

## Purpose

This project is intended as a learning and experimentation platform for:

* Tool-using AI agents
* Local LLM integration
* Orchestrator design patterns
* Building blocks for larger AI systems

---

## License

MIT License

---

## Author

Developed as part of an ongoing exploration into AI systems, local LLMs, and practical agent architectures.
