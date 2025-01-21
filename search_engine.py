import os
import re
from collections import defaultdict

class SearchEngine:
    def __init__(self):
        # Inverted index: {word: [{'dir': ..., 'file': ..., 'line': ..., 'content': ...}, ...]}
        self.index = defaultdict(list)

    def crawl_directory(self, root_dir):
        """
        Recursively index all .txt files in the given directory.
        """
        for dirpath, _, filenames in os.walk(root_dir):
            for file in filenames:
                if file.endswith('.txt'):  # Index only .txt files
                    self.index_file(dirpath, file)

    def index_file(self, dirpath, filename):
        """
        Index the tokens of a file, adding them to the inverted index.
        """
        file_path = os.path.join(dirpath, filename)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_no, line in enumerate(f, start=1):
                tokens = self.tokenize(line)
                for token in tokens:
                    self.index[token].append({
                        'dir': dirpath,
                        'file': filename,
                        'line': line_no,
                        'content': line.strip()
                    })

    @staticmethod
    def tokenize(line):
        """
        Convert a line of text into lowercase tokens, removing non-alphanumeric characters.
        """
        line = re.sub(r'[^a-zA-Z0-9]', ' ', line).lower()
        return line.split()

    def search(self, query):
        """
        Search the index for occurrences of each token in the query.
        """
        tokens = self.tokenize(query)
        results = defaultdict(list)

        for token in tokens:
            if token in self.index:
                results[token].extend(self.index[token])

        return results


if __name__ == "__main__":
    # Example usage
    base_dir = "./test_dir"
    base_dir = "./complex_test_dir"  # Replace with your test directory path

    # Initialize search engine
    engine = SearchEngine()

    print(f"Indexing directory: {base_dir}...")
    engine.crawl_directory(base_dir)
    print("Indexing complete.")

    # Interactive search
    while True:
        query = input("> Enter your search query (or type 'exit' to quit): ")
        if query.strip().lower() == "exit":
            print("Exiting search engine. Goodbye!")
            break

        # Perform search
        results = engine.search(query)

        # Display results
        if not results:
            print("No results found.")
        else:
            for token, occurrences in results.items():
                print(f"Results for '{token}':")
                for occ in occurrences:
                    print(f"  {occ['dir']}/{occ['file']} (Line {occ['line']}): {occ['content']}")
