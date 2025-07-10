"""
chat/user_input.py

Handles user input and returns chat message content for the orchestration system.
"""

from semantic_kernel.contents import ChatMessageContent, AuthorRole

def human_response_function() -> ChatMessageContent:
    """
    Prompts the user for input and returns a ChatMessageContent object.

    Returns:
        ChatMessageContent: The user's input wrapped as a chat message.

    Raises:
        Exception: If input or message creation fails.
    """
    try:
        user_input = input("User: ")
        return ChatMessageContent(role=AuthorRole.USER, content=user_input)
    except Exception as e:
        print(f"[UserInput] Error getting user input: {e}")
        raise
