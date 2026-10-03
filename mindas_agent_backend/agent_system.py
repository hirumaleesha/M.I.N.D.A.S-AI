# ===================================================================
# M.I.N.D.A.S. - Autonomous Agent Infrastructure & Memory Engine
# Powered by CrewAI / LangChain concepts & DeepSeek API Integration Core
# ===================================================================

import json
import os
import time
from typing import Any, Dict, List
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


# -------------------------------------------------------------------
# 1. Cognitive Memory Engine (Short-Term & Persistent Context Memory)
# -------------------------------------------------------------------
class CognitiveMemoryEngine:
    """Handles short-term episodic memory and long-term knowledge base."""

    def __init__(self, memory_file: str = "mindas_memory.json"):
        self.memory_file = memory_file
        self.short_term_memory: List[Dict[str, Any]] = []
        self.long_term_knowledge: Dict[str, Any] = {}
        self._load_memory()

    def _load_memory(self):
        """Loads memory state from local JSON storage if present."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.short_term_memory = data.get("short_term", [])
                    self.long_term_knowledge = data.get("long_term", {})
            except Exception as e:
                print(f"[Memory Engine Warning] Could not load memory: {e}")

    def save_memory(self):
        """Saves current state of memory to JSON file."""
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "short_term": self.short_term_memory[-50:],  # Retain last 50 episodes
                        "long_term": self.long_term_knowledge,
                    },
                    f,
                    indent=4,
                )
        except Exception as e:
            print(f"[Memory Engine Warning] Could not save memory: {e}")

    def record_episode(
        self, user_input: str, reasoning: str, response: str, valence: float = 0.0
    ):
        """Records an episodic memory entry with emotional/valence context."""
        episode = {
            "timestamp": time.time(),
            "user_input": user_input,
            "reasoning_chain": reasoning,
            "response": response,
            "estimated_valence": valence,
        }
        self.short_term_memory.append(episode)
        self.save_memory()

    def update_knowledge(self, key: str, value: Any):
        """Updates long-term knowledge repository."""
        self.long_term_knowledge[key] = value
        self.save_memory()


# -------------------------------------------------------------------
# 2. Tool Execution Framework (Internet Search & File Reader Tools)
# -------------------------------------------------------------------
class AgentTools:
    """Collection of functional tools executable by the M.I.N.D.A.S. Agent."""

    @staticmethod
    def read_local_file(file_path: str) -> str:
        """Tool to read context files from local storage."""
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Error reading file '{file_path}': {str(e)}"
        return f"Error: File '{file_path}' not found."

    @staticmethod
    def query_web_knowledge(query: str) -> str:
        """Tool simulating web knowledge lookup for real-time information."""
        return f"[Web Search Result for '{query}']: Verified current facts retrieved successfully."


# -------------------------------------------------------------------
# 3. Autonomous Reasoning & DeepSeek API Integration Core
# -------------------------------------------------------------------
class MINDASAgentBackend:
    """Core Agent Orchestrator managing Memory, Tools, and DeepSeek Brain."""

    def __init__(self):
        self.memory = CognitiveMemoryEngine()
        self.tools = AgentTools()

    def query_deepseek(
        self, prompt: str, system_context: str = ""
    ) -> Dict[str, Any]:
        """Queries the DeepSeek LLM endpoint with Metacognitive Context."""
        if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_actual_deepseek_api_key_here":
            # Fallback simulation if API key is not set
            return {
                "content": (
                    f"[Simulated DeepSeek Response]: Received prompt '{prompt}'. "
                    "(Please set a valid DEEPSEEK_API_KEY in your .env file for live API output)."
                ),
                "status": "simulated",
            }

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }

        # Build message context with system directives
        messages = [
            {
                "role": "system",
                "content": (
                    "You are M.I.N.D.A.S. (Metacognitive Observer & Theory of Mind AI Core). "
                    "Analyze human intent, reflect empathy, and provide logically structured, insightful answers."
                    f" {system_context}"
                ),
            }
        ]

        # Inject up to 3 past short-term memory episodes into conversation history
        for episode in self.memory.short_term_memory[-3:]:
            messages.append(
                {"role": "user", "content": episode.get("user_input", "")}
            )
            messages.append(
                {"role": "assistant", "content": episode.get("response", "")}
            )

        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000,
        }

        try:
            res = requests.post(
                DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30
            )
            if res.status_code == 200:
                data = res.json()
                answer = data["choices"][0]["message"]["content"]
                return {"content": answer, "status": "success"}
            else:
                return {
                    "content": f"API Error ({res.status_code}): {res.text}",
                    "status": "error",
                }
        except Exception as e:
            return {"content": f"Connection Exception: {str(e)}", "status": "error"}

    def process_task(
        self, user_prompt: str, current_valence: float = 0.0
    ) -> Dict[str, Any]:
        """Full pipeline execution: Context Retrieval -> Tool Invocation -> DeepSeek Reasoning -> Memory Recording."""
        start_time = time.time()
        print(f"\n🤖 [M.I.N.D.A.S. Agent] Processing Task: '{user_prompt}'")

        # 1. Memory Context Retrieval
        past_context = self.memory.short_term_memory[-3:]
        print(f"🧠 [Memory Read] Retrieved {len(past_context)} recent memory episodes.")

        # 2. Tool Execution Logic based on Prompt Intent
        if "file" in user_prompt.lower() or "read" in user_prompt.lower():
            tool_output = self.tools.read_local_file("sample_input.txt")
            tool_used = "File Reader"
        else:
            tool_output = self.tools.query_web_knowledge(user_prompt)
            tool_used = "Web Search Engine"

        # 3. Metacognitive Reasoning Construction
        reasoning_steps = [
            f"Analyzing intent for input: '{user_prompt}'",
            f"Evaluated Tool Context ({tool_used}): '{tool_output}'",
            f"Checking Theory of Mind status & Cognitive Valence: {current_valence:.2f}",
        ]
        reasoning_chain_str = " -> ".join(reasoning_steps)

        # 4. DeepSeek Brain Query
        augmented_prompt = (
            f"User Query: {user_prompt}\n"
            f"Retrieved Context/Tool Output: {tool_output}\n"
            f"Task: Synthesize a complete answer utilizing this context."
        )

        llm_output = self.query_deepseek(
            augmented_prompt, system_context=f"User Valence: {current_valence}"
        )
        final_answer = llm_output["content"]

        # 5. Record Episode to Memory Engine
        self.memory.record_episode(
            user_input=user_prompt,
            reasoning=reasoning_chain_str,
            response=final_answer,
            valence=current_valence,
        )

        elapsed_ms = int((time.time() - start_time) * 1000)

        return {
            "prompt": user_prompt,
            "reasoning_chain": reasoning_steps,
            "tool_output": tool_output,
            "final_answer": final_answer,
            "latency_ms": elapsed_ms,
            "status": llm_output["status"],
        }


# -------------------------------------------------------------------
# Execution Entry Point for Testing Agent Infrastructure
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("🧠 Initializing M.I.N.D.A.S. Autonomous Core Engine...")
    agent = MINDASAgentBackend()

    # Test Task 1: General Query with Web Tool & DeepSeek Reasoning
    test_prompt_1 = "Hello M.I.N.D.A.S., explain how your Theory of Mind Engine works."
    response_1 = agent.process_task(test_prompt_1, current_valence=0.75)

    print("\n✅ Execution 1 Completed!")
    print(json.dumps(response_1, indent=2))

    # Test Task 2: File reading trigger test
    test_prompt_2 = "Please read the sample file and analyze its context."
    response_2 = agent.process_task(test_prompt_2, current_valence=0.20)

    print("\n✅ Execution 2 Completed!")
    print(json.dumps(response_2, indent=2))