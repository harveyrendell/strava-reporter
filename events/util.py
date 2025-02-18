# Function to flatten a dict to single level dict
def flatten_dict(input_dict, parent_key='', separator='.'):
    flat_dict = {}

    def _flatten_dict(data, parent_key):
        for k, v in data.items():
            key = f"{parent_key}{separator}{k}" if parent_key else k
            if isinstance(v, dict):
                _flatten_dict(v, key)
            else:
                flat_dict[key] = v

    _flatten_dict(input_dict, parent_key)
    return flat_dict