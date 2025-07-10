"""
chat/callbacks.py

Contains callback functions for handling streaming agent responses and chat message processing.
"""

from semantic_kernel.contents import StreamingChatMessageContent, FunctionCallContent, FunctionResultContent

_is_new_message = True  # Internal flag for message state

def streaming_agent_response_callback(message: StreamingChatMessageContent, is_final: bool) -> None:
    """
    Observer function to print the messages from the agents.

    This function is called whenever the agent generates a response,
    including internal processing messages (such as tool calls) that are not visible
    to other agents in the orchestration.

    In streaming mode, the FunctionCallContent and FunctionResultContent are provided as a
    complete message.

    Args:
        message (StreamingChatMessageContent): The streaming message content from the agent.
        is_final (bool): Indicates if this is the final part of the message.
    """
    global _is_new_message
    try:
        if _is_new_message:
            print(f"{message.name}: ", end="", flush=True)
            _is_new_message = False
        print(message.content, end="", flush=True)

        for item in message.items:
            if isinstance(item, FunctionCallContent):
                print(f"Calling '{item.name}' with arguments '{item.arguments}'", end="", flush=True)
            if isinstance(item, FunctionResultContent):
                print(f"Result from '{item.name}' is '{item.result}'", end="", flush=True)

        if is_final:
            print()
            _is_new_message = True
    except Exception as e:
        print(f"[Chat] Error in streaming_agent_response_callback: {e}")
