# # # # # # main_api.py

# # # # # """
# # # # # Main FastAPI Backend Server
# # # # # ===========================
# # # # # This script serves as the main entry point for our AI agent.

# # # # # What it does:
# # # # # 1. Creates a web server using the FastAPI framework.
# # # # # 2. Defines a primary endpoint `/invoke_agent` that accepts user queries.
# # # # # 3. Imports the compiled LangGraph agent from `graph_agent.py`.
# # # # # 4. When a request is received, it passes the user's query to the agent,
# # # # #    streams the complete response, and returns the final answer.
# # # # # 5. Includes a health check endpoint `/health` for monitoring.
# # # # # 6. Configures CORS to allow the Streamlit frontend to connect to it.
# # # # # """
# # # # # # main_api.py
# # # # # """
# # # # # FastAPI backend for the Productivity SME Agent
# # # # # -----------------------------------------------
# # # # # Endpoints:
# # # # # - POST /invoke_agent    : { "query": "<user question>" } -> runs retriever + llm and returns answer
# # # # # - GET  /health          : health check
# # # # # """

# # # # # # main_api.py
# # # # # """
# # # # # Main API Layer for Productivity SME Agent
# # # # # =========================================

# # # # # This file exposes:
# # # # # - /ask  → Run the agent and return answer
# # # # # - /health → Check if server is running

# # # # # It connects the UI (app.py) to the graph-based RAG agent in graph_agent.py.
# # # # # """

# # # # # from fastapi import FastAPI
# # # # # from pydantic import BaseModel

# # # # # from graph_agent import run_agent

# # # # # # -------------------------------------------------------------
# # # # # # FastAPI initialization
# # # # # # -------------------------------------------------------------
# # # # # app = FastAPI(
# # # # #     title="Productivity SME Agent",
# # # # #     description="RAG + Agentic Workflow with LangGraph",
# # # # #     version="1.0.0"
# # # # # )


# # # # # # -------------------------------------------------------------
# # # # # # Request/Response Schemas
# # # # # # -------------------------------------------------------------
# # # # # class QueryRequest(BaseModel):
# # # # #     question: str


# # # # # class QueryResponse(BaseModel):
# # # # #     answer: str


# # # # # # -------------------------------------------------------------
# # # # # # Routes
# # # # # # -------------------------------------------------------------
# # # # # @app.get("/health")
# # # # # def health_check():
# # # # #     return {"status": "ok", "message": "Server is running."}


# # # # # @app.post("/ask", response_model=QueryResponse)
# # # # # def ask_question(request: QueryRequest):
# # # # #     """
# # # # #     Main endpoint:
# # # # #     - Runs the LangGraph agent workflow
# # # # #     - Returns final answer
# # # # #     """
# # # # #     user_question = request.question.strip()

# # # # #     if not user_question:
# # # # #         return QueryResponse(answer="Please provide a valid question.")

# # # # #     try:
# # # # #         answer = run_agent(user_question)
# # # # #         return QueryResponse(answer=answer)
# # # # #     except Exception as e:
# # # # #         print("ERROR in /ask:", e)
# # # # #         return QueryResponse(
# # # # #             answer="An error occurred while processing your request."
# # # # #         )


# # # # # # -------------------------------------------------------------
# # # # # # Self-test when running directly
# # # # # # -------------------------------------------------------------
# # # # # if __name__ == "__main__":
# # # # #     import uvicorn
# # # # #     print("Running local API server on http://localhost:8000 ...")
# # # # #     uvicorn.run(app, host="0.0.0.0", port=8000)


# # # # # --- START OF FILE main_api.py ---

# # # # # main_api.py



# # # # # """
# # # # # Main API Layer for Productivity SME Agent
# # # # # =========================================

# # # # # This file exposes:
# # # # # - /ask  → Run the agent and return answer and reasoning steps
# # # # # - /health → Check if server is running

# # # # # It connects the UI (app.py) to the graph-based RAG agent in graph_agent.py.
# # # # # """

# # # # # from fastapi import FastAPI
# # # # # from pydantic import BaseModel
# # # # # from typing import List

# # # # # from graph_agent import run_agent_with_reasoning

# # # # # # -------------------------------------------------------------
# # # # # # FastAPI initialization
# # # # # # -------------------------------------------------------------
# # # # # app = FastAPI(
# # # # #     title="Productivity SME Agent",
# # # # #     description="RAG + Agentic Workflow with LangGraph",
# # # # #     version="1.0.0"
# # # # # )


# # # # # # -------------------------------------------------------------
# # # # # # Request/Response Schemas
# # # # # # -------------------------------------------------------------
# # # # # class QueryRequest(BaseModel):
# # # # #     question: str


# # # # # class QueryResponse(BaseModel):
# # # # #     answer: str
# # # # #     reasoning_steps: List[str]


# # # # # # -------------------------------------------------------------
# # # # # # Routes
# # # # # # -------------------------------------------------------------
# # # # # @app.get("/health")
# # # # # def health_check():
# # # # #     return {"status": "ok", "message": "Server is running."}


# # # # # @app.post("/ask", response_model=QueryResponse)
# # # # # def ask_question(request: QueryRequest):
# # # # #     """
# # # # #     Main endpoint:
# # # # #     - Runs the LangGraph agent workflow
# # # # #     - Returns final answer and reasoning steps
# # # # #     """
# # # # #     user_question = request.question.strip()

# # # # #     if not user_question:
# # # # #         return QueryResponse(
# # # # #             answer="Please provide a valid question.",
# # # # #             reasoning_steps=[]
# # # # #         )

# # # # #     try:
# # # # #         result = run_agent_with_reasoning(user_question)
# # # # #         return QueryResponse(
# # # # #             answer=result["answer"],
# # # # #             reasoning_steps=result["reasoning_steps"]
# # # # #         )
# # # # #     except Exception as e:
# # # # #         print("ERROR in /ask:", e)
# # # # #         return QueryResponse(
# # # # #             answer="An error occurred while processing your request.",
# # # # #             reasoning_steps=[f"Error: {e}"]
# # # # #         )


# # # # # # -------------------------------------------------------------
# # # # # # Self-test when running directly
# # # # # # -------------------------------------------------------------
# # # # # if __name__ == "__main__":
# # # # #     import uvicorn
# # # # #     print("Running local API server on http://localhost:8000 ...")
# # # # #     uvicorn.run(app, host="0.0.0.0", port=8000)

# # # # # main_api.py



# # # # # """
# # # # # FastAPI backend for Productivity SME Agent
# # # # # ------------------------------------------
# # # # # Endpoints:
# # # # # - POST /ask   -> { "question": "...", "mode": "fast"|"reasoning" } -> returns answer + reasoning_steps
# # # # # - GET  /health
# # # # # """

# # # # # from fastapi import FastAPI, HTTPException
# # # # # from pydantic import BaseModel
# # # # # from typing import List, Optional
# # # # # from fastapi.middleware.cors import CORSMiddleware

# # # # # from graph_agent import run_agent, run_agent_with_reasoning

# # # # # app = FastAPI(
# # # # #     title="Productivity SME Agent API",
# # # # #     description="RAG + Agentic Workflow with LangGraph",
# # # # #     version="1.0.0"
# # # # # )

# # # # # # Allow local frontends (adjust origins as needed)
# # # # # app.add_middleware(
# # # # #     CORSMiddleware,
# # # # #     allow_origins=["*"],  # change to explicit origins in production
# # # # #     allow_credentials=True,
# # # # #     allow_methods=["*"],
# # # # #     allow_headers=["*"],
# # # # # )


# # # # # class QueryRequest(BaseModel):
# # # # #     question: str
# # # # #     mode: Optional[str] = "reasoning"  # "fast" or "reasoning"


# # # # # class QueryResponse(BaseModel):
# # # # #     answer: str
# # # # #     reasoning_steps: List[str] = []


# # # # # @app.get("/health")
# # # # # def health_check():
# # # # #     return {"status": "ok", "message": "Server is running."}


# # # # # @app.post("/ask", response_model=QueryResponse)
# # # # # def ask_question(request: QueryRequest):
# # # # #     q = (request.question or "").strip()
# # # # #     mode = (request.mode or "reasoning").strip().lower()

# # # # #     if not q:
# # # # #         raise HTTPException(status_code=400, detail="Empty question provided")

# # # # #     try:
# # # # #         if mode == "fast":
# # # # #             res = run_agent(q)
# # # # #         else:
# # # # #             res = run_agent_with_reasoning(q)

# # # # #         # Agent historically returns a simple string — handle both shapes
# # # # #         if isinstance(res, str):
# # # # #             return QueryResponse(answer=res, reasoning_steps=[])
# # # # #         elif isinstance(res, dict):
# # # # #             # try to extract fields safely
# # # # #             ans = res.get("answer") or res.get("final_answer") or str(res)
# # # # #             steps = res.get("reasoning_steps") or res.get("plan_steps") or []
# # # # #             # ensure steps is a list of strings
# # # # #             if not isinstance(steps, list):
# # # # #                 steps = [str(steps)]
# # # # #             return QueryResponse(answer=ans, reasoning_steps=steps)
# # # # #         else:
# # # # #             return QueryResponse(answer=str(res), reasoning_steps=[])
# # # # #     except Exception as e:
# # # # #         # log server-side
# # # # #         print("ERROR /ask:", e)
# # # # #         raise HTTPException(status_code=500, detail="Error processing the request.")


# # # # # if __name__ == "__main__":
# # # # #     import uvicorn
# # # # #     print("Starting API on http://0.0.0.0:8000")
# # # # #     uvicorn.run(app, host="0.0.0.0", port=8000)



# # # # # # main_api.py
# # # # # """
# # # # # FastAPI backend for Productivity SME Agent
# # # # # ------------------------------------------
# # # # # Endpoints:
# # # # # - POST /ask   -> { "question": "...", "mode": "fast"|"reasoning" } -> returns answer + reasoning_steps
# # # # # - GET  /health
# # # # # """

# # # # # from fastapi import FastAPI, HTTPException
# # # # # from pydantic import BaseModel
# # # # # from typing import List, Optional
# # # # # from fastapi.middleware.cors import CORSMiddleware

# # # # # from graph_agent import run_agent, run_agent_with_reasoning

# # # # # app = FastAPI(
# # # # #     title="Productivity SME Agent API",
# # # # #     description="RAG + Agentic Workflow with LangGraph",
# # # # #     version="1.0.0"
# # # # # )

# # # # # # Allow local frontends (adjust origins as needed)
# # # # # app.add_middleware(
# # # # #     CORSMiddleware,
# # # # #     allow_origins=["*"],  # change to explicit origins in production
# # # # #     allow_credentials=True,
# # # # #     allow_methods=["*"],
# # # # #     allow_headers=["*"],
# # # # # )


# # # # # class QueryRequest(BaseModel):
# # # # #     question: str
# # # # #     mode: Optional[str] = "reasoning"  # "fast" or "reasoning"


# # # # # class QueryResponse(BaseModel):
# # # # #     answer: str
# # # # #     reasoning_steps: List[str] = []


# # # # # @app.get("/health")
# # # # # def health_check():
# # # # #     return {"status": "ok", "message": "Server is running."}


# # # # # @app.post("/ask", response_model=QueryResponse)
# # # # # def ask_question(request: QueryRequest):
# # # # #     q = (request.question or "").strip()
# # # # #     mode = (request.mode or "reasoning").strip().lower()

# # # # #     if not q:
# # # # #         raise HTTPException(status_code=400, detail="Empty question provided")

# # # # #     try:
# # # # #         if mode == "fast":
# # # # #             res = run_agent(q)
# # # # #         else:
# # # # #             res = run_agent_with_reasoning(q)

# # # # #         # Agent historically returns a simple string — handle both shapes
# # # # #         if isinstance(res, str):
# # # # #             return QueryResponse(answer=res, reasoning_steps=[])
# # # # #         elif isinstance(res, dict):
# # # # #             # try to extract fields safely
# # # # #             ans = res.get("answer") or res.get("final_answer") or str(res)
# # # # #             steps = res.get("reasoning_steps") or res.get("plan_steps") or []
# # # # #             # ensure steps is a list of strings
# # # # #             if not isinstance(steps, list):
# # # # #                 steps = [str(steps)]
# # # # #             return QueryResponse(answer=ans, reasoning_steps=steps)
# # # # #         else:
# # # # #             return QueryResponse(answer=str(res), reasoning_steps=[])
# # # # #     except Exception as e:
# # # # #         # log server-side
# # # # #         print("ERROR /ask:", e)
# # # # #         raise HTTPException(status_code=500, detail="Error processing the request.")


# # # # # if __name__ == "__main__":
# # # # #     import uvicorn
# # # # #     print("Starting API on http://0.0.0.0:8000")
# # # # #     uvicorn.run(app, host="0.0.0.0", port=8000)


# # # # # main_api.py
# # # # """
# # # # FastAPI backend for Productivity SME Agent
# # # # ------------------------------------------
# # # # Endpoints:
# # # # - POST /ask   -> { "question": "...", "mode": "fast"|"reasoning" } -> returns answer + reasoning_steps
# # # # - GET  /health
# # # # """

# # # # from fastapi import FastAPI, HTTPException
# # # # from pydantic import BaseModel
# # # # from typing import List, Optional
# # # # from fastapi.middleware.cors import CORSMiddleware

# # # # # Import the two primary execution functions from the agent
# # # # from graph_agent import run_agent, run_agent_with_reasoning

# # # # app = FastAPI(
# # # #     title="Productivity SME Agent API",
# # # #     description="RAG + Agentic Workflow with LangGraph",
# # # #     version="2.0.0" # Version bump for new architecture
# # # # )

# # # # # Allow cross-origin requests for local development
# # # # app.add_middleware(
# # # #     CORSMiddleware,
# # # #     allow_origins=["*"],
# # # #     allow_credentials=True,
# # # #     allow_methods=["*"],
# # # #     allow_headers=["*"],
# # # # )


# # # # class QueryRequest(BaseModel):
# # # #     question: str
# # # #     mode: Optional[str] = "reasoning"  # Default to the more powerful "reasoning" mode


# # # # class QueryResponse(BaseModel):
# # # #     answer: str
# # # #     reasoning_steps: List[str] = []


# # # # @app.get("/health", summary="Health Check")
# # # # def health_check():
# # # #     """Check if the API server is running."""
# # # #     return {"status": "ok", "message": "Server is running."}


# # # # @app.post("/ask", response_model=QueryResponse, summary="Ask the Agent a Question")
# # # # def ask_question(request: QueryRequest):
# # # #     """
# # # #     Main endpoint to interact with the agent.
# # # #     - **question**: The user's question.
# # # #     - **mode**: 'reasoning' (default) for the full Think->Action loop, or 'fast' for a direct answer.
# # # #     """
# # # #     question = (request.question or "").strip()
# # # #     mode = (request.mode or "reasoning").strip().lower()

# # # #     if not question:
# # # #         raise HTTPException(status_code=400, detail="Question cannot be empty.")

# # # #     try:
# # # #         if mode == "fast":
# # # #             print(f"[API] Running in FAST mode for question: '{question[:50]}...'")
# # # #             result = run_agent(question)
# # # #         else:
# # # #             print(f"[API] Running in REASONING mode for question: '{question[:50]}...'")
# # # #             result = run_agent_with_reasoning(question)

# # # #         # The new agent always returns a dictionary
# # # #         if not isinstance(result, dict):
# # # #              # This is a fallback in case something goes wrong
# # # #             raise ValueError("Agent did not return the expected dictionary format.")
            
# # # #         return QueryResponse(
# # # #             answer=result.get("answer", "No answer was generated."),
# # # #             reasoning_steps=result.get("reasoning_steps", [])
# # # #         )
        
# # # #     except Exception as e:
# # # #         print(f"ERROR in /ask endpoint: {e}")
# # # #         # In a production scenario, you might log the full traceback here
# # # #         raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")


# # # # if __name__ == "__main__":
# # # #     import uvicorn
# # # #     print("Starting API server on http://0.0.0.0:8000")
# # # #     uvicorn.run(app, host="0.0.0.0", port=8000)




# # # # main_api.py
# # # """
# # # FastAPI backend for Productivity SME Agent
# # # ------------------------------------------
# # # This version provides real-time streaming of agent reasoning.

# # # Endpoints:
# # # - POST /ask   -> (Streams Server-Sent Events with reasoning steps and final answer)
# # # - GET  /status -> Checks if email is configured.
# # # - GET  /health -> Basic health check.
# # # """

# # # import os
# # # import json
# # # import asyncio
# # # from fastapi import FastAPI, HTTPException
# # # from pydantic import BaseModel
# # # from typing import List, Optional
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from fastapi.responses import StreamingResponse
# # # from dotenv import load_dotenv

# # # load_dotenv()

# # # from graph_agent import REASONING_GRAPH # Import the compiled graph directly

# # # app = FastAPI(
# # #     title="Productivity SME Agent API",
# # #     description="RAG + Agentic Workflow with LangGraph",
# # #     version="3.0.0" # Version bump for streaming architecture
# # # )

# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # # --- Pydantic Models ---
# # # class QueryRequest(BaseModel):
# # #     question: str
# # #     mode: Optional[str] = "reasoning"

# # # class StatusResponse(BaseModel):
# # #     email_configured: bool

# # # # --- API Endpoints ---
# # # @app.get("/health", summary="Health Check")
# # # def health_check():
# # #     return {"status": "ok"}

# # # @app.get("/status", response_model=StatusResponse, summary="Check Backend Config Status")
# # # def get_status():
# # #     email_user = os.getenv("EMAIL_USER")
# # #     email_password = os.getenv("EMAIL_PASSWORD")
# # #     is_configured = bool(email_user and email_password)
# # #     return StatusResponse(email_configured=is_configured)

# # # # --- START OF NEW STREAMING ENDPOINT ---
# # # @app.post("/ask", summary="Ask the Agent (Streaming)")
# # # async def ask_question_streaming(request: QueryRequest):
# # #     """
# # #     Main endpoint using Server-Sent Events (SSE) to stream the agent's process.
# # #     - Streams each reasoning step as it occurs.
# # #     - Streams the final answer at the end.
# # #     """
# # #     question = (request.question or "").strip()
# # #     if not question:
# # #         raise HTTPException(status_code=400, detail="Question cannot be empty.")

# # #     async def stream_events():
# # #         """The generator function that yields SSE events."""
# # #         try:
# # #             # Initial state for the graph
# # #             initial_state = {"user_input": question, "reasoning_steps": [], "tool_history": []}
            
# # #             # Use the .stream() method of the compiled LangGraph
# # #             last_steps_count = 0
# # #             final_answer = "No final answer was generated by the agent."

# # #             async for event in REASONING_GRAPH.astream(initial_state):
# # #                 # The event contains the full state at that point in the graph
# # #                 # We look for the latest update
# # #                 if "planner" in event:
# # #                     state = event["planner"]
# # #                 elif "tool" in event:
# # #                     state = event["tool"]
# # #                 elif "actor" in event:
# # #                     state = event["actor"]
# # #                 else: # Skip intermediate events without node data
# # #                     continue

# # #                 # Check for new reasoning steps
# # #                 current_steps = state.get("reasoning_steps", [])
# # #                 if len(current_steps) > last_steps_count:
# # #                     new_step = current_steps[-1]
# # #                     last_steps_count = len(current_steps)
                    
# # #                     # Yield a 'step' event
# # #                     step_payload = {"type": "step", "data": new_step}
# # #                     yield f"data: {json.dumps(step_payload)}\n\n"
# # #                     await asyncio.sleep(0.05) # Small delay to ensure message is sent

# # #                 if state.get("final_answer"):
# # #                     final_answer = state["final_answer"]

# # #             # After the loop, send the final answer
# # #             answer_payload = {"type": "final_answer", "data": final_answer}
# # #             yield f"data: {json.dumps(answer_payload)}\n\n"

# # #         except Exception as e:
# # #             print(f"ERROR during agent execution stream: {e}")
# # #             error_payload = {"type": "error", "data": f"An internal error occurred: {e}"}
# # #             yield f"data: {json.dumps(error_payload)}\n\n"

# # #     return StreamingResponse(stream_events(), media_type="text/event-stream")
# # # # --- END OF NEW STREAMING ENDPOINT ---


# # # if __name__ == "__main__":
# # #     import uvicorn
# # #     print("Starting Streaming API server on http://0.0.0.0:8000")
# # #     uvicorn.run(app, host="0.0.0.0", port=8000)


# # # main_api.py (with chat history)

# # import os
# # import json
# # import asyncio
# # from fastapi import FastAPI, HTTPException
# # from pydantic import BaseModel
# # from typing import List, Optional, Dict, Any
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import StreamingResponse
# # from dotenv import load_dotenv

# # load_dotenv()

# # from graph_agent import REASONING_GRAPH

# # app = FastAPI(
# #     title="Productivity SME Agent API",
# #     description="RAG + Agentic Workflow with LangGraph",
# #     version="3.1.0" # Version bump for chat history
# # )

# # app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# # # --- START OF CHANGE ---

# # class QueryRequest(BaseModel):
# #     question: str
# #     mode: Optional[str] = "reasoning"
# #     chat_history: Optional[List[Dict[str, Any]]] = [] # Accept chat history

# # # --- END OF CHANGE ---

# # class StatusResponse(BaseModel):
# #     email_configured: bool

# # @app.get("/health", summary="Health Check")
# # def health_check():
# #     return {"status": "ok"}

# # @app.get("/status", response_model=StatusResponse, summary="Check Backend Config Status")
# # def get_status():
# #     email_user = os.getenv("EMAIL_USER")
# #     email_password = os.getenv("EMAIL_PASSWORD")
# #     return StatusResponse(email_configured=bool(email_user and email_password))

# # @app.post("/ask", summary="Ask the Agent (Streaming)")
# # async def ask_question_streaming(request: QueryRequest):
# #     question = (request.question or "").strip()
# #     if not question:
# #         raise HTTPException(status_code=400, detail="Question cannot be empty.")

# #     async def stream_events():
# #         try:
# #             # --- START OF CHANGE ---
# #             # Pass the chat history from the request into the agent's initial state
# #             initial_state = {
# #                 "user_input": question,
# #                 "chat_history": request.chat_history or [], # Ensure it's a list
# #                 "reasoning_steps": [],
# #                 "tool_history": []
# #             }
# #             # --- END OF CHANGE ---

# #             last_steps_count = 0
# #             final_answer = "No final answer was generated by the agent."

# #             async for event in REASONING_GRAPH.astream(initial_state):
# #                 state_update = next(iter(event.values()))
# #                 if state_update:
# #                     current_steps = state_update.get("reasoning_steps", [])
# #                     if len(current_steps) > last_steps_count:
# #                         new_step = current_steps[-1]
# #                         last_steps_count = len(current_steps)
# #                         step_payload = {"type": "step", "data": new_step}
# #                         yield f"data: {json.dumps(step_payload)}\n\n"
# #                         await asyncio.sleep(0.05)
# #                     if state_update.get("final_answer"):
# #                         final_answer = state_update["final_answer"]
            
# #             answer_payload = {"type": "final_answer", "data": final_answer}
# #             yield f"data: {json.dumps(answer_payload)}\n\n"
# #         except Exception as e:
# #             print(f"ERROR during agent execution stream: {e}")
# #             error_payload = {"type": "error", "data": f"An internal error occurred: {e}"}
# #             yield f"data: {json.dumps(error_payload)}\n\n"

# #     return StreamingResponse(stream_events(), media_type="text/event-stream")

# # if __name__ == "__main__":
# #     import uvicorn
# #     print("Starting Streaming API server with Chat History on http://0.0.0.0:8000")
# #     uvicorn.run(app, host="0.0.0.0", port=8000)


# # main_api.py (with file download endpoint)

# import os
# import json
# import asyncio
# import re
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional, Dict, Any
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse, FileResponse # Import FileResponse
# from pathlib import Path # Import Path
# from dotenv import load_dotenv

# load_dotenv()

# from graph_agent import REASONING_GRAPH

# # --- START OF NEW SECTION ---
# # Define the reports directory so the API knows where to find files
# REPORTS_DIR = Path("reports")
# # --- END OF NEW SECTION ---

# app = FastAPI(
#     title="Productivity SME Agent API",
#     description="RAG + Agentic Workflow with LangGraph",
#     version="3.2.0" # Version bump for download feature
# )

# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# class QueryRequest(BaseModel):
#     question: str
#     mode: Optional[str] = "reasoning"
#     chat_history: Optional[List[Dict[str, Any]]] = []

# class StatusResponse(BaseModel):
#     email_configured: bool

# @app.get("/health", summary="Health Check")
# def health_check():
#     return {"status": "ok"}

# @app.get("/status", response_model=StatusResponse, summary="Check Backend Config Status")
# def get_status():
#     email_user = os.getenv("EMAIL_USER")
#     email_password = os.getenv("EMAIL_PASSWORD")
#     return StatusResponse(email_configured=bool(email_user and email_password))

# # --- START OF NEW SECTION: DOWNLOAD ENDPOINT ---
# @app.get("/download/{filename}", summary="Download a Generated Report")
# async def download_report(filename: str):
#     """
#     Allows the frontend to download a file from the 'reports' directory.
#     """
#     # Security check: prevent directory traversal attacks (e.g., ../../some_other_file)
#     if ".." in filename or "/" in filename:
#         raise HTTPException(status_code=400, detail="Invalid filename.")

#     file_path = REPORTS_DIR / filename
#     if not file_path.is_file():
#         raise HTTPException(status_code=404, detail="File not found.")
    
#     return FileResponse(path=file_path, media_type='application/octet-stream', filename=filename)
# # --- END OF NEW SECTION ---


# @app.post("/ask", summary="Ask the Agent (Streaming)")
# async def ask_question_streaming(request: QueryRequest):
#     question = (request.question or "").strip()
#     if not question:
#         raise HTTPException(status_code=400, detail="Question cannot be empty.")

#     async def stream_events():
#         try:
#             initial_state = {
#                 "user_input": question,
#                 "chat_history": request.chat_history or [],
#                 "reasoning_steps": [],
#                 "tool_history": []
#             }
#             last_steps_count = 0
#             final_answer = "No final answer was generated."

#             async for event in REASONING_GRAPH.astream(initial_state):
#                 state_update = next(iter(event.values()))
#                 if state_update:
#                     current_steps = state_update.get("reasoning_steps", [])
#                     if len(current_steps) > last_steps_count:
#                         new_step = current_steps[-1]
#                         last_steps_count = len(current_steps)
#                         step_payload = {"type": "step", "data": new_step}
#                         yield f"data: {json.dumps(step_payload)}\n\n"
#                         await asyncio.sleep(0.05)
#                     if state_update.get("final_answer"):
#                         final_answer = state_update["final_answer"]
            
#             answer_payload = {"type": "final_answer", "data": final_answer}
#             yield f"data: {json.dumps(answer_payload)}\n\n"
#         except Exception as e:
#             print(f"ERROR during agent execution stream: {e}")
#             error_payload = {"type": "error", "data": f"An internal error occurred: {e}"}
#             yield f"data: {json.dumps(error_payload)}\n\n"

#     return StreamingResponse(stream_events(), media_type="text/event-stream")

# if __name__ == "__main__":
#     import uvicorn
#     print("Starting Streaming API server with Download endpoint on http://0.0.0.0:8000")
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# main_api.py (with enhanced /evaluate endpoint)

import os
import json
import asyncio
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from graph_agent import REASONING_GRAPH
from retriever import Retriever
from llm_client import llm_judge

REPORTS_DIR = Path("reports")
retriever = Retriever()

app = FastAPI(
    title="Productivity SME Agent API",
    description="RAG + Agentic Workflow with LangGraph",
    version="3.4.0" # Version bump for dashboard integration
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class QueryRequest(BaseModel):
    question: str
    chat_history: Optional[List[Dict[str, Any]]] = []

class EvaluationRequest(BaseModel):
    question: str
    answer: str

# --- NEW: Richer response for the dashboard ---
class DetailedEvaluationResponse(BaseModel):
    question: str
    answer: str
    contexts: List[str]
    metrics: Dict[str, Any]

def extract_float(x, default=0.0):
    try:
        if isinstance(x, (int, float)): return float(x)
        m = re.search(r"(\d+(?:\.\d+)?)", str(x)); return float(m.group(1)) if m else default
    except: return default

def unified_evaluate(contexts: List[str], question: str, answer: str):
    ctx = "\n\n".join(contexts)
    prompt = f"""You are an expert evaluator. Judge the ANSWER based on the QUESTION and CONTEXT. Return a strict JSON with scores (0.0-1.0).
{{ "faithfulness": float, "completeness": float, "quality": float, "hallucinations": ["list of strings"] }}
CONTEXT: ---
{ctx}
---
QUESTION: {question}
ANSWER: {answer}
Return ONLY the JSON.
"""
    raw = llm_judge(prompt)
    try: data = json.loads(raw)
    except: m = re.search(r"(\{.*\})", raw, re.DOTALL); data = json.loads(m.group(1)) if m else {}
    return {
        "faithfulness": extract_float(data.get("faithfulness")),
        "completeness": extract_float(data.get("completeness")),
        "quality": extract_float(data.get("quality")),
        "hallucinations": data.get("hallucinations", [])
    }

@app.get("/health")
def health_check(): return {"status": "ok"}

@app.get("/status")
def get_status():
    email_user, email_pass = os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD")
    return {"email_configured": bool(email_user and email_pass)}

@app.get("/download/{filename}")
async def download_report(filename: str):
    if ".." in filename or "/" in filename: raise HTTPException(400, "Invalid filename.")
    file_path = REPORTS_DIR / filename
    if not file_path.is_file(): raise HTTPException(404, "File not found.")
    return FileResponse(path=file_path, media_type='application/octet-stream', filename=filename)

@app.post("/evaluate", response_model=DetailedEvaluationResponse)
async def evaluate_response(request: EvaluationRequest):
    try:
        docs = retriever.fetch_relevant_chunks(request.question)
        contexts = [d.get("text", "") for d in docs]
        metrics = unified_evaluate(contexts, request.question, request.answer)
        return DetailedEvaluationResponse(
            question=request.question,
            answer=request.answer,
            contexts=contexts,
            metrics=metrics
        )
    except Exception as e:
        raise HTTPException(500, f"Evaluation error: {e}")

@app.post("/ask")
async def ask_question_streaming(request: QueryRequest):
    # This endpoint is unchanged
    question = (request.question or "").strip()
    if not question: raise HTTPException(400, "Question cannot be empty.")
    async def stream_events():
        try:
            initial_state = {"user_input": question, "chat_history": request.chat_history or [], "reasoning_steps": [], "tool_history": []}
            final_answer = "No final answer was generated."
            last_steps_count = 0
            async for event in REASONING_GRAPH.astream(initial_state):
                state_update = next(iter(event.values()))
                if state_update:
                    current_steps = state_update.get("reasoning_steps", [])
                    if len(current_steps) > last_steps_count:
                        yield f"data: {json.dumps({'type': 'step', 'data': current_steps[-1]})}\n\n"
                        last_steps_count = len(current_steps)
                        await asyncio.sleep(0.05)
                    if state_update.get("final_answer"):
                        final_answer = state_update["final_answer"]
            yield f"data: {json.dumps({'type': 'final_answer', 'data': final_answer})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'data': str(e)})}\n\n"
    return StreamingResponse(stream_events(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)