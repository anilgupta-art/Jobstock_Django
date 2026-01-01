import json
from types import SimpleNamespace



def dict_to_namespace(d):
    """Convert dictionary to object with dot notation access"""
    if isinstance(d, dict):
        return SimpleNamespace(**{k: dict_to_namespace(v) for k, v in d.items()})
    elif isinstance(d, list):
        return [dict_to_namespace(i) for i in d]
    else:
        return d

def file_to_json(filepath):
    """Convert dictionary to object with dot notation access"""    
    with open(filepath, 'r') as file:
        config_dict = json.load(file)
    config = dict_to_namespace(config_dict)
    return config



# with open(filepath, 'r') as file:
#     config_dict = json.load(file)

# config = dict_to_namespace(config_dict)

# # Access using dot notation
# print(f"Data file: {config.UserImport.FileUpload.data_file}")
# print(f"Mapping file: {config.UserImport.FileUpload.mapping_file}")
# print(f"Default role: {config.UserImport.default_values.role_id}")
# print(f"Case sensitive: {config.UserImport.case_sensitive}")