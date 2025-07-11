from semantic_kernel.functions import kernel_function

class ToolsPlugin:
    """Allgemeine Hilfsfunktionen."""

    @kernel_function(
        description="Addiert zwei ganze Zahlen.",
        name="add_numbers",
    )
    def add_numbers(self, a: int, b: int) -> int:
        print(f"Adding {a} and {b}")
        """Addiert zwei ganze Zahlen."""
        return a + b