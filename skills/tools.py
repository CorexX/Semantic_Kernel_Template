"""
skills/tools.py

Provides general utility functions as plugins for the Semantic Kernel system.
"""

# === Imports ===
from semantic_kernel.functions import kernel_function

# === Class Definition ===
class ToolsPlugin:
    """
    General utility functions for use as kernel plugins.
    """

    # === Methods ===
    @kernel_function(
        description="Adds two integers.",
        name="add_numbers",
    )
    def add_numbers(self, a: int, b: int) -> int:
        """
        Adds two integers and prints the operation.

        Args:
            a (int): The first integer.
            b (int): The second integer.

        Returns:
            int: The sum of a and b.
        """
        print(f"This Message is called within the function add_numbers with a:{a} and b:{b}")  # Log the operation for debugging
        return a + b
