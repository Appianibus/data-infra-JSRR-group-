#write a python class that read a json file and clean it
import json

class JSONReader:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.data = self._read_json()

    def _read_json(self):
        try:
            with open(self.input_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {self.input_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def get_data(self):
        """Return the loaded JSON data."""
        return self.data
    
    def _clean_data(self, obj):
        """
        Recursively remove keys with null values from dictionaries and
        remove nulls from lists.
        """
        if isinstance(obj, dict):
            return {k: self._clean_data(v) for k, v in obj.items() if v is not None}
        elif isinstance(obj, list):
            return [self._clean_data(item) for item in obj if item is not None]
        else:
            return obj

    def clean(self):
        """Clean the loaded JSON data by removing null values."""
        if self.data is not None:
            self.data = self._clean_data(self.data)
            print("JSON data cleaned (nulls removed).")
        else:
            print("No data to clean.")
        return self  # allows method chaining
    
    def save(self):
        """Save the (possibly cleaned) JSON data to the output file."""
        if self.data is None:
            print("No data to save.")
            return
        try:
            with open(self.output_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=4, ensure_ascii=False)
            print(f"Cleaned JSON saved to: {self.output_path}")
        except Exception as e:
            print(f"Failed to save file: {e}")