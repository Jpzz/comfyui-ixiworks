from .virtualinteraction_nodes import TextParserNode, UnzipPromptNode

NODE_CLASS_MAPPINGS = {
    "TextParserNode": TextParserNode,
    "UnzipPromptNode": UnzipPromptNode,
}
__all__ = ["TextParserNode", "UnzipPromptNode"]