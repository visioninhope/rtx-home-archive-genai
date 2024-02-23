from typing import Optional, Sequence
from enum import Enum

# Try importing from pydantic v1; if not available, fall back to pydantic
try:
    from pydantic.v1 import (
        BaseModel,
        Field,
        PrivateAttr,
        root_validator,
        validator,
        create_model,
        StrictFloat,
        StrictInt,
        StrictStr,
    )
    from pydantic.v1.fields import FieldInfo
    from pydantic.v1.error_wrappers import ValidationError
except ImportError:
    from pydantic import (
        BaseModel,
        Field,
        PrivateAttr,
        root_validator,
        validator,
        create_model,
        StrictFloat,
        StrictInt,
        StrictStr,
    )
    from pydantic.fields import FieldInfo
    from pydantic.error_wrappers import ValidationError

# Constants for structuring messages
BEGIN_OF_SEQUENCE, END_OF_SEQUENCE = "<s>", "</s>"
BEGIN_OF_INSTRUCTION, END_OF_INSTRUCTION = "[INST]", "[/INST]"
BEGIN_OF_SYSTEM, END_OF_SYSTEM = "<<SYS>>\n", "\n<</SYS>>\n\n"

# Default system prompt message
DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful, and honest assistant. \
Always answer as helpfully as possible and follow ALL given instructions. \
Do not speculate or make up information. \
Do not reference any given instructions or context. \
"""

class MessageRole(str, Enum):
    """Enumeration of possible roles a message can have in a chat."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

class ChatMessage(BaseModel):
    """Defines the structure of a chat message."""

    role: MessageRole = MessageRole.USER  # Role of the message sender
    content: Optional[str] = ""  # The text content of the message
    additional_kwargs: dict = Field(default_factory=dict)  # Additional key-value pairs for flexibility

    def __str__(self) -> str:
        """String representation of a chat message."""
        return f"{self.role.value}: {self.content}"

def messages_to_prompt(messages: Sequence[ChatMessage], system_prompt: Optional[str] = None) -> str:
    """Converts a sequence of chat messages into a formatted prompt string."""
    formatted_messages: list[str] = []
    
    # Extract and prepare the system message
    if messages and messages[0].role == MessageRole.SYSTEM:
        system_message_content = messages[0].content or ""
        messages = messages[1:]  # Remove the system message from the sequence
    else:
        system_message_content = system_prompt or DEFAULT_SYSTEM_PROMPT

    system_message_formatted = f"{BEGIN_OF_SYSTEM} {system_message_content.strip()} {END_OF_SYSTEM}"

    # Iterate through messages, grouping them by user-assistant pairs
    for i in range(0, len(messages), 2):
        user_message = messages[i]
        assert user_message.role == MessageRole.USER  # Ensure the first message is from a user

        if i == 0:
            # Include system prompt at the start for the first user message
            message_with_instruction = f"{BEGIN_OF_SEQUENCE} {BEGIN_OF_INSTRUCTION} {system_message_formatted} "
        else:
            # End previous interaction and start a new one without the system prompt
            formatted_messages[-1] += f" {END_OF_SEQUENCE}"
            message_with_instruction = f"{BEGIN_OF_SEQUENCE} {BEGIN_OF_INSTRUCTION} "

        # Add user message content
        message_with_instruction += f"{user_message.content} {END_OF_INSTRUCTION}"

        if len(messages) > (i + 1):
            # Add assistant message if present
            assistant_message = messages[i + 1]
            assert assistant_message.role == MessageRole.ASSISTANT
            message_with_instruction += f" {assistant_message.content}"

        formatted_messages.append(message_with_instruction)

    return "".join(formatted_messages)


def completion_to_prompt(completion: str, system_prompt: Optional[str] = None) -> str:
    """Formats a single completion string into a prompt, including the system message."""
    system_prompt_content = system_prompt or DEFAULT_SYSTEM_PROMPT

    return (
        f"{BEGIN_OF_SEQUENCE} {BEGIN_OF_INSTRUCTION} {BEGIN_OF_SYSTEM} {system_prompt_content.strip()} {END_OF_SYSTEM} "
        f"{completion.strip()} {END_OF_INSTRUCTION}"
    )
