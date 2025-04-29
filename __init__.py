from .virtualinteraction_nodes import TextParserNode, UnzipPromptNode, JoinPromptNode

NODE_CLASS_MAPPINGS = {
    "TextParserNode": TextParserNode,
    "UnzipPromptNode": UnzipPromptNode,
    "JoinPromptNode": JoinPromptNode,
}
__all__ = ["TextParserNode", "UnzipPromptNode", "JoinPromptNode"]