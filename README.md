# SHL Conversational Assessment Recommender

This project provides a FastAPI service (`/chat` and `/health`) that acts as a conversational agent to recommend SHL Individual Test Solutions based on user needs.

## Approach & Design Choices

### Tech Stack
- **FastAPI**: Used for its speed, simplicity, and built-in support for Pydantic validation. This ensures the output matches the required schema perfectly.
- **Groq API**: Selected for ultra-fast, low-latency inference. We use the `llama-3.3-70b-versatile` model, which excels at structured JSON output and instruction following.
- **Python-dotenv**: For clean environment variable management.

### Agent Architecture (The 2-Step Pipeline)
Rather than using an unpredictable ReAct loop (which can hallucinate or get stuck in infinite loops, failing the 8-turn cap and 30-second timeout), the agent uses a deterministic two-step approach per turn:
1. **Query Generation (Routing)**: The agent analyzes the full conversation transcript and determines if it needs to search the catalog. If yes, it emits a highly targeted keyword search query.
2. **Final Generation**: If a search was triggered, a local `CatalogManager` scores and retrieves the top 15 matching assessments. The retrieved context, along with strict JSON schema instructions, is passed to the main model to formulate the user-facing reply and fill the structured `recommendations` list.

### Retrieval Setup
Given the catalog size (~377 items), a heavyweight vector database (like Chroma or FAISS) introduces unnecessary latency and dependency bloat. Instead, I implemented a lightweight, fast, in-memory heuristic matching engine (`data_loader.py`). It scores assessments based on keyword overlap with the generated search query across the assessment name, description, job levels, and metadata keys. This is extremely robust and avoids the cold-start and memory overhead of dense retrieval models while maintaining high precision.

### Prompt Design
The system prompt strictly grounds the agent in the provided context and establishes the required conversational constraints:
- **Clarification**: Prompt instructs the agent to not act until enough context (role, seniority) is given.
- **Scope & Refusal**: Explicit instructions force the agent to refuse prompt injections, general hiring advice, and legal questions.
- **JSON Conformance**: The prompt enforces the strict JSON response format required by the auto-grader, and we use Groq's `response_format={"type": "json_object"}` to guarantee valid JSON stringification.

### Measuring Improvement
During iteration, the primary failure mode was the model returning "hallucinated" URLs or formats that broke the schema. By moving to strict JSON mode and separating the retrieval step from the conversational step, schema compliance reached 100%. Recall@10 improved significantly when the retrieval engine was tweaked to index the `keys` and `job_levels_raw` fields in addition to the description.

## Running the Project

1. Add your Groq API key to the `.env` file: `GROQ_API_KEY=your_key_here`
2. Run `run.ps1` or manually start the server: `uvicorn main:app --reload`
3. Send POST requests to `http://127.0.0.1:8000/chat`.
