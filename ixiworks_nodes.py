import os
import logging
import json

class JsonParserNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"file_name": ("STRING", {"default": "prompt.json"})},
        }
    
    RETURN_TYPES = ("ZIPPED_PROMPT", "ZIPPED_PROMPT", "INT")    
    RETURN_NAMES = ("zipped_prompt", "zipped_character", "count")
    FUNCTION = "parse_text"
    CATEGORY = "StoryBoard"
    OUTPUT_IS_LIST = (True, True, False)
    
    def parse_text(self, file_name):
        file_path = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "input", "prompt", file_name)))
        logging.info(f"[StoryBoard] JsonParserNode: file path '{file_path}'")
        try:
            # Load the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            scene_data = data.get('scene', {})
            
            # Process the JSON data - new format only
            result = []
            character_result = []
            
            # New format - extract English fields only
            for item in scene_data.values():
                if isinstance(item, dict):
                    # Extract scene information (English only)
                    time = item.get("time", {}).get("en", "")
                    weather = item.get("weather", {}).get("en", "")
                    camera_shot = item.get("camera_shot", {}).get("en", "")
                    camera_movement = item.get("camera_movement", {}).get("en", "")
                    description = item.get("description", {}).get("en", "")
                    detailed_script = item.get("detailed_script", {}).get("en", "")
                    negative_prompt = item.get("negative_prompt", {}).get("en", "")
                    
                    # Combine camera shot and movement
                    camera_info = f"{camera_shot}, {camera_movement}" if camera_movement else camera_shot
                    
                    # Combine time and weather
                    time_weather = f"{time}, {weather}" if time and weather else f"{time}{weather}"
                    
                    # Use detailed_script as composition, combine description with negative prompt
                    full_description = f"{description} Negative: {negative_prompt}" if negative_prompt else description
                    
                    result.append((full_description, time_weather, camera_info, detailed_script))
                    
                    # Extract character information for each scene
                    m_char = item.get("m_character", {})
                    s_char = item.get("s_character", {})
                    
                    main_char_ko_name = m_char.get("ko_name", "")
                    main_char_en_name = m_char.get("en_name", "")
                    main_char_desc = m_char.get("description", "")
                    
                    sub_char_ko_name = s_char.get("ko_name", "")
                    sub_char_en_name = s_char.get("en_name", "")
                    sub_char_desc = s_char.get("description", "")
                    
                    character_result.append((main_char_ko_name, main_char_en_name, sub_char_ko_name, sub_char_en_name, main_char_desc, sub_char_desc))
            
            return (result, character_result, len(result))
        except Exception as e:
            logging.error(f"[StoryBoard] JsonParserNode: Error reading file: {e}")
            return ([("", "", "", "")], [("", "", "", "", "", "")], 0)


class BuildCharacterPromptNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"zipped_character": ("ZIPPED_PROMPT",),}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("character_prompt",)
    FUNCTION = "build_character_prompt"
    CATEGORY = "StoryBoard"
    OUTPUT_IS_LIST = (True,)

    def build_character_prompt(self, zipped_character):
        character_prompts = []
        logging.info(f"[StoryBoard] BuildCharacterPromptNode: Processing {len(zipped_character)} character sets")
        
        for idx, char_data in enumerate(zipped_character):
            if isinstance(char_data, tuple) and len(char_data) >= 6:
                main_char_en_name = char_data[1]
                sub_char_en_name = char_data[3]
                main_char_desc = char_data[4]
                sub_char_desc = char_data[5]
                
                # Build natural language character descriptions
                char_descriptions = []
                
                if main_char_en_name and main_char_desc:
                    # Convert description to natural sentence
                    desc = main_char_desc.lower()
                    if desc.startswith("a ") or desc.startswith("an "):
                        char_descriptions.append(f"{main_char_en_name} is {desc}")
                    elif desc.startswith("female") or desc.startswith("male"):
                        char_descriptions.append(f"{main_char_en_name} is a {desc}")
                    else:
                        char_descriptions.append(f"{main_char_en_name} is {desc}")
                
                if sub_char_en_name and sub_char_desc:
                    # Convert description to natural sentence
                    desc = sub_char_desc.lower()
                    if desc.startswith("a ") or desc.startswith("an "):
                        char_descriptions.append(f"{sub_char_en_name} is {desc}")
                    elif desc.startswith("humanoid") or desc.startswith("robot"):
                        char_descriptions.append(f"{sub_char_en_name} is a {desc}")
                    else:
                        char_descriptions.append(f"{sub_char_en_name} is {desc}")
                
                # Join character descriptions
                character_prompt = ". ".join(char_descriptions) + "." if char_descriptions else ""
                character_prompts.append(character_prompt)
                
                logging.info(f"[StoryBoard] BuildCharacterPromptNode: Built character prompt {idx+1}")
        
        return (character_prompts,)


class BuildPromptNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"zipped_prompt": ("ZIPPED_PROMPT",),}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build_prompt"
    CATEGORY = "StoryBoard"
    OUTPUT_IS_LIST = (True,)

    def build_prompt(self, zipped_prompt):
        prompts = []
        logging.info(f"[StoryBoard] BuildPromptNode: Processing {len(zipped_prompt)} scenes")
        
        # Handle both list of tuples and single tuple
        if isinstance(zipped_prompt, tuple) and len(zipped_prompt) == 4 and all(isinstance(x, str) for x in zipped_prompt):
            # Single tuple case (from SelectIndexNode)
            zipped_prompt = [zipped_prompt]
        
        for idx, item in enumerate(zipped_prompt):
            if isinstance(item, tuple) and len(item) >= 4:
                full_description = item[0]
                time_weather = item[1] 
                camera_info = item[2]
                detailed_script = item[3]
                
                # Build the prompt by combining all fields
                combined_prompt = f"{full_description} {time_weather} {camera_info} {detailed_script}"
                
                # Clean up multiple spaces
                combined_prompt = " ".join(combined_prompt.split())
                
                prompts.append(combined_prompt)
                logging.info(f"[StoryBoard] BuildPromptNode: Built prompt for scene {idx+1}")
        
        logging.info(f"[StoryBoard] BuildPromptNode: Generated {len(prompts)} prompts")
        return (prompts,)

class SelectIndexNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "zipped_prompt": ("ZIPPED_PROMPT",),
                "index": ("INT", {"default": 0, "min": 0, "max": 100}),
            }
        }
    
    RETURN_TYPES = ("ZIPPED_PROMPT",)
    RETURN_NAMES = ("selected_prompt",)
    FUNCTION = "select_index"
    CATEGORY = "StoryBoard"
    OUTPUT_IS_LIST = (False,)
    
    def select_index(self, zipped_prompt, index):
        logging.info(f"[StoryBoard] SelectIndexNode: Selecting index {index} from {len(zipped_prompt)} items")
        
        if index < 0 or index >= len(zipped_prompt):
            logging.error(f"[StoryBoard] SelectIndexNode: Index {index} out of range (0-{len(zipped_prompt)-1})")
            # Return empty tuple if index is out of range
            return (("", "", "", ""),)
        
        selected = zipped_prompt[index]
        logging.info(f"[StoryBoard] SelectIndexNode: Selected item at index {index}")
        
        return (selected,)

class MergeStringsNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "strings_a": ("STRING",),
                "strings_b": ("STRING",),
            },
            "optional": {
                "separator": ("STRING", {"default": " "}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_strings",)
    FUNCTION = "merge_strings"
    CATEGORY = "StoryBoard"
    OUTPUT_IS_LIST = (True,)
    
    def merge_strings(self, strings_a, strings_b, separator=" "):
        # Ensure inputs are lists
        if not isinstance(strings_a, list):
            strings_a = [strings_a]
        if not isinstance(strings_b, list):
            strings_b = [strings_b]
            
        merged_strings = []
        
        # Check if arrays have same length
        if len(strings_a) != len(strings_b):
            logging.warning(f"[StoryBoard] MergeStringsNode: Array lengths don't match. strings_a: {len(strings_a)}, strings_b: {len(strings_b)}")
            # Use the shorter length
            min_length = min(len(strings_a), len(strings_b))
        else:
            min_length = len(strings_a)
            
        logging.info(f"[StoryBoard] MergeStringsNode: Merging {min_length} string pairs")
        
        for i in range(min_length):
            # Merge with separator
            merged = f"{strings_a[i]}{separator}{strings_b[i]}"
            
            # Clean up multiple spaces if separator is space
            if separator == " ":
                merged = " ".join(merged.split())
                
            merged_strings.append(merged)
            
        return (merged_strings,)


# Initialize NODE_CLASS_MAPPINGS if not already defined
if 'NODE_CLASS_MAPPINGS' not in globals():
    NODE_CLASS_MAPPINGS = {}

NODE_CLASS_MAPPINGS.update({
    "JsonParserNode": JsonParserNode,
    "BuildPromptNode": BuildPromptNode,
    "BuildCharacterPromptNode": BuildCharacterPromptNode,
    "SelectIndexNode": SelectIndexNode,
    "MergeStringsNode": MergeStringsNode,
})
