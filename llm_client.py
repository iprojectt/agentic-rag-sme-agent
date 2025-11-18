# # llm_client.py  — TWO-MODEL VERSION (Generation + Judge)
# # Includes auto-tuning rate-limit logic

# import os
# import time
# import google.generativeai as genai
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# # -----------------------------------------------------------
# # CONFIG
# # -----------------------------------------------------------
# LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # TWO MODEL SYSTEM (Generation + Judge)
# GEMINI_MODEL_GENERATE = os.getenv("LLM_MODEL_GENERATE", "gemini-2.5-flash")
# GEMINI_MODEL_JUDGE    = os.getenv("LLM_MODEL_JUDGE", "gemini-2.5-pro")

# OPENAI_MODEL_GENERATE = os.getenv("OPENAI_MODEL_GENERATE", "gpt-4o-mini")
# OPENAI_MODEL_JUDGE    = os.getenv("OPENAI_MODEL_JUDGE", "gpt-4o")

# # -----------------------------------------------------------
# # AUTO-TUNE GLOBALS
# # -----------------------------------------------------------
# GLOBAL_DELAY = 1.0
# MIN_DELAY = 0.5
# MAX_DELAY = 6.0
# SUCCESS_COUNTER = 0


# def compute_dynamic_delay(prompt_len: int) -> float:
#     base = GLOBAL_DELAY
#     size_factor = min(2.0, prompt_len / 4000)
#     return min(MAX_DELAY, base + size_factor)

# def increase_delay():
#     global GLOBAL_DELAY
#     GLOBAL_DELAY = min(GLOBAL_DELAY * 2, MAX_DELAY)
#     print(f"🔧 AutoTune: RATE-LIMIT INCREASE → delay={GLOBAL_DELAY:.2f}s")

# def decrease_delay():
#     global GLOBAL_DELAY
#     GLOBAL_DELAY = max(MIN_DELAY, GLOBAL_DELAY * 0.9)
#     print(f"🔧 AutoTune: RATE-LIMIT DECREASE → delay={GLOBAL_DELAY:.2f}s")


# # -----------------------------------------------------------
# # GEMINI: Initialize two separate models
# # -----------------------------------------------------------
# gemini_generate = None
# gemini_judge = None

# if LLM_PROVIDER == "gemini":
#     try:
#         genai.configure(api_key=GOOGLE_API_KEY)

#         gemini_generate = genai.GenerativeModel(GEMINI_MODEL_GENERATE)
#         gemini_judge    = genai.GenerativeModel(GEMINI_MODEL_JUDGE)

#         print(f"Gemini GENERATE model: {GEMINI_MODEL_GENERATE}")
#         print(f"Gemini JUDGE model:    {GEMINI_MODEL_JUDGE}")

#     except Exception as e:
#         print("Gemini init failed:", e)


# # -----------------------------------------------------------
# # OPENAI: Initialize two separate models
# # -----------------------------------------------------------
# openai_client = None
# if LLM_PROVIDER == "openai":
#     try:
#         openai_client = OpenAI(api_key=OPENAI_API_KEY)
#         print(f"OpenAI GENERATE model: {OPENAI_MODEL_GENERATE}")
#         print(f"OpenAI JUDGE model:    {OPENAI_MODEL_JUDGE}")
#     except Exception as e:
#         print("OpenAI init failed:", e)


# # -----------------------------------------------------------
# # INTERNAL Gemini Helper
# # -----------------------------------------------------------
# def _gemini_call(model, prompt: str) -> str:
#     global SUCCESS_COUNTER

#     if model is None:
#         return "Gemini model not initialized."

#     dynamic_delay = compute_dynamic_delay(len(prompt))

#     for attempt in range(5):
#         try:
#             res = model.generate_content(prompt)

#             time.sleep(dynamic_delay)

#             SUCCESS_COUNTER += 1
#             if SUCCESS_COUNTER >= 5:
#                 decrease_delay()
#                 SUCCESS_COUNTER = 0

#             return res.text or ""

#         except Exception as e:
#             err = str(e).lower()
#             if "429" in err or "quota" in err:
#                 wait = 2 ** attempt
#                 print(f"⚠️ Gemini 429 → retry in {wait}s")
#                 increase_delay()
#                 time.sleep(wait)
#                 continue

#             print("Gemini error:", e)
#             return "Gemini API error."

#     return "Gemini failed after retries."


# # -----------------------------------------------------------
# # INTERNAL OpenAI Helper
# # -----------------------------------------------------------
# def _openai_call(model_name: str, prompt: str) -> str:
#     global SUCCESS_COUNTER

#     if openai_client is None:
#         return "OpenAI not initialized."

#     dynamic_delay = compute_dynamic_delay(len(prompt))

#     for attempt in range(5):
#         try:
#             res = openai_client.chat.completions.create(
#                 model=model_name,
#                 messages=[{"role": "user", "content": prompt}],
#             )

#             time.sleep(dynamic_delay)

#             SUCCESS_COUNTER += 1
#             if SUCCESS_COUNTER >= 5:
#                 decrease_delay()
#                 SUCCESS_COUNTER = 0

#             return res.choices[0].message.content

#         except Exception as e:
#             err = str(e).lower()
#             if "429" in err or "rate" in err:
#                 wait = 2 ** attempt
#                 print(f"⚠️ OpenAI 429 → retry in {wait}s")
#                 increase_delay()
#                 time.sleep(wait)
#                 continue

#             print("OpenAI error:", e)
#             return "OpenAI API error."

#     return "OpenAI failed after retries."


# # -----------------------------------------------------------
# # PUBLIC FUNCTIONS
# # -----------------------------------------------------------

# # 1️⃣ MODEL THAT GENERATES ANSWERS (FLASH / MINI)
# def llm_generate(prompt: str) -> str:
#     print(f"[LLM-GENERATE] Model={GEMINI_MODEL_GENERATE if LLM_PROVIDER=='gemini' else OPENAI_MODEL_GENERATE}, len={len(prompt)}")

#     if LLM_PROVIDER == "gemini":
#         return _gemini_call(gemini_generate, prompt)
#     else:
#         return _openai_call(OPENAI_MODEL_GENERATE, prompt)


# # 2️⃣ MODEL THAT JUDGES ANSWERS (PRO / GPT-4)
# def llm_judge(prompt: str) -> str:
#     print(f"[LLM-JUDGE] Model={GEMINI_MODEL_JUDGE if LLM_PROVIDER=='gemini' else OPENAI_MODEL_JUDGE}, len={len(prompt)}")

#     if LLM_PROVIDER == "gemini":
#         return _gemini_call(gemini_judge, prompt)
#     else:
#         return _openai_call(OPENAI_MODEL_JUDGE, prompt)


# # 3️⃣ BACKWARD COMPATIBILITY
# def get_llm_response(prompt: str) -> str:
#     """
#     Old interface — now defaults to GENERATION model.
#     """
#     return llm_generate(prompt)



# llm_client.py  — THREE-ROLE VERSION (actor, planner, critic)
# Retains your TWO-MODEL logic + auto-tune backoff







# llm_client.py — TWO-MODE MULTI-PROVIDER ENGINE (FINAL)

import os
import time
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

# load_dotenv()
load_dotenv(dotenv_path="/home/raj/LMA_major/.env")
# -----------------------------------------------------------
# CONFIG
# -----------------------------------------------------------
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# MODEL SETTINGS — SUPPORT MIXED PROVIDERS
GEMINI_MODEL_GENERATE = os.getenv("LLM_MODEL_GENERATE", "gemini-2.5-flash")
GEMINI_MODEL_JUDGE    = os.getenv("LLM_MODEL_JUDGE", "gemini-2.5-flash")   # DEFAULT: USE OPENAI FOR JUDGE

OPENAI_MODEL_GENERATE = os.getenv("OPENAI_MODEL_GENERATE", "gpt-4o-mini")
OPENAI_MODEL_JUDGE    = os.getenv("OPENAI_MODEL_JUDGE",  "gpt-4o")

print("======================================")
print("LLM CLIENT CONFIGURATION")
print(f"PROVIDER: {LLM_PROVIDER}")
print(f"GEMINI ACTOR: {GEMINI_MODEL_GENERATE}")
print(f"GEMINI JUDGE: {GEMINI_MODEL_JUDGE}")
print(f"OPENAI ACTOR: {OPENAI_MODEL_GENERATE}")
print(f"OPENAI JUDGE: {OPENAI_MODEL_JUDGE}")
print("======================================\n")

# -----------------------------------------------------------
# RATE LIMIT ADAPTATION
# -----------------------------------------------------------
GLOBAL_DELAY = 1.0
MIN_DELAY = 0.5
MAX_DELAY = 6.0
SUCCESS_COUNTER = 0

def compute_dynamic_delay(prompt_len: int) -> float:
    base = GLOBAL_DELAY
    size_factor = min(2.0, prompt_len / 4000)
    return min(MAX_DELAY, base + size_factor)

def increase_delay():
    global GLOBAL_DELAY
    GLOBAL_DELAY = min(GLOBAL_DELAY * 2, MAX_DELAY)
    print(f"🔧 AutoTune: Increased delay → {GLOBAL_DELAY:.2f}s")

def decrease_delay():
    global GLOBAL_DELAY
    GLOBAL_DELAY = max(MIN_DELAY, GLOBAL_DELAY * 0.9)
    print(f"🔧 AutoTune: Decreased delay → {GLOBAL_DELAY:.2f}s")

# -----------------------------------------------------------
# GEMINI INIT
# -----------------------------------------------------------
gemini_generate = None
gemini_judge = None

try:
    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)
        gemini_generate = genai.GenerativeModel(GEMINI_MODEL_GENERATE)

        # Only initialize Gemini judge if Gemini judge model is chosen
        if GEMINI_MODEL_JUDGE.startswith("gemini"):
            gemini_judge = genai.GenerativeModel(GEMINI_MODEL_JUDGE)
except Exception as e:
    print("⚠️ Gemini init failed:", e)

# -----------------------------------------------------------
# OPENAI INIT
# -----------------------------------------------------------
openai_client = None
try:
    if OPENAI_API_KEY:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    print("⚠️ OpenAI init failed:", e)

# -----------------------------------------------------------
# INTERNAL GEMINI CALL
# -----------------------------------------------------------
def _gemini_call(model, prompt: str) -> str:
    global SUCCESS_COUNTER
    if model is None:
        return "Gemini model not initialized."

    delay = compute_dynamic_delay(len(prompt))

    for attempt in range(5):
        try:
            res = model.generate_content(prompt)
            time.sleep(delay)
            SUCCESS_COUNTER += 1
            if SUCCESS_COUNTER >= 5:
                decrease_delay()
                SUCCESS_COUNTER = 0
            return res.text or ""
        except Exception as e:
            msg = str(e).lower()
            if "429" in msg or "quota" in msg or "exhausted" in msg:
                wait = 2 ** attempt
                print(f"⚠️ Gemini 429 → retrying in {wait}s")
                increase_delay()
                time.sleep(wait)
                continue
            return f"Gemini API error: {e}"
    return "Gemini failed after retries."

# -----------------------------------------------------------
# INTERNAL OPENAI CALL
# -----------------------------------------------------------
def _openai_call(model_name: str, prompt: str) -> str:
    global SUCCESS_COUNTER
    if openai_client is None:
        return "OpenAI not initialized."

    delay = compute_dynamic_delay(len(prompt))

    for attempt in range(5):
        try:
            res = openai_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            time.sleep(delay)
            SUCCESS_COUNTER += 1
            if SUCCESS_COUNTER >= 5:
                decrease_delay()
                SUCCESS_COUNTER = 0
            return res.choices[0].message.content
        except Exception as e:
            msg = str(e).lower()
            if "429" in msg:
                wait = 2 ** attempt
                print(f"⚠️ OpenAI 429 → retrying in {wait}s")
                increase_delay()
                time.sleep(wait)
                continue
            return f"OpenAI API error: {e}"
    return "OpenAI failed after retries."

# -----------------------------------------------------------
# PUBLIC UNIFIED ROUTER
# -----------------------------------------------------------
def get_llm_response(prompt: str, role: str = "actor") -> str:
    """
    role = actor | planner | critic
    Planner + Critic use JUDGE model
    Actor uses GENERATE model
    Supports mixed providers automatically.
    """

    role = role.lower().strip()

    # ---------------------------------------------
    # ACTOR (always generation)
    # ---------------------------------------------
    if role == "actor":
        if LLM_PROVIDER == "gemini":
            return _gemini_call(gemini_generate, prompt)
        else:
            return _openai_call(OPENAI_MODEL_GENERATE, prompt)

    # ---------------------------------------------
    # PLANNER / CRITIC (judge model)
    # ---------------------------------------------
    if role in ("planner", "critic"):

        # If judge model is OpenAI
        if GEMINI_MODEL_JUDGE.startswith("gpt-") or GEMINI_MODEL_JUDGE.startswith("openai"):
            return _openai_call(GEMINI_MODEL_JUDGE, prompt)

        # If judge is Gemini
        return _gemini_call(gemini_judge, prompt)

    # Default fallback
    return get_llm_response(prompt, role="actor")


# -----------------------------------------------------------
# BACKWARD COMPAT
# -----------------------------------------------------------
def llm_generate(prompt: str) -> str:
    return get_llm_response(prompt, role="actor")

def llm_judge(prompt: str) -> str:
    return get_llm_response(prompt, role="critic")


if __name__ == "__main__":
    print("Actor:", llm_generate("Test actor")[:100])
    print("Critic:", llm_judge("Test critic")[:100])
