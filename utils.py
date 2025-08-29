import csv
from collections import defaultdict
from pathlib import Path

def build_category_tree(csv_path: str):
    tree = lambda: defaultdict(tree)
    root = tree()

    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            path_parts = row["category_path"].split("/")
            current = root
            for part in path_parts:
                current = current[part]  # walk down or create new

    return root
