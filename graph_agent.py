# # # # # graph_agent.py (Full Corrected Code with Looping)

# # # # import json
# # # # import re
# # # # from typing import TypedDict, Optional, Dict, Any, List

# # # # from langgraph.graph import StateGraph, END
# # # # from langchain_core.runnables import RunnableLambda

# # # # from retriever import Retriever
# # # # from tools import TOOLS, TOOLS_BY_NAME
# # # # from llm_client import get_llm_response

# # # # # =========================================================
# # # # # Helper to clean LLM's JSON output
# # # # # =========================================================
# # # # def extract_json(text: str) -> Optional[Dict]:
# # # #     if not text: return None
# # # #     text = text.replace("```json", "").replace("```", "").strip()
# # # #     try: return json.loads(text)
# # # #     except json.JSONDecodeError:
# # # #         match = re.search(r"\{.*\}", text, re.DOTALL)
# # # #         if match:
# # # #             try: return json.loads(match.group(0))
# # # #             except json.JSONDecodeError: return None
# # # #     return None

# # # # # =========================================================
# # # # # Agent State Model
# # # # # =========================================================
# # # # class AgentState(TypedDict, total=False):
# # # #     user_input: str
# # # #     retrieved_context: Optional[str]
# # # #     plan: Optional[Dict[str, Any]]
# # # #     generated_content: Optional[str]
# # # #     final_answer: Optional[str]
# # # #     reasoning_steps: List[str]
# # # #     # --- NEW: Add a history of tool calls to the state ---
# # # #     tool_history: List[Dict[str, Any]]

# # # # # =========================================================
# # # # # Nodes for the Graph
# # # # # =========================================================
# # # # def retrieve_node(state: AgentState) -> AgentState:
# # # #     q = state["user_input"]
# # # #     r = Retriever()
# # # #     reasoning_steps = state.get("reasoning_steps", [])
# # # #     try:
# # # #         docs = r.fetch_relevant_chunks(q)
# # # #         ctx = "\n\n".join(d.get("text", "") for d in docs)
# # # #         reasoning_steps.append(f"OBSERVATION (retrieve): Found {len(docs)} relevant document chunks.")
# # # #     except Exception as e:
# # # #         ctx = ""
# # # #         reasoning_steps.append(f"OBSERVATION (retrieve): Failed with error - {e}")
# # # #     return {**state, "retrieved_context": ctx, "reasoning_steps": reasoning_steps}

# # # # def planner_node(state: AgentState) -> AgentState:
# # # #     q = state["user_input"]
# # # #     ctx = state.get("retrieved_context", "")
# # # #     reasoning_steps = state.get("reasoning_steps", [])
# # # #     # --- NEW: Get the tool history to inform the planner ---
# # # #     tool_history = state.get("tool_history", [])
    
# # # #     tool_descriptions = []
# # # #     for tool in TOOLS:
# # # #         try:
# # # #             schema = tool.args_schema.model_json_schema()
# # # #             desc = f"- **{tool.name}**: {schema.get('description', '')}\n  - Arguments:\n"
# # # #             properties = schema.get('properties', {})
# # # #             if not properties: desc += "    - (No arguments required)\n"
# # # #             else:
# # # #                 for prop, details in properties.items():
# # # #                     desc += f"    - `{prop}` ({details.get('type')}): {details.get('description')}\n"
# # # #             tool_descriptions.append(desc)
# # # #         except Exception as e:
# # # #             print(f"Warning: Could not generate schema for tool '{tool.name}'. Error: {e}")
# # # #     tool_list_detailed = "\n".join(tool_descriptions)
    
# # # #     prompt = f"""
# # # # You are the PLANNER. Your job is to decide the next logical step to fulfill the user's request.
# # # # Analyze the user's question, the retrieved context, and the history of tools already executed.

# # # # - If the user's request is not yet complete, choose the next tool to run.
# # # # - If all steps are complete, you MUST choose the "answer" action to finish.

# # # # USER QUESTION: "{q}"

# # # # RETRIEVED CONTEXT:
# # # # ---
# # # # {ctx[:2000]}...
# # # # ---

# # # # TOOL EXECUTION HISTORY (what you have already done):
# # # # ---
# # # # {json.dumps(tool_history, indent=2)}
# # # # ---

# # # # AVAILABLE TOOLS:
# # # # ---
# # # # {tool_list_detailed}
# # # # ---

# # # # Return ONLY valid JSON. If the task is finished, set "action": "answer".
# # # # {{
# # # #   "action": "tools" | "answer",
# # # #   "tool_name": "<name of the tool if action is 'tools'>",
# # # #   "tool_input": {{ "argument": "value" }},
# # # #   "reasoning": "<Your reasoning for this next step>"
# # # # }}
# # # # """
# # # #     raw = get_llm_response(prompt, role="planner")
# # # #     plan = extract_json(raw)
# # # #     if not plan:
# # # #         plan = {"action": "answer", "reasoning": "Planner failed, defaulting to answer."}
    
# # # #     reasoning_steps.append(f"THINK (Planner): {plan.get('reasoning', 'No reasoning.')}\nAction: {plan.get('action')}")
# # # #     return {**state, "plan": plan, "reasoning_steps": reasoning_steps}

# # # # def generate_content_node(state: AgentState) -> AgentState:
# # # #     """Generates the full, high-quality text content for the report."""
# # # #     q = state["user_input"]
# # # #     ctx = state.get("retrieved_context", "")
# # # #     plan = state.get("plan", {})
# # # #     # Extract the report title from the plan to focus the LLM
# # # #     report_title = plan.get("tool_input", {}).get("title", "Report")
    
# # # #     reasoning_steps = state.get("reasoning_steps", [])
# # # #     reasoning_steps.append(f"ACTION (Content Generator): Writing the content for the report titled '{report_title}'.")

# # # #     prompt = f"""
# # # # You are a world-class Productivity Expert.
# # # # Your task is to write a comprehensive, well-structured, and helpful article that will serve as the content for a report.

# # # # The report title is: "{report_title}"
# # # # The user's original request was: "{q}"

# # # # Use the following context to inform your writing:
# # # # ---
# # # # {ctx}
# # # # ---

# # # # Generate ONLY the body content for the report. Do not add extra titles or email drafts.
# # # # """
# # # #     content = get_llm_response(prompt, role="actor")
# # # #     return {**state, "generated_content": content, "reasoning_steps": reasoning_steps}


# # # # def tool_node(state: AgentState) -> AgentState:
# # # #     plan = state.get("plan", {})
# # # #     reasoning_steps = state.get("reasoning_steps", [])
# # # #     # --- NEW: Initialize tool history if it doesn't exist ---
# # # #     tool_history = state.get("tool_history", [])
    
# # # #     tool_name = (plan.get("tool_name") or "").lower()
# # # #     tool_input = plan.get("tool_input", {})
# # # #     tool = TOOLS_BY_NAME.get(tool_name)

# # # #     if not tool:
# # # #         result = {"status": "error", "error": f"Tool '{tool_name}' not found."}
# # # #     else:
# # # #         try:
# # # #             # Inject generated content into the create_report tool
# # # #             if tool_name == "create_docx_report":
# # # #                 tool_input['content'] = state.get("generated_content", "Error.")
            
# # # #             # --- NEW: Inject the generated report path into the send_email tool ---
# # # #             if tool_name == "send_email":
# # # #                 # Find the path from the previous tool call in history
# # # #                 for past_tool in reversed(tool_history):
# # # #                     if past_tool.get("tool_name") == "create_docx_report" and past_tool.get("result", {}).get("status") == "ok":
# # # #                         tool_input['attachment_path'] = past_tool["result"]["path"]
# # # #                         break
            
# # # #             reasoning_steps.append(f"ACTION: Executing tool '{tool.name}' with input: {tool_input}")
# # # #             result = tool.func(tool_input)
# # # #         except Exception as e:
# # # #             result = {"status": "error", "error": f"Tool execution failed: {e}"}

# # # #     reasoning_steps.append(f"OBSERVATION (tool): {result}")
# # # #     # --- NEW: Append the result to the history for the next planning step ---
# # # #     tool_history.append({"tool_name": tool_name, "tool_input": tool_input, "result": result})
# # # #     return {**state, "reasoning_steps": reasoning_steps, "tool_history": tool_history}

# # # # def actor_node(state: AgentState) -> AgentState:
# # # #     reasoning_steps = state.get("reasoning_steps", [])
# # # #     tool_history = state.get("tool_history", [])
    
# # # #     # Generate a final summary of actions taken
# # # #     summary = "Based on your request, I have completed the following actions:\n"
# # # #     for tool_call in tool_history:
# # # #         if tool_call.get("result", {}).get("status") == "ok":
# # # #             if tool_call["tool_name"] == "create_docx_report":
# # # #                 summary += f"- Successfully created the report at: `{tool_call['result']['path']}`\n"
# # # #             if tool_call["tool_name"] == "send_email":
# # # #                 summary += f"- Successfully sent the email to: `{tool_call['tool_input']['recipient']}`\n"

# # # #     reasoning_steps.append("ACTION (Actor): Generating final summary for the user.")
# # # #     return {**state, "final_answer": summary, "reasoning_steps": reasoning_steps}

# # # # def should_continue(state: AgentState) -> str:
# # # #     action = state.get("plan", {}).get("action")
# # # #     if action == "answer":
# # # #         return "actor" # The planner has decided the task is complete
    
# # # #     tool_name = state.get("plan", {}).get("tool_name", "")
# # # #     if tool_name == "create_docx_report":
# # # #         return "generate_content"
    
# # # #     return "tool"

# # # # # =========================================================
# # # # # Build Graphs
# # # # # =========================================================
# # # # def build_reasoning_graph():
# # # #     G = StateGraph(AgentState)
# # # #     G.add_node("retrieve", RunnableLambda(retrieve_node))
# # # #     G.add_node("planner", RunnableLambda(planner_node))
# # # #     G.add_node("generate_content", RunnableLambda(generate_content_node))
# # # #     G.add_node("tool", RunnableLambda(tool_node))
# # # #     G.add_node("actor", RunnableLambda(actor_node))
    
# # # #     G.set_entry_point("retrieve")
# # # #     G.add_edge("retrieve", "planner")
    
# # # #     G.add_conditional_edges(
# # # #         "planner",
# # # #         should_continue,
# # # #         {
# # # #             "generate_content": "generate_content",
# # # #             "tool": "tool",
# # # #             "actor": "actor"
# # # #         }
# # # #     )
    
# # # #     G.add_edge("generate_content", "tool")
    
# # # #     # --- THIS IS THE KEY CHANGE: THE LOOP ---
# # # #     # After a tool is used, go back to the planner to decide the next step
# # # #     G.add_edge("tool", "planner")
    
# # # #     G.add_edge("actor", END)
    
# # # #     return G.compile()

# # # # REASONING_GRAPH = build_reasoning_graph()

# # # # # =========================================================
# # # # # Public API and Fast Graph (No changes needed below this line)
# # # # # =========================================================
# # # # def build_fast_graph():
# # # #     G = StateGraph(AgentState)
# # # #     G.add_node("retrieve", RunnableLambda(retrieve_node))
# # # #     G.add_node("actor", RunnableLambda(generate_content_node)) # Use generate_content for a better fast answer
# # # #     G.set_entry_point("retrieve")
# # # #     G.add_edge("retrieve", "actor")
# # # #     G.add_edge("actor", END)
# # # #     return G.compile()

# # # # FAST_GRAPH = build_fast_graph()

# # # # def run_agent(prompt: str) -> Dict:
# # # #     initial_state = {"user_input": prompt, "reasoning_steps": ["Starting in FAST mode."]}
# # # #     out = FAST_GRAPH.invoke(initial_state)
# # # #     # The 'fast' graph's final answer is now in 'generated_content'
# # # #     return {"answer": out.get("generated_content", ""), "reasoning_steps": out.get("reasoning_steps", [])}

# # # # def run_agent_with_reasoning(prompt: str) -> Dict:
# # # #     initial_state = {"user_input": prompt, "reasoning_steps": ["Starting in REASONING mode."], "tool_history": []}
# # # #     out = REASONING_GRAPH.invoke(initial_state)
# # # #     return {"answer": out.get("final_answer", ""), "reasoning_steps": out.get("reasoning_steps", [])}


# # # # graph_agent.py (Verified to show both live reasoning AND a final conversational answer)

# # # import json
# # # import re
# # # from typing import TypedDict, Optional, Dict, Any, List

# # # from langgraph.graph import StateGraph, END
# # # from langchain_core.runnables import RunnableLambda

# # # from retriever import Retriever
# # # from tools import TOOLS, TOOLS_BY_NAME
# # # from llm_client import get_llm_response

# # # # =========================================================
# # # # Helper and State (Unchanged)
# # # # =========================================================
# # # def extract_json(text: str) -> Optional[Dict]:
# # #     if not text: return None
# # #     text = text.replace("```json", "").replace("```", "").strip()
# # #     try: return json.loads(text)
# # #     except json.JSONDecodeError:
# # #         match = re.search(r"\{.*\}", text, re.DOTALL)
# # #         if match:
# # #             try: return json.loads(match.group(0))
# # #             except json.JSONDecodeError: return None
# # #     return None

# # # class AgentState(TypedDict, total=False):
# # #     user_input: str
# # #     retrieved_context: Optional[str]
# # #     plan: Optional[Dict[str, Any]]
# # #     generated_content: Optional[str]
# # #     final_answer: Optional[str]
# # #     reasoning_steps: List[str] # <-- THIS IS THE LIST FOR LIVE REASONING
# # #     tool_history: List[Dict[str, Any]]

# # # # =========================================================
# # # # Nodes for the Graph
# # # # =========================================================
# # # def retrieve_node(state: AgentState) -> AgentState:
# # #     # This node adds to `reasoning_steps` and the API streams it
# # #     q = state["user_input"]
# # #     r = Retriever()
# # #     reasoning_steps = state.get("reasoning_steps", [])
# # #     try:
# # #         docs = r.fetch_relevant_chunks(q)
# # #         ctx = "\n\n".join(d.get("text", "") for d in docs)
# # #         reasoning_steps.append(f"OBSERVATION (retrieve): Found {len(docs)} relevant document chunks.")
# # #     except Exception as e:
# # #         ctx = ""
# # #         reasoning_steps.append(f"OBSERVATION (retrieve): Failed with error - {e}")
# # #     return {**state, "retrieved_context": ctx, "reasoning_steps": reasoning_steps}

# # # def planner_node(state: AgentState) -> AgentState:
# # #     # This node adds to `reasoning_steps` and the API streams it
# # #     q = state["user_input"]
# # #     ctx = state.get("retrieved_context", "")
# # #     reasoning_steps = state.get("reasoning_steps", [])
# # #     tool_history = state.get("tool_history", [])
    
# # #     tool_descriptions = []
# # #     for tool in TOOLS:
# # #         try:
# # #             schema = tool.args_schema.model_json_schema()
# # #             desc = f"- **{tool.name}**: {schema.get('description', '')}\n  - Arguments:\n"
# # #             properties = schema.get('properties', {})
# # #             if not properties: desc += "    - (No arguments required)\n"
# # #             else:
# # #                 for prop, details in properties.items():
# # #                     desc += f"    - `{prop}` ({details.get('type')}): {details.get('description')}\n"
# # #             tool_descriptions.append(desc)
# # #         except Exception as e:
# # #             print(f"Warning: Could not generate schema for tool '{tool.name}'. Error: {e}")
# # #     tool_list_detailed = "\n".join(tool_descriptions)
    
# # #     prompt = f"""
# # # You are the PLANNER. Your job is to decide the next logical step. Analyze the user's question, retrieved context, and tool history. If all steps are complete, you MUST choose the "answer" action.

# # # USER QUESTION: "{q}"
# # # RETRIEVED CONTEXT:
# # # ---
# # # {ctx[:2000]}...
# # # ---
# # # TOOL HISTORY:
# # # ---
# # # {json.dumps(tool_history, indent=2)}
# # # ---
# # # AVAILABLE TOOLS:
# # # ---
# # # {tool_list_detailed}
# # # ---
# # # Return ONLY valid JSON.
# # # {{
# # #   "action": "tools" | "answer",
# # #   "tool_name": "<name of tool>",
# # #   "tool_input": {{ "argument": "value" }},
# # #   "reasoning": "<Your reasoning>"
# # # }}
# # # """
# # #     raw = get_llm_response(prompt, role="planner")
# # #     plan = extract_json(raw)
# # #     if not plan:
# # #         plan = {"action": "answer", "reasoning": "Planner failed, defaulting to answer."}
    
# # #     reasoning_steps.append(f"THINK (Planner): {plan.get('reasoning', 'No reasoning.')}\nAction: {plan.get('action')}")
# # #     return {**state, "plan": plan, "reasoning_steps": reasoning_steps}

# # # def generate_content_node(state: AgentState) -> AgentState:
# # #     # This node adds to `reasoning_steps` and the API streams it
# # #     q = state["user_input"]
# # #     ctx = state.get("retrieved_context", "")
# # #     plan = state.get("plan", {})
# # #     report_title = plan.get("tool_input", {}).get("title", "Report")
    
# # #     reasoning_steps = state.get("reasoning_steps", [])
# # #     reasoning_steps.append(f"ACTION (Content Generator): Writing the content for the report titled '{report_title}'.")

# # #     prompt = f"You are a Productivity Expert. Write a comprehensive article for a report titled '{report_title}' based on the user's request '{q}' and the following context:\n\n{ctx}\n\nGenerate ONLY the body content."
# # #     content = get_llm_response(prompt, role="actor")
# # #     return {**state, "generated_content": content, "reasoning_steps": reasoning_steps}

# # # def tool_node(state: AgentState) -> AgentState:
# # #     # This node adds to `reasoning_steps` and the API streams it
# # #     plan = state.get("plan", {})
# # #     reasoning_steps = state.get("reasoning_steps", [])
# # #     tool_history = state.get("tool_history", [])
    
# # #     tool_name = (plan.get("tool_name") or "").lower()
# # #     tool_input = plan.get("tool_input", {})
# # #     tool = TOOLS_BY_NAME.get(tool_name)

# # #     if not tool:
# # #         result = {"status": "error", "error": f"Tool '{tool_name}' not found."}
# # #     else:
# # #         try:
# # #             if tool_name == "create_docx_report":
# # #                 tool_input['content'] = state.get("generated_content", "Error: No content was generated.")
# # #             if tool_name == "send_email":
# # #                 for past_tool in reversed(tool_history):
# # #                     if past_tool.get("tool_name") == "create_docx_report" and past_tool.get("result", {}).get("status") == "ok":
# # #                         tool_input['attachment_path'] = past_tool["result"]["path"]
# # #                         break
            
# # #             reasoning_steps.append(f"ACTION: Executing tool '{tool.name}' with input: {tool_input}")
# # #             result = tool.func(tool_input)
# # #         except Exception as e:
# # #             result = {"status": "error", "error": f"Tool execution failed: {e}"}

# # #     reasoning_steps.append(f"OBSERVATION (tool): {result}")
# # #     tool_history.append({"tool_name": tool_name, "tool_input": tool_input, "result": result})
# # #     return {**state, "reasoning_steps": reasoning_steps, "tool_history": tool_history}

# # # # --- THIS IS THE KEY NODE FOR YOUR FINAL OUTPUT ---
# # # def actor_node(state: AgentState) -> AgentState:
# # #     """
# # #     This node runs LAST. It does two things:
# # #     1. It adds one final step to the `reasoning_steps` list, which you will see live.
# # #     2. It generates the `final_answer` variable, which is the polished text sent at the end.
# # #     """
# # #     reasoning_steps = state.get("reasoning_steps", [])
# # #     tool_history = state.get("tool_history", [])
# # #     user_question = state["user_input"]
# # #     context = state.get("retrieved_context", "No context was retrieved.")

# # #     # 1. This is the final reasoning step you will see in the expander
# # #     reasoning_steps.append("ACTION (Actor): Generating final conversational answer for the user.")

# # #     # 2. This is the prompt that creates the final, polished answer for the main chat bubble
# # #     prompt = f"""
# # # You are a helpful and knowledgeable Productivity Expert. Your goal is to provide a final, comprehensive response to the user.

# # # Your response must have two parts:
# # # 1.  **A Direct Answer:** First, provide a direct and helpful answer to the user's original question. Use the provided context to formulate this answer. Be conversational and clear.
# # # 2.  **A Summary of Actions:** After the answer, provide a brief summary of the actions you have successfully completed (like creating files). Do not mention actions that failed.

# # # USER'S ORIGINAL QUESTION:
# # # "{user_question}"

# # # CONTEXT FOR YOUR ANSWER:
# # # ---
# # # {context}
# # # ---

# # # ACTIONS YOU HAVE COMPLETED:
# # # ---
# # # {json.dumps(tool_history, indent=2)}
# # # ---

# # # Please generate the final response now. Combine the answer and the action summary into a single, well-formatted Markdown response.
# # # """
    
# # #     final_answer_content = get_llm_response(prompt, role="actor")
    
# # #     return {**state, "final_answer": final_answer_content, "reasoning_steps": reasoning_steps}

# # # def should_continue(state: AgentState) -> str:
# # #     action = state.get("plan", {}).get("action")
# # #     if action == "answer":
# # #         return "actor"
# # #     tool_name = state.get("plan", {}).get("tool_name", "")
# # #     if tool_name == "create_docx_report":
# # #         return "generate_content"
# # #     return "tool"

# # # # =========================================================
# # # # Build and Export Graph (Unchanged)
# # # # =========================================================
# # # def build_reasoning_graph():
# # #     G = StateGraph(AgentState)
# # #     G.add_node("retrieve", RunnableLambda(retrieve_node))
# # #     G.add_node("planner", RunnableLambda(planner_node))
# # #     G.add_node("generate_content", RunnableLambda(generate_content_node))
# # #     G.add_node("tool", RunnableLambda(tool_node))
# # #     G.add_node("actor", RunnableLambda(actor_node))
# # #     G.set_entry_point("retrieve")
# # #     G.add_edge("retrieve", "planner")
# # #     G.add_conditional_edges("planner", should_continue, {"generate_content": "generate_content", "tool": "tool", "actor": "actor"})
# # #     G.add_edge("generate_content", "tool")
# # #     G.add_edge("tool", "planner")
# # #     G.add_edge("actor", END)
# # #     return G.compile()

# # # REASONING_GRAPH = build_reasoning_graph()

# # # # Unused functions for non-streaming mode
# # # def run_agent_with_reasoning(prompt: str) -> Dict:
# # #     initial_state = {"user_input": prompt, "reasoning_steps": [], "tool_history": []}
# # #     out = REASONING_GRAPH.invoke(initial_state)
# # #     return {"answer": out.get("final_answer", ""), "reasoning_steps": out.get("reasoning_steps", [])}





# # # graph_agent.py (with intelligent query router)

# # import json
# # import re
# # from typing import TypedDict, Optional, Dict, Any, List

# # from langgraph.graph import StateGraph, END
# # from langchain_core.runnables import RunnableLambda

# # from retriever import Retriever
# # from tools import TOOLS, TOOLS_BY_NAME
# # from llm_client import get_llm_response

# # # (Helper functions extract_json and _format_chat_history are unchanged)
# # def extract_json(text: str) -> Optional[Dict]:
# #     if not text: return None
# #     text = text.replace("```json", "").replace("```", "").strip()
# #     try: return json.loads(text)
# #     except json.JSONDecodeError:
# #         match = re.search(r"\{.*\}", text, re.DOTALL)
# #         if match:
# #             try: return json.loads(match.group(0))
# #             except json.JSONDecodeError: return None
# #     return None

# # def _format_chat_history(history: List[Dict[str, Any]]) -> str:
# #     if not history: return "No previous conversation history."
# #     formatted = [f"{'User' if m.get('role') == 'user' else 'Assistant'}: {m.get('content', '')}" for m in history]
# #     return "\n".join(formatted)

# # class AgentState(TypedDict, total=False):
# #     user_input: str
# #     chat_history: List[Dict[str, Any]]
# #     retrieved_context: Optional[str]
# #     plan: Optional[Dict[str, Any]]
# #     generated_content: Optional[str]
# #     final_answer: Optional[str]
# #     reasoning_steps: List[str]
# #     tool_history: List[Dict[str, Any]]
# #     route: str # <-- NEW: To store the decision from the router

# # # --- START OF NEW SECTION: ROUTER NODE ---

# # def route_query_node(state: AgentState) -> AgentState:
# #     """
# #     The new first step. It classifies the user's query to decide if retrieval is necessary.
# #     """
# #     q = state["user_input"]
# #     chat_history_formatted = _format_chat_history(state.get("chat_history", []))
# #     reasoning_steps = state.get("reasoning_steps", [])

# #     prompt = f"""You are an expert query router. Your task is to analyze the user's latest input and the preceding chat history to determine the best next step.

# # CHAT HISTORY:
# # ---
# # {chat_history_formatted}
# # ---

# # LATEST USER INPUT: "{q}"

# # Based on the input, choose one of the following routes:

# # 1.  `retrieve`: If the user is asking a new question that requires information from a knowledge base (e.g., "What is X?", "How do I do Y?").
# # 2.  `direct_answer`: If the user's input is a simple greeting ("hi", "thanks"), a statement of fact, or a follow-up question that can be answered using ONLY the chat history above (e.g., "Which technique did you just mention?", "Can you explain point 2 again?").

# # Return ONLY a JSON object with your decision. Example:
# # {{"route": "retrieve"}}
# # """
    
# #     raw = get_llm_response(prompt, role="planner") # Use the cheaper/faster model for routing
# #     try:
# #         decision = extract_json(raw)
# #         route = decision.get("route", "retrieve") # Default to retrieve if something goes wrong
# #     except:
# #         route = "retrieve"

# #     reasoning_steps.append(f"THINK (Router): Decided that the best route for this query is '{route}'.")
    
# #     return {**state, "route": route, "reasoning_steps": reasoning_steps}

# # def should_retrieve(state: AgentState) -> str:
# #     """Conditional edge that directs the graph based on the router's decision."""
# #     if state.get("route") == "retrieve":
# #         return "retrieve"
# #     else:
# #         # If we don't need to retrieve, we can go straight to the planner.
# #         # The planner will see an empty context and rely on the chat history.
# #         return "planner"

# # # --- END OF NEW SECTION ---


# # def retrieve_node(state: AgentState) -> AgentState:
# #     # This node now only runs if the router decides it's necessary.
# #     q = state["user_input"]
# #     r = Retriever()
# #     reasoning_steps = state.get("reasoning_steps", [])
# #     try:
# #         docs = r.fetch_relevant_chunks(q)
# #         ctx = "\n\n".join(d.get("text", "") for d in docs)
# #         reasoning_steps.append(f"ACTION (Retrieve): Found {len(docs)} relevant document chunks.")
# #     except Exception as e:
# #         ctx = ""
# #         reasoning_steps.append(f"ACTION (Retrieve): Failed with error - {e}")
# #     # Initialize context as empty if not set, for the direct_answer route
# #     return {**state, "retrieved_context": ctx or "", "reasoning_steps": reasoning_steps}

# # def planner_node(state: AgentState) -> AgentState:
# #     # (This node's code is unchanged, but its behavior is now smarter because
# #     # it sometimes receives an empty context and must rely on chat history)
# #     q = state["user_input"]
# #     ctx = state.get("retrieved_context", "")
# #     reasoning_steps = state.get("reasoning_steps", [])
# #     tool_history = state.get("tool_history", [])
# #     chat_history_formatted = _format_chat_history(state.get("chat_history", []))
# #     tool_descriptions = "\n".join([f"- **{t.name}**: {t.args_schema.model_json_schema().get('description', '')}" for t in TOOLS])
    
# #     prompt = f"""You are the PLANNER. Your job is to decide the next step. Analyze the chat history and the user's latest question.

# # CHAT HISTORY:
# # ---
# # {chat_history_formatted}
# # ---
# # LATEST USER QUESTION: "{q}"
# # RETRIEVED CONTEXT (if any):
# # ---
# # {ctx[:2000]}...
# # ---
# # TOOL HISTORY (for this turn):
# # ---
# # {json.dumps(tool_history, indent=2)}
# # ---
# # AVAILABLE TOOLS: {tool_descriptions}

# # Return ONLY valid JSON for the next step. If the task is finished, set "action": "answer".
# # {{
# #   "action": "tools" | "answer",
# #   "tool_name": "<name>",
# #   "tool_input": {{ "arg": "val" }},
# #   "reasoning": "<your reasoning>"
# # }}
# # """
# #     raw = get_llm_response(prompt, role="planner")
# #     plan = extract_json(raw)
# #     if not plan:
# #         plan = {"action": "answer", "reasoning": "Planner failed, defaulting to answer."}
    
# #     reasoning_steps.append(f"THINK (Planner): {plan.get('reasoning', 'No reasoning.')}\nAction: {plan.get('action')}")
# #     return {**state, "plan": plan, "reasoning_steps": reasoning_steps}


# # # (generate_content_node, tool_node, and actor_node are unchanged)
# # def generate_content_node(state: AgentState) -> AgentState:
# #     q = state["user_input"]
# #     ctx = state.get("retrieved_context", "")
# #     plan = state.get("plan", {})
# #     report_title = plan.get("tool_input", {}).get("title", "Report")
# #     reasoning_steps = state.get("reasoning_steps", [])
# #     reasoning_steps.append(f"ACTION (Content Generator): Writing content for report '{report_title}'.")
# #     prompt = f"You are a Productivity Expert. Write a comprehensive article for a report titled '{report_title}' based on the user's request '{q}' and the following context:\n\n{ctx}\n\nGenerate ONLY the body content."
# #     content = get_llm_response(prompt, role="actor")
# #     return {**state, "generated_content": content, "reasoning_steps": reasoning_steps}

# # def tool_node(state: AgentState) -> AgentState:
# #     plan = state.get("plan", {})
# #     reasoning_steps = state.get("reasoning_steps", [])
# #     tool_history = state.get("tool_history", [])
# #     tool_name = (plan.get("tool_name") or "").lower()
# #     tool_input = plan.get("tool_input", {})
# #     tool = TOOLS_BY_NAME.get(tool_name)
# #     if not tool:
# #         result = {"status": "error", "error": f"Tool '{tool_name}' not found."}
# #     else:
# #         try:
# #             if tool_name == "create_docx_report":
# #                 tool_input['content'] = state.get("generated_content", "Error: No content generated.")
# #             if tool_name == "send_email":
# #                 for past_tool in reversed(tool_history):
# #                     if past_tool.get("tool_name") == "create_docx_report" and past_tool.get("result", {}).get("status") == "ok":
# #                         tool_input['attachment_path'] = past_tool["result"]["path"]
# #                         break
# #             reasoning_steps.append(f"ACTION: Executing tool '{tool.name}' with input: {tool_input}")
# #             result = tool.func(tool_input)
# #         except Exception as e:
# #             result = {"status": "error", "error": f"Tool execution failed: {e}"}
# #     reasoning_steps.append(f"OBSERVATION (tool): {result}")
# #     tool_history.append({"tool_name": tool_name, "tool_input": tool_input, "result": result})
# #     return {**state, "reasoning_steps": reasoning_steps, "tool_history": tool_history}

# # def actor_node(state: AgentState) -> AgentState:
# #     reasoning_steps = state.get("reasoning_steps", [])
# #     tool_history = state.get("tool_history", [])
# #     user_question = state["user_input"]
# #     context = state.get("retrieved_context", "No context retrieved.")
# #     chat_history_formatted = _format_chat_history(state.get("chat_history", []))
# #     reasoning_steps.append("ACTION (Actor): Generating final conversational answer.")
# #     prompt = f"""You are a helpful Productivity Expert. Review the CHAT HISTORY and LATEST USER QUESTION, then provide a final, comprehensive response.
# # Your response must have two parts:
# # 1.  **A Direct Answer:** Answer the user's latest question. Use the chat history and any retrieved context.
# # 2.  **A Summary of Actions:** After the answer, summarize any actions you successfully completed *in this turn*.

# # CHAT HISTORY:
# # ---
# # {chat_history_formatted}
# # ---
# # LATEST USER QUESTION: "{user_question}"
# # CONTEXT (for the latest question):
# # ---
# # {context}
# # ---
# # ACTIONS COMPLETED (this turn):
# # ---
# # {json.dumps(tool_history, indent=2)}
# # ---
# # Generate the final Markdown response now.
# # """
# #     final_answer_content = get_llm_response(prompt, role="actor")
# #     return {**state, "final_answer": final_answer_content, "reasoning_steps": reasoning_steps}


# # def should_continue(state: AgentState) -> str:
# #     action = state.get("plan", {}).get("action")
# #     if action == "answer":
# #         return "actor"
# #     tool_name = state.get("plan", {}).get("tool_name", "")
# #     if tool_name == "create_docx_report":
# #         return "generate_content"
# #     return "tool"


# # # --- START OF MODIFIED SECTION: GRAPH DEFINITION ---

# # def build_reasoning_graph():
# #     G = StateGraph(AgentState)
    
# #     # Add all the nodes
# #     G.add_node("router", RunnableLambda(route_query_node))
# #     G.add_node("retrieve", RunnableLambda(retrieve_node))
# #     G.add_node("planner", RunnableLambda(planner_node))
# #     G.add_node("generate_content", RunnableLambda(generate_content_node))
# #     G.add_node("tool", RunnableLambda(tool_node))
# #     G.add_node("actor", RunnableLambda(actor_node))
    
# #     # Set the new entry point
# #     G.set_entry_point("router")
    
# #     # Add the new conditional edge from the router
# #     G.add_conditional_edges(
# #         "router",
# #         should_retrieve,
# #         {
# #             "retrieve": "retrieve",
# #             "planner": "planner" # Skip retrieval and go to planner
# #         }
# #     )
    
# #     # The rest of the graph flow
# #     G.add_edge("retrieve", "planner")
# #     G.add_conditional_edges("planner", should_continue, {"generate_content": "generate_content", "tool": "tool", "actor": "actor"})
# #     G.add_edge("generate_content", "tool")
# #     G.add_edge("tool", "planner")
# #     G.add_edge("actor", END)
    
# #     return G.compile()

# # # --- END OF MODIFIED SECTION ---

# # REASONING_GRAPH = build_reasoning_graph()


# # graph_agent.py (with a stricter planner prompt)

# import json
# import re
# from typing import TypedDict, Optional, Dict, Any, List

# from langgraph.graph import StateGraph, END
# from langchain_core.runnables import RunnableLambda

# from retriever import Retriever
# from tools import TOOLS, TOOLS_BY_NAME
# from llm_client import get_llm_response

# # (Helper functions and AgentState are unchanged)
# def extract_json(text: str) -> Optional[Dict]:
#     if not text: return None
#     text = text.replace("```json", "").replace("```", "").strip()
#     try: return json.loads(text)
#     except json.JSONDecodeError:
#         match = re.search(r"\{.*\}", text, re.DOTALL)
#         if match:
#             try: return json.loads(match.group(0))
#             except json.JSONDecodeError: return None
#     return None

# def _format_chat_history(history: List[Dict[str, Any]]) -> str:
#     if not history: return "No previous conversation history."
#     formatted = [f"{'User' if m.get('role') == 'user' else 'Assistant'}: {m.get('content', '')}" for m in history]
#     return "\n".join(formatted)

# class AgentState(TypedDict, total=False):
#     user_input: str
#     chat_history: List[Dict[str, Any]]
#     retrieved_context: Optional[str]
#     plan: Optional[Dict[str, Any]]
#     generated_content: Optional[str]
#     final_answer: Optional[str]
#     reasoning_steps: List[str]
#     tool_history: List[Dict[str, Any]]
#     route: str

# # (Router and retrieve nodes are unchanged)
# def route_query_node(state: AgentState) -> AgentState:
#     q = state["user_input"]
#     chat_history_formatted = _format_chat_history(state.get("chat_history", []))
#     reasoning_steps = state.get("reasoning_steps", [])
#     prompt = f"""You are an expert query router. Analyze the user's latest input and chat history to determine the best route.
# CHAT HISTORY:
# ---
# {chat_history_formatted}
# ---
# LATEST USER INPUT: "{q}"
# Choose one of the following routes:
# 1.  `retrieve`: If the user is asking a new question that requires knowledge.
# 2.  `direct_answer`: For greetings, follow-ups, or questions that can be answered from chat history alone.
# Return ONLY a JSON object with your decision. Example: {{"route": "retrieve"}}
# """
#     raw = get_llm_response(prompt, role="planner")
#     try:
#         route = extract_json(raw).get("route", "retrieve")
#     except:
#         route = "retrieve"
#     reasoning_steps.append(f"THINK (Router): Decided that the best route for this query is '{route}'.")
#     return {**state, "route": route, "reasoning_steps": reasoning_steps}

# def should_retrieve(state: AgentState) -> str:
#     return "retrieve" if state.get("route") == "retrieve" else "planner"

# def retrieve_node(state: AgentState) -> AgentState:
#     q = state["user_input"]
#     r = Retriever()
#     reasoning_steps = state.get("reasoning_steps", [])
#     try:
#         docs = r.fetch_relevant_chunks(q)
#         ctx = "\n\n".join(d.get("text", "") for d in docs)
#         reasoning_steps.append(f"ACTION (Retrieve): Found {len(docs)} relevant document chunks.")
#     except Exception as e:
#         ctx = ""
#         reasoning_steps.append(f"ACTION (Retrieve): Failed with error - {e}")
#     return {**state, "retrieved_context": ctx or "", "reasoning_steps": reasoning_steps}

# # --- START OF MODIFIED SECTION ---

# def planner_node(state: AgentState) -> AgentState:
#     q = state["user_input"]
#     ctx = state.get("retrieved_context", "")
#     reasoning_steps = state.get("reasoning_steps", [])
#     tool_history = state.get("tool_history", [])
#     chat_history_formatted = _format_chat_history(state.get("chat_history", []))
    
#     # Generate the detailed tool descriptions including arguments
#     tool_descriptions = []
#     for tool in TOOLS:
#         try:
#             schema = tool.args_schema.model_json_schema()
#             desc = f"- **{tool.name}**: {schema.get('description', '')}\n  - Arguments:\n"
#             properties = schema.get('properties', {})
#             if not properties:
#                 desc += "    - (No arguments required)\n"
#             else:
#                 for prop, details in properties.items():
#                     desc += f"    - `{prop}` ({details.get('type')}): {details.get('description')}\n"
#             tool_descriptions.append(desc)
#         except Exception:
#             # Fallback for simpler tool definitions
#             tool_descriptions.append(f"- **{tool.name}**")
#     tool_list_detailed = "\n".join(tool_descriptions)

#     # Updated prompt with stricter instructions
#     prompt = f"""You are the PLANNER. Your job is to decide the next step. Analyze the chat history and the user's latest question.

# CHAT HISTORY:
# ---
# {chat_history_formatted}
# ---
# LATEST USER QUESTION: "{q}"
# RETRIEVED CONTEXT (if any):
# ---
# {ctx}...
# ---
# TOOL HISTORY (for this turn):
# ---
# {json.dumps(tool_history, indent=2)}
# ---
# AVAILABLE TOOLS:
# {tool_list_detailed}
# ---
# **CRITICAL INSTRUCTION:** When using a tool, you **MUST** use the exact argument names specified in the 'Arguments' section for each tool. Do not invent new argument names.

# Return ONLY valid JSON for the next step. If the task is finished, set "action": "answer".
# {{
#   "action": "tools" | "answer",
#   "tool_name": "<name>",
#   "tool_input": {{ "arg": "val" }},
#   "reasoning": "<your reasoning>"
# }}
# """
#     raw = get_llm_response(prompt, role="planner")
#     plan = extract_json(raw)
#     if not plan:
#         plan = {"action": "answer", "reasoning": "Planner failed, defaulting to answer."}
    
#     reasoning_steps.append(f"THINK (Planner): {plan.get('reasoning', 'No reasoning.')}\nAction: {plan.get('action')}")
#     return {**state, "plan": plan, "reasoning_steps": reasoning_steps}

# # --- END OF MODIFIED SECTION ---


# # (generate_content_node, tool_node, and actor_node are unchanged)
# def generate_content_node(state: AgentState) -> AgentState:
#     q = state["user_input"]
#     ctx = state.get("retrieved_context", "")
#     plan = state.get("plan", {})
#     report_title = plan.get("tool_input", {}).get("title", "Report")
#     reasoning_steps = state.get("reasoning_steps", [])
#     reasoning_steps.append(f"ACTION (Content Generator): Writing content for report '{report_title}'.")
#     prompt = f"You are a Productivity Expert. Write a comprehensive article for a report titled '{report_title}' based on the user's request '{q}' and the following context:\n\n{ctx}\n\nGenerate ONLY the body content."
#     content = get_llm_response(prompt, role="actor")
#     return {**state, "generated_content": content, "reasoning_steps": reasoning_steps}

# def tool_node(state: AgentState) -> AgentState:
#     plan = state.get("plan", {})
#     reasoning_steps = state.get("reasoning_steps", [])
#     tool_history = state.get("tool_history", [])
#     tool_name = (plan.get("tool_name") or "").lower()
#     tool_input = plan.get("tool_input", {})
#     tool = TOOLS_BY_NAME.get(tool_name)
#     if not tool:
#         result = {"status": "error", "error": f"Tool '{tool_name}' not found."}
#     else:
#         try:
#             if tool_name == "create_docx_report":
#                 tool_input['content'] = state.get("generated_content", "Error: No content generated.")
#             if tool_name == "send_email":
#                 # This logic to find the attachment path remains crucial
#                 for past_tool in reversed(state.get("tool_history", []) + state.get("chat_history", [])):
#                     if isinstance(past_tool, dict) and past_tool.get("tool_name") == "create_docx_report" and past_tool.get("result", {}).get("status") == "ok":
#                         tool_input['attachment_path'] = past_tool["result"]["path"]
#                         break
#             reasoning_steps.append(f"ACTION: Executing tool '{tool.name}' with input: {tool_input}")
#             result = tool.func(tool_input)
#         except Exception as e:
#             result = {"status": "error", "error": f"Tool execution failed: {e}"}
#     reasoning_steps.append(f"OBSERVATION (tool): {result}")
#     tool_history.append({"tool_name": tool_name, "tool_input": tool_input, "result": result})
#     return {**state, "reasoning_steps": reasoning_steps, "tool_history": tool_history}

# def actor_node(state: AgentState) -> AgentState:
#     reasoning_steps = state.get("reasoning_steps", [])
#     tool_history = state.get("tool_history", [])
#     user_question = state["user_input"]
#     context = state.get("retrieved_context", "No context retrieved.")
#     chat_history_formatted = _format_chat_history(state.get("chat_history", []))
#     reasoning_steps.append("ACTION (Actor): Generating final conversational answer.")
#     prompt = f"""You are a helpful Productivity Expert. Review the CHAT HISTORY and LATEST USER QUESTION, then provide a final, comprehensive response.
# Your response must have two parts:
# 1.  **A Direct Answer:** Answer the user's latest question. Use the chat history and any retrieved context.
# 2.  **A Summary of Actions:** After the answer, summarize any actions you successfully completed *in this turn*.

# CHAT HISTORY:
# ---
# {chat_history_formatted}
# ---
# LATEST USER QUESTION: "{user_question}"
# CONTEXT (for the latest question):
# ---
# {context}
# ---
# ACTIONS COMPLETED (this turn):
# ---
# {json.dumps(tool_history, indent=2)}
# ---
# Generate the final Markdown response now.
# """
#     final_answer_content = get_llm_response(prompt, role="actor")
#     return {**state, "final_answer": final_answer_content, "reasoning_steps": reasoning_steps}

# def should_continue(state: AgentState) -> str:
#     action = state.get("plan", {}).get("action")
#     if action == "answer":
#         return "actor"
#     tool_name = state.get("plan", {}).get("tool_name", "")
#     if tool_name == "create_docx_report":
#         return "generate_content"
#     return "tool"

# def build_reasoning_graph():
#     G = StateGraph(AgentState)
#     G.add_node("router", RunnableLambda(route_query_node))
#     G.add_node("retrieve", RunnableLambda(retrieve_node))
#     G.add_node("planner", RunnableLambda(planner_node))
#     G.add_node("generate_content", RunnableLambda(generate_content_node))
#     G.add_node("tool", RunnableLambda(tool_node))
#     G.add_node("actor", RunnableLambda(actor_node))
#     G.set_entry_point("router")
#     G.add_conditional_edges("router", should_retrieve, {"retrieve": "retrieve", "planner": "planner"})
#     G.add_edge("retrieve", "planner")
#     G.add_conditional_edges("planner", should_continue, {"generate_content": "generate_content", "tool": "tool", "actor": "actor"})
#     G.add_edge("generate_content", "tool")
#     G.add_edge("tool", "planner")
#     G.add_edge("actor", END)
#     return G.compile()

# REASONING_GRAPH = build_reasoning_graph()

# graph_agent.py (with a more cautious planner)






import json
import re
from typing import TypedDict, Optional, Dict, Any, List

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

from retriever import Retriever
from tools import TOOLS, TOOLS_BY_NAME
from llm_client import get_llm_response

# --- Helper Functions & State Definition (Unchanged) ---
def extract_json(text: str):
    if not text: return None
    # This regex is more robust and handles nested structures
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None

def _format_chat_history(history: List[Dict[str, Any]]) -> str:
    if not history: return "No previous conversation history."
    return "\n".join([f"{'User' if m.get('role') == 'user' else 'Assistant'}: {m.get('content', '')}" for m in history])

class AgentState(TypedDict, total=False):
    user_input: str
    chat_history: List[Dict[str, Any]]
    retrieved_context: Optional[str]
    plan: Optional[Dict[str, Any]]
    generated_content: Optional[str]
    final_answer: Optional[str]
    reasoning_steps: List[str]
    tool_history: List[Dict[str, Any]]
    route: str

# --- Graph Nodes ---
def route_query_node(state: AgentState) -> AgentState:
    q, history = state["user_input"], state.get("chat_history", [])
    reasoning_steps = state.get("reasoning_steps", [])
    
    # PROMPT CORRECTION: More explicit instructions for the router.
    prompt = f"""You are a methodical query router. Your job is to analyze the user's latest message and the conversation history to choose the correct path.

CONVERSATION HISTORY:
---
{_format_chat_history(history)}
---
LATEST USER MESSAGE: "{q}"

Based on the message, choose one route:
1.  `retrieve`: If the user is asking a new question that requires external knowledge (e.g., "What is the Pomodoro Technique?", "How do I create SMART goals?","my name is prakhar, and my email id is praj.muz03@gmail.com.I have a quiz after 1 week, can you make a strategy to properly manage my time and increase my productivity.can you generate a report of this strategy that you provided.can you send email of that report you created to my email.").
2.  `direct_answer`: If the message is a greeting, a thank you, or a follow-up that can be answered **only** from the conversation history. Also use this route if the user is asking to perform an action with a tool (e.g., "email that report," "create a document about...").

Return ONLY a valid JSON object. Example:
{{"route": "retrieve"}}"""
    
    try: route = extract_json(get_llm_response(prompt, role="planner")).get("route", "retrieve")
    except: route = "retrieve"
    reasoning_steps.append(f"THINK (Router): Decided route is '{route}'.")
    return {**state, "route": route, "reasoning_steps": reasoning_steps}

def retrieve_node(state: AgentState) -> AgentState:
    q, reasoning_steps = state["user_input"], state.get("reasoning_steps", [])
    try:
        docs = Retriever().fetch_relevant_chunks(q)
        ctx = "\n\n".join(d.get("text", "") for d in docs)
        reasoning_steps.append(f"ACTION (Retrieve): Found {len(docs)} relevant document chunks.")
    except Exception as e:
        ctx = ""
        reasoning_steps.append(f"ACTION (Retrieve): Failed with error - {e}")
    return {**state, "retrieved_context": ctx or "", "reasoning_steps": reasoning_steps}

def decide_tool_or_answer_node(state: AgentState) -> AgentState:
    q, tool_history, history = state["user_input"], state.get("tool_history", []), state.get("chat_history", [])
    reasoning_steps = state.get("reasoning_steps", [])
    tool_descriptions = "\n".join([f"- {t.name}" for t in TOOLS])

    # PROMPT CORRECTION: Clearer, rule-based decision logic.
    prompt = f"""You are a logical decision-maker. Based on the user's latest message, decide if a tool is needed or if you can answer directly.

**Decision Logic:**
1.  **Is the task already done?** Check the `TOOL HISTORY` for this turn. If the user's request was just completed, choose `answer`.
2.  **Does the user want to use a tool?** Look for explicit keywords in the `LATEST USER MESSAGE` like 'create', 'generate', 'report', 'doc', 'email', 'send'. If found, choose `tools`.
3.  **Otherwise,** choose `answer`.

**Context:**
---
CHAT HISTORY: {_format_chat_history(history)}
LATEST USER MESSAGE: "{q}"
TOOL HISTORY (this turn): {json.dumps(tool_history, indent=2)}
AVAILABLE TOOLS: {tool_descriptions}
---
Return ONLY a valid JSON object. Specify the `tool_name` if choosing 'tools'.
{{
  "action": "tools" | "answer",
  "tool_name": "<name of tool or null>",
  "reasoning": "<your brief reasoning>"
}}"""
    
    raw = get_llm_response(prompt, role="planner")
    plan = extract_json(raw) or {"action": "answer", "reasoning": "Decision fallback."}
    reasoning_steps.append(f"THINK (Decision): {plan.get('reasoning', 'N/A')}\nAction: {plan.get('action')}")
    return {**state, "plan": plan, "reasoning_steps": reasoning_steps}

def generate_tool_args_node(state: AgentState) -> AgentState:
    q, history, plan = state["user_input"], state.get("chat_history", []), state.get("plan", {})
    reasoning_steps, tool_name = state.get("reasoning_steps", []), plan.get("tool_name")
    tool = TOOLS_BY_NAME.get(tool_name)
    if not tool: return {**state}
    properties = tool.args_schema.model_json_schema().get('properties', {})

    # PROMPT CORRECTION: Stricter rules for JSON generation.
    prompt = f"""You are an argument generator. Your task is to create the JSON arguments for the `{tool_name}` tool.

**CRITICAL RULES:**
1.  Provide a value for **all** required arguments in the schema.
2.  If the user hasn't provided a value (e.g., a 'title'), **invent a sensible one** from the conversation context.
3.  Your output **MUST** be only the JSON object. Do not add explanations.

**Context:**
---
CHAT HISTORY: {_format_chat_history(history)}
LATEST USER MESSAGE: "{q}"
TOOL SCHEMA (`{tool_name}`): {json.dumps(properties, indent=2)}
---
Generate ONLY the JSON object for the `tool_input`.
"""
    
    raw = get_llm_response(prompt, role="planner")
    tool_input = extract_json(raw) or {}
    plan['tool_input'] = tool_input
    reasoning_steps.append(f"THINK (Args): Generated arguments for `{tool_name}` tool.")
    return {**state, "plan": plan, "reasoning_steps": reasoning_steps}

def generate_content_node(state: AgentState) -> AgentState:
    q, ctx, plan, history = state["user_input"], state.get("retrieved_context", ""), state.get("plan", {}), state.get("chat_history", [])
    report_title = plan.get("tool_input", {}).get("title", "Report")
    reasoning_steps = state.get("reasoning_steps", [])
    source_material = f"Use retrieved context:\n\n{ctx}" if ctx.strip() else f"Use chat history as context:\n\n{_format_chat_history(history)}"
    prompt = f"Write the body for a report titled '{report_title}' based on the user's request '{q}'.\n{source_material}\nGenerate ONLY the body content in Markdown format."
    content = get_llm_response(prompt, role="actor")
    reasoning_steps.append(f"ACTION (Content Gen): Wrote content for report '{report_title}'.")
    return {**state, "generated_content": content, "reasoning_steps": reasoning_steps}

def tool_node(state: AgentState) -> AgentState:
    plan, reasoning_steps, tool_history = state.get("plan", {}), state.get("reasoning_steps", []), state.get("tool_history", [])
    tool_name, tool_input = (plan.get("tool_name") or "").lower(), plan.get("tool_input", {})
    tool = TOOLS_BY_NAME.get(tool_name)
    
    if not tool:
        result = {"status": "error", "error": f"Tool '{tool_name}' not found."}
    else:
        try:
            tool_input_final = tool_input.copy()
            if tool_name == "create_docx_report":
                tool_input_final['content'] = state.get("generated_content", "Error: No content was generated for the report.")
            
            # --- START OF MODIFICATION: ROBUST EMAIL ATTACHMENT LOGIC ---
            if tool_name == "send_email":
                attachment_path = None
                # Priority 1: Check if a report was created in the current turn.
                for past_tool in reversed(tool_history):
                    if (past_tool.get("tool_name") == "create_docx_report" and 
                        past_tool.get("result", {}).get("status") == "ok"):
                        attachment_path = past_tool["result"].get("path")
                        break
                
                # Priority 2: If not found, search the entire chat history for a previously mentioned report path.
                if not attachment_path:
                    for msg in reversed(state.get("chat_history", [])):
                        if msg.get("role") == "assistant":
                            # Use regex to find a filepath in past assistant messages
                            match = re.search(r"(reports/[\w\._\-\s]+\.docx)", msg.get("content", ""))
                            if match:
                                attachment_path = match.group(1)
                                break
                
                if attachment_path:
                    tool_input_final['attachment_path'] = attachment_path
                    reasoning_steps.append(f"THINK (Tool Node): Found report path '{attachment_path}' in memory to use as attachment.")
                else:
                    reasoning_steps.append("THINK (Tool Node): Could not find a report path in memory. The email will be sent without an attachment.")
            # --- END OF MODIFICATION ---

            reasoning_steps.append(f"ACTION: Executing tool '{tool.name}' with input: {tool_input}")
            result = tool.func(tool_input_final)
            
        except Exception as e:
            result = {"status": "error", "error": f"Tool execution failed: {e}"}
            
    reasoning_steps.append(f"OBSERVATION (tool): {result}")
    tool_history.append({"tool_name": tool_name, "tool_input": tool_input, "result": result})
    return {**state, "reasoning_steps": reasoning_steps, "tool_history": tool_history}

def actor_node(state: AgentState) -> AgentState:
    reasoning_steps, tool_history, user_question, context, chat_history = state.get("reasoning_steps", []), state.get("tool_history", []), state["user_input"], state.get("retrieved_context", ""), state.get("chat_history", [])
    reasoning_steps.append("ACTION (Actor): Generating final answer.")

    # PROMPT CORRECTION: Added explicit instruction to include the file path.
    prompt = f"""You are a helpful and conversational Productivity Expert. Your task is to provide a final, comprehensive response to the user.

Your response must be structured in two parts:

1.  **A Direct, Conversational Answer:** First, provide a helpful and direct answer to the user's latest question. Use the provided context and chat history to formulate this answer.
2.  **A Summary of Actions:** After the answer, if you have performed any actions in this turn, provide a clear summary of what you did.
    - **CRITICAL:** If you created a report, you **MUST** include the full path to the file in your summary.

**Context for Your Answer:**
---
CHAT HISTORY: {_format_chat_history(chat_history)}
LATEST USER QUESTION: "{user_question}"
RETRIEVED KNOWLEDGE: "{context}"
ACTIONS YOU COMPLETED (this turn): {json.dumps(tool_history, indent=2)}
---
Generate the final, well-formatted Markdown response now.
"""
    
    final_answer_content = get_llm_response(prompt, role="actor")
    return {**state, "final_answer": final_answer_content, "reasoning_steps": reasoning_steps}

# --- Conditional Edges & Graph Assembly (Unchanged) ---
def should_retrieve(state: AgentState) -> str:
    return "retrieve" if state.get("route") == "retrieve" else "decide_tool_or_answer"

def should_use_tool_or_answer(state: AgentState) -> str:
    return "generate_tool_args" if state.get("plan", {}).get("action") == "tools" else "actor"

def should_generate_content_or_tool(state: AgentState) -> str:
    return "generate_content" if state.get("plan", {}).get("tool_name") == "create_docx_report" else "tool"

def build_reasoning_graph():
    G = StateGraph(AgentState)
    nodes = ["router", "retrieve", "decide_tool_or_answer", "generate_tool_args", "generate_content", "tool", "actor"]
    node_funcs = [route_query_node, retrieve_node, decide_tool_or_answer_node, generate_tool_args_node, generate_content_node, tool_node, actor_node]
    for name, func in zip(nodes, node_funcs): G.add_node(name, RunnableLambda(func))
    G.set_entry_point("router")
    G.add_conditional_edges("router", should_retrieve, {"retrieve": "retrieve", "decide_tool_or_answer": "decide_tool_or_answer"})
    G.add_edge("retrieve", "decide_tool_or_answer")
    G.add_conditional_edges("decide_tool_or_answer", should_use_tool_or_answer, {"generate_tool_args": "generate_tool_args", "actor": "actor"})
    G.add_conditional_edges("generate_tool_args", should_generate_content_or_tool, {"generate_content": "generate_content", "tool": "tool"})
    G.add_edge("generate_content", "tool")
    G.add_edge("tool", "decide_tool_or_answer")
    G.add_edge("actor", END)
    return G.compile()

REASONING_GRAPH = build_reasoning_graph()

# ### Summary of Expert Updates

# Here is a clear explanation of the changes I made and the reasoning behind them.

# #### 1. Smarter Email Attachment Logic in `tool_node`
# The most significant functional change is in the `tool_node` function. The agent can now intelligently find a report to email even if it was created in a previous turn.

# *   **Previous Logic:** The agent could only find an attachment path if the `create_docx_report` tool was called in the *exact same turn* as the `send_email` tool. This would fail if the user said "Create a report" and then, in a separate message, "Now email it to me."
# *   **New Logic:**
#     1.  **Priority 1 (Current Turn):** It first checks the `tool_history` of the current turn, just as before. This is the most immediate and relevant context.
#     2.  **Priority 2 (Chat History):** If no report was created in the current turn, it now searches backwards through the entire `chat_history`. It uses a regular expression (`re.search`) to find any assistant message that mentions a file path (e.g., `reports/My_Report.docx`).
# *   **Benefit:** This makes the agent's memory far more effective. It can now handle multi-turn conversations involving file actions, which is a much more realistic and user-friendly behavior.

# #### 2. Explicit File Path in Final Answer (`actor_node`)
# You requested that the path to a created DOCX file be printed for the user. I have updated the prompt for the `actor_node` to ensure this happens.

# *   **Previous Logic:** The agent would simply say it created a report.
# *   **New Prompt:** I added a **"CRITICAL"** instruction directly into the prompt: *"If you created a report, you **MUST** include the full path to the file in your summary."*
# *   **Benefit:** The user now receives immediate, actionable information. They know exactly where the file they asked for is located, which is essential for the `st.download_button` in the frontend to work correctly and for user clarity.

#### 3. Further Prompt Corrections for Clarity and Reliability
# I have continued to refine the prompts for other nodes to make them even more foolproof.

# *   **`route_query_node`:** Added a specific instruction to use the `direct_answer` route for tool-related commands (like "email that report"), ensuring the agent doesn't unnecessarily perform a knowledge base search when the user wants to perform an action.
# *   **`decide_tool_or_answer_node`:** Rephrased the prompt to use a more structured "Decision Logic" format, making it easier for the LLM to follow the rules in the correct order.
# *   **`generate_tool_args_node`:** Reinforced the rule that the LLM's output must *only* be the JSON object. This is a best practice that drastically reduces parsing errors.

# These updates make your agent more intelligent, its behavior more predictable, and its final output more helpful to the end-user.