from pydantic import BaseModel

# Json example:
# {
#   "id": "chatcmpl-72vFmS5elunBEaM84veuLybD8mtau",
#   "object": "chat.completion",
#   "created": 1680931094,
#   "model": "gpt-35-turbo",
#   "choices": [
#     {
#       "index": 0,
#       "finish_reason": "stop",
#       "message": {
#         "role": "assistant",
#         "content": "Hola mundo, ¿cómo se encuentra hoy?"
#       }
#     }
#   ],
#   "usage": {
#     "completion_tokens": 12,
#     "prompt_tokens": 35,
#     "total_tokens": 47
#   }
# }

class OPENAICompletionResponseChoiceMessage(BaseModel):
    """
    OPENAI response model
    """
    role: str
    content: str

class OPENAICompletionResponseChoice(BaseModel):
    """
    OPENAI response model
    """
    index: int
    finish_reason: str | None = None
    message: OPENAICompletionResponseChoiceMessage | None = None

class OPENAICompletionResponseUsage(BaseModel):
    """
    OPENAI response model
    """
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

class OPENAICompletionResponse(BaseModel):
    """
    OPENAI response model
    """
    id: str
    object: str
    created: int
    model: str
    choices: list[OPENAICompletionResponseChoice] = list()
    usage: OPENAICompletionResponseUsage | None = None