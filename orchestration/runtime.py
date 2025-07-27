"""
orchestration/runtime.py

Manages the orchestration runtime, including starting and stopping the runtime process.
"""

# === Imports ===
from semantic_kernel.agents.runtime import InProcessRuntime

# === Class Definition ===
class OrchestrationRuntime:
    """
    Wrapper for InProcessRuntime to manage start and stop operations.
    """

    def __init__(self):
        # Initialize the in-process runtime
        self.runtime = InProcessRuntime()

    # === Methods ===
    def start(self):
        """
        Starts the runtime process.
        """
        try:
            self.runtime.start()
        except Exception as e:
            # Log and re-raise any errors during runtime start
            print(f"[Runtime] Error starting runtime: {e}")
            raise

    async def stop_when_idle(self):
        """
        Stops the runtime when idle (async).
        """
        try:
            await self.runtime.stop_when_idle()
        except Exception as e:
            # Log and re-raise any errors during runtime stop
            print(f"[Runtime] Error stopping runtime: {e}")
            raise
