class UnzipPrompt:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"zipped_prompt": ("ZIPPED_PROMPT",), }}

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("positive", "negative", "name")

    FUNCTION = "doit"

    CATEGORY = "InspirePack/Prompt"

    def doit(self, zipped_prompt):
        return zipped_prompt


class LoadPromptsFromFile:
    @classmethod
    def INPUT_TYPES(cls):
        prompt_files = []
        try:
            prompts_paths = folder_paths.get_folder_paths('inspire_prompts')
            for prompts_path in prompts_paths:
                for root, dirs, files in os.walk(prompts_path):
                    for file in files:
                        if file.endswith(".txt"):
                            file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(file_path, prompts_path)
                            prompt_files.append(rel_path)
        except Exception:
            prompt_files = []

        return {"required": {
                        "prompt_file": (prompt_files,)
                        },
                "optional": {
                        "text_data_opt": ("STRING", {"defaultInput": True}),
                        "reload": ("BOOLEAN", {"default": False, "label_on": "if file changed", "label_off": "if value changed"}),
                        "load_cap": ("INT", {"default": 0, "min": 0, "step": 1, "advanced": True, "tooltip": "The amount of prompts to load at once:\n0: Load all\n1 or higher: Load a specified number"}),
                        "start_index": ("INT", {"default": 0, "min": -1, "max": 0xffffffffffffffff, "step": 1, "advanced": True, "tooltip": "Starting index for loading prompts:\n-1: The last prompt\n0 or higher: Load from the specified index"}),
                        }
                }

    RETURN_TYPES = ("ZIPPED_PROMPT", "INT", "INT")
    RETURN_NAMES = ("zipped_prompt", "count", "remaining_count")
    OUTPUT_IS_LIST = (True, False, False)

    FUNCTION = "doit"

    CATEGORY = "InspirePack/Prompt"

    @staticmethod
    def IS_CHANGED(prompt_file, text_data_opt=None, reload=False, load_cap=0, start_index=-1):
        md5 = hashlib.md5()

        if text_data_opt is not None:
            md5.update(text_data_opt)
            return md5.hexdigest(), load_cap, start_index
        elif not reload:
            return prompt_file, load_cap, start_index
        else:
            matched_path = None
            for x in folder_paths.get_folder_paths('inspire_prompts'):
                matched_path = os.path.join(x, prompt_file)
                if not os.path.exists(matched_path):
                    matched_path = None
                else:
                    break

            if matched_path is None:
                return float('NaN')

            with open(matched_path, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    md5.update(chunk)

            return md5.hexdigest(), load_cap, start_index

    @staticmethod
    def doit(prompt_file, text_data_opt=None, reload=False, load_cap=0, start_index=-1):
        matched_path = None
        for d in folder_paths.get_folder_paths('inspire_prompts'):
            matched_path = os.path.join(d, prompt_file)
            if os.path.exists(matched_path):
                break
            else:
                matched_path = None

        if matched_path:
            logging.info(f"[Inspire Pack] LoadPromptsFromFile: file found '{prompt_file}'")
        else:
            logging.warning(f"[Inspire Pack] LoadPromptsFromFile: file not found '{prompt_file}'")

        prompts = []
        try:
            if not text_data_opt:
                with open(matched_path, "r", encoding="utf-8") as file:
                    prompt_data = file.read()
            else:
                prompt_data = text_data_opt

            prompt_list = re.split(r'\n\s*-+\s*\n', prompt_data)

            pattern = r"^(?:(?:positive:(?P<positive>.*?)|negative:(?P<negative>.*?)|name:(?P<name>.*?))\n*)+$"

            for p in prompt_list:
                matches = re.search(pattern, p, re.DOTALL)

                if matches:
                    positive_text = matches.group('positive').strip()
                    negative_text = matches.group('negative').strip()
                    name_text = matches.group('name').strip() if matches.group('name') else prompt_file
                    result_tuple = (positive_text, negative_text, name_text)
                    prompts.append(result_tuple)
                else:
                    logging.warning(f"[Inspire Pack] LoadPromptsFromFile: invalid prompt format in '{prompt_file}'")
        except Exception as e:
            logging.error(f"[Inspire Pack] LoadPromptsFromFile: an error occurred while processing '{prompt_file}': {str(e)}\nNOTE: Only files with UTF-8 encoding are supported.")

        # slicing [start_index ~ start_index + load_cap]
        total_prompts = len(prompts)
        prompts = prompts[start_index:]
        remaining_count = 0
        if load_cap > 0:
            remaining_count = max(0, len(prompts) - load_cap)
            prompts = prompts[:load_cap]

        return prompts, total_prompts, remaining_count