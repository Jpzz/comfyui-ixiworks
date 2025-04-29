import os
import logging
import json

class JsonParserNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"file_name": ("STRING", {"default": "prompt.json"})},
        }
    
    RETURN_TYPES = ("ZIPPED_PROMPT", "INT", "INT")    
    RETURN_NAMES = ("zipped_prompt", "count", "remaining_count")
    FUNCTION = "parse_text"
    CATEGORY = "StoryBoard"
    
    def parse_text(self, file_name):
        file_path = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "input", "prompt", file_name)))
        logging.info(f"[StoryBoard] JsonParserNode: file path '{file_path}'")
        try:
            # Load the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Process the JSON data
            result = []
            for key, item in data.items():  
                if isinstance(item, dict):
                    scene_desc = item.get("scene_description", "")
                    time_weather = item.get("time_and_weather", "")
                    camera_shot = item.get("camera_shot", "")
                    composition = item.get("composition", "")
                    result.append((scene_desc, time_weather, camera_shot, composition))
            
            return (result, len(result), len(result))
        except Exception as e:
            print(f"Error reading file: {e}")
            return ([("", "", "", "")], 0, 0)

class UnzipPromptNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"zipped_prompt": ("ZIPPED_PROMPT",), }}

    RETURN_TYPES = ("STRING_LIST", "STRING_LIST", "STRING_LIST", "STRING_LIST")
    RETURN_NAMES = ("descriptions", "time_and_weathers", "camera_shots", "compositions")

    FUNCTION = "unzip_prompt"

    CATEGORY = "StoryBoard"

    def unzip_prompt(self, zipped_prompt):
        if zipped_prompt and len(zipped_prompt) > 0:
            # Extract each category into separate lists
            scene_desc_list = [item[0] for item in zipped_prompt]
            time_weather_list = [item[1] for item in zipped_prompt]
            camera_shot_list = [item[2] for item in zipped_prompt]
            composition_list = [item[3] for item in zipped_prompt]
            return (scene_desc_list, time_weather_list, camera_shot_list, composition_list)
        else:
            return ([], [], [], [])

class JoinPromptNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"descriptions": ("STRING_LIST",), "time_and_weathers": ("STRING_LIST",), "camera_shots": ("STRING_LIST",), "compositions": ("STRING_LIST",), }}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "join_prompt"
    CATEGORY = "StoryBoard"

    def join_prompt(self, descriptions, time_and_weathers, camera_shots, compositions):
        prompts = []
        for i in range(len(descriptions)):
            prompts.append(descriptions[i] + time_and_weathers[i] + camera_shots[i] + compositions[i])
        return (prompts,)

# Initialize NODE_CLASS_MAPPINGS if not already defined
if 'NODE_CLASS_MAPPINGS' not in globals():
    NODE_CLASS_MAPPINGS = {}

NODE_CLASS_MAPPINGS.update({
    "JsonParserNode": JsonParserNode,
    "UnzipPromptNode": UnzipPromptNode,
    "JoinPromptNode": JoinPromptNode,
})
