"""
chat/user_input.py

Handles user input and returns chat message content for the orchestration system.
"""

# === Imports ===
from semantic_kernel.contents import ChatMessageContent, AuthorRole

# === Functions ===
def human_response_function() -> ChatMessageContent:
    """
    Prompts the user for input and returns a ChatMessageContent object.

    Returns:
        ChatMessageContent: The user's input wrapped as a chat message.

    Raises:
        Exception: If input or message creation fails.
    """
    try:
        # Prompt the user for input
        user_input = input("User: ")
        # Wrap the input as a chat message content object
        return ChatMessageContent(role=AuthorRole.USER, content=user_input)
    except Exception as e:
        # Log and re-raise any errors during user input handling
        print(f"[UserInput] Error getting user input: {e}")
        raise
