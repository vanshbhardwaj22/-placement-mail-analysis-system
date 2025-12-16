import json

# Load the notebook
with open('phases/Phase 2/data_cleaning.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

print(f"Total cells: {len(notebook['cells'])}")

for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        print(f"\nCell {i}: {len(source)} chars")
        # Show first 100 chars
        print(f"  Start: {source[:100]}")
        if 'KNOWLEDGE_BASE' in source:
            print(f"  >>> Contains KNOWLEDGE_BASE")
        if 'REMOVE_PATTERNS' in source:
            print(f"  >>> Contains REMOVE_PATTERNS")
        if '__main__' in source:
            print(f"  >>> Contains __main__")
