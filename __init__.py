from .ixiworks_nodes import *

NODE_CLASS_MAPPINGS = {
    "JsonParserNode": JsonParserNode,
    "BuildPromptNode": BuildPromptNode,
    "BuildCharacterPromptNode": BuildCharacterPromptNode,
    "SelectIndexNode": SelectIndexNode,
    "MergeStringsNode": MergeStringsNode,
}
__all__ = ["JsonParserNode", "BuildPromptNode", "BuildCharacterPromptNode", "SelectIndexNode", "MergeStringsNode"]  