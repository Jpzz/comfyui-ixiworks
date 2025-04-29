from .virtualinteraction_nodes import JsonParserNode, UnzipPromptNode, JoinPromptNode

NODE_CLASS_MAPPINGS = {
    "JsonParserNode": JsonParserNode,
    "UnzipPromptNode": UnzipPromptNode,
    "JoinPromptNode": JoinPromptNode,
}
__all__ = ["JsonParserNode", "UnzipPromptNode", "JoinPromptNode"]