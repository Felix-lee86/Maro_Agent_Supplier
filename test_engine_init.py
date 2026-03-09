from reasoning_engine import MaroReasoningEngine
import sys

try:
    print("Initializing engine...")
    engine = MaroReasoningEngine()
    print("SUCCESS: Engine initialized.")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)
