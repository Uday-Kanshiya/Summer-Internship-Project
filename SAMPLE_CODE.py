SAMPLE_CODE = '''
import os
import json
from pathlib import Path
from typing import List, Optional

class FileProcessor:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.files = []

    def load_files(self, extension: str = ".txt") -> List[str]:
        result = []
        for fname in os.listdir(self.base_dir):
            if fname.endswith(extension):
                result.append(fname)
        self.files = result
        return result

    def read_file(self, filename: str) -> Optional[str]:
        path = Path(self.base_dir) / filename
        if path.exists():
            return path.read_text()
        return None


class DataParser:
    def __init__(self):
        self.processor = FileProcessor("/data")

    def parse_json(self, filename: str) -> dict:
        content = self.processor.read_file(filename)
        if content:
            return json.loads(content)
        return {}

    def batch_parse(self, extension: str = ".json") -> List[dict]:
        files = self.processor.load_files(extension)
        results = []
        for f in files:
            results.append(self.parse_json(f))
        return results


def summarize_results(data: List[dict]) -> str:
    return f"Processed {len(data)} records."


def main():
    parser = DataParser()
    results = parser.batch_parse()
    print(summarize_results(results))


if __name__ == "__main__":
    main()
'''
print(f"Sample code loaded: {len(SAMPLE_CODE.splitlines())} lines")