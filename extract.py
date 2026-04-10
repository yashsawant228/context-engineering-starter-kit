import os
import re

VALID_EXTENSIONS = {
    '.py', '.yml', '.yaml', '.md', '.txt', '.toml', '.cfg', '.env',
    '.json', '.sh', '.gitignore', '.example'
}

def is_valid_filepath(path: str) -> bool:
    """Validate that a captured string is a real file path, not instruction text."""
    # Must be short (real paths rarely exceed 120 chars)
    if len(path) > 120:
        return False
    # Must not contain spaces (instruction text always has spaces)
    if ' ' in path:
        return False
    # Must not contain newlines
    if '\n' in path:
        return False
    # Must have a recognisable file extension OR be .gitignore / .env style
    _, ext = os.path.splitext(path)
    base = os.path.basename(path)
    if ext.lower() in VALID_EXTENSIONS:
        return True
    # Allow dotfiles like .env, .gitignore, .env.example
    if base.startswith('.') and '.' in base[1:]:
        return True
    if base in {'.gitignore', '.env', '.env.example'}:
        return True
    return False

def extract_from_file(filename: str):
    if not os.path.exists(filename):
        print(f"Skipping '{filename}' — file not found.")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    # Match <file_path>...</file_path> immediately followed by a fenced code block
    pattern = r'<file_path>(.*?)</file_path>\s*```[\w\-]*\n(.*?)```'
    matches = re.finditer(pattern, text, re.DOTALL)

    count = 0
    skipped = 0
    for match in matches:
        filepath = match.group(1).strip()
        code = match.group(2)

        # Skip invalid paths (catches the example/instruction text)
        if not is_valid_filepath(filepath):
            print(f"  ⚠ Skipped invalid path: '{filepath[:60]}...'")
            skipped += 1
            continue

        # Create all necessary parent directories
        parent = os.path.dirname(filepath)
        if parent:
            os.makedirs(parent, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as out:
            out.write(code)

        print(f"  ✓ Created: {filepath}")
        count += 1

    print(f"\nDone — {count} file(s) extracted, {skipped} invalid path(s) skipped.")

if __name__ == "__main__":
    print("Starting extraction from improvements.md ...\n")
    extract_from_file('improvements.md')