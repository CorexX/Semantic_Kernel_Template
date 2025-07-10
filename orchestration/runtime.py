"""
orchestration/runtime.py

Manages the orchestration runtime, including starting and stopping the runtime process.
"""

from semantic_kernel.agents.runtime import InProcessRuntime

class OrchestrationRuntime:
    """
    Wrapper for InProcessRuntime to manage start and stop operations.
    """

    def __init__(self):
        self.runtime = InProcessRuntime()

    def start(self):
        """
        Starts the runtime process.
        """
        try:
            self.runtime.start()
        except Exception as e:
            print(f"[Runtime] Error starting runtime: {e}")
            raise

    async def stop_when_idle(self):
        """
        Stops the runtime when idle (async).
        """
        try:
            await self.runtime.stop_when_idle()
        except Exception as e:
            print(f"[Runtime] Error stopping runtime: {e}")
            raise
