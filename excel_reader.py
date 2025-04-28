import pandas as pd

class ExcelReaderNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"excel_file": ("FILE",)},
        }
    
    RETURN_TYPES = ("STRING",)    
    FUNCTION = "read_excel"
    CATEGORY = "custom_nodes"
    
    def read_excel(self, excel_file):
        df = pd.read_excel(excel_file)
        first_column = df.iloc[:, 0].tolist()   
        return (first_column, )
    
NODE_CLASS_MAPPINGS = {
    "ExcelReaderNode": ExcelReaderNode,
}
    
    