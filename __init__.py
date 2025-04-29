from .text_parser import TextParserNode
from .unzip_prompt import UnzipPromptNode

NODE_CLASS_MAPPINGS = {
    "TextParserNode": TextParserNode,
    "UnzipPromptNode": UnzipPromptNode,
}
__all__ = ["TextParserNode", "UnzipPromptNode"]