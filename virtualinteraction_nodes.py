class TextParserNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"text_file": ("STRING", {"default": "/path/to/your/file.txt"})},
        }
    
    RETURN_TYPES = ("ZIPPED_PROMPT", "INT", "INT")    
    RETURN_NAMES = ("zipped_prompt", "count", "remaining_count")
    FUNCTION = "parse_text"
    CATEGORY = "StoryBoard"
    
    def parse_text(self, text_file):
        try:
            with open(text_file, 'r', encoding='utf-8') as file:
                content = file.read()
            sections = content.split("---")
            sections = [s.strip() for s in sections if s.strip()]
            
            # Create a list of tuples with the required fields
            result = []
            for i in range(len(sections)):
                scene_desc = sections[i] if i == 0 else ""
                time_weather = sections[i] if i == 1 else ""
                camera_shot = sections[i] if i == 2 else ""
                composition = sections[i] if i == 3 else ""
                result.append((scene_desc, time_weather, camera_shot, composition))
            
            return (result, len(result), len(result))
        except Exception as e:
            print(f"Error reading file: {e}")
            return ([("", "", "", "")], 0, 0)

class UnzipPromptNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"zipped_prompt": ("ZIPPED_PROMPT",), }}

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("scene_description", "time_and_weather", "camera_shot", "composition")

    FUNCTION = "unzip_prompt"

    CATEGORY = "StoryBoard"

    def unzip_prompt(self, zipped_prompt):
        if zipped_prompt and len(zipped_prompt) > 0:
            # Assuming zipped_prompt is a list of tuples with 4 elements
            item = zipped_prompt[0]
            return (item[0], item[1], item[2], item[3])
        else:
            return ("", "", "", "")

NODE_CLASS_MAPPINGS.update({
    "TextParserNode": TextParserNode,
    "UnzipPromptNode": UnzipPromptNode,
})