# ComfyUI-IxiWorks

StoryBoard nodes for ComfyUI - Parse JSON templates and build prompts for generative movie creation.

## Features

This custom node pack helps you create consistent storyboard prompts from structured JSON templates. Perfect for generating scenes with consistent characters across multiple frames.

## Nodes

### JsonParserNode
- Parses JSON files containing scene and character information
- Outputs structured data for prompt building
- Supports the new storyboard JSON format with multilingual support

### BuildPromptNode
- Converts scene tuples into formatted prompt strings
- Combines description, time/weather, camera info, and composition details

### BuildCharacterPromptNode
- Converts character information into natural language descriptions
- Formats: "Somyung is a teenage girl..." instead of "Somyung: teenage girl"

### SelectIndexNode
- Selects a specific scene or character from the parsed arrays
- Useful for processing individual scenes

### MergeStringsNode
- Merges two string arrays element by element
- Perfect for combining character descriptions with scene prompts
- Supports custom separators

## Installation

1. Clone this repository into your ComfyUI custom_nodes folder:
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Jpzz/comfyui-ixiworks.git
```

2. Restart ComfyUI

## Usage

1. Place your JSON template file in the `ComfyUI/input/prompt/` directory
2. Create a workflow:
   - JsonParserNode → Load your JSON file
   - BuildPromptNode → Convert scenes to prompts
   - BuildCharacterPromptNode → Convert characters to descriptions
   - MergeStringsNode → Combine character + scene prompts
   - Connect to CLIP Text Encode for batch processing

## JSON Template Format

```json
{
  "scene": {
    "1": {
      "title": {"en": "Scene Title"},
      "m_character": {
        "en_name": "MainChar",
        "description": "Character description"
      },
      "s_character": {
        "en_name": "SubChar", 
        "description": "Character description"
      },
      "time": {"en": "5:00 PM"},
      "weather": {"en": "Clear"},
      "camera_shot": {"en": "Close-up"},
      "camera_movement": {"en": "Pan"},
      "description": {"en": "Scene description"},
      "detailed_script": {"en": "Camera directions"},
      "negative_prompt": {"en": "Things to avoid"}
    }
  }
}
```

## Example Output

Input scenes are converted to prompts like:
```
Somyung is a teenage girl with long brown hair. Robu is a humanoid robot. 
The scene shows Somyung infiltrating a facility... 5:00 PM, Clear. 
Close-up, Pan. Camera positioned on the right...
```

## License

MIT License - see LICENSE file for details

## Author

IxiWorks

## Contributing

Pull requests are welcome! Please feel free to submit issues or feature requests.