import re
import sys
from pathlib import Path


ARGS_HEADER_RE = re.compile(r"^\s*Args:\s*$")
RETURNS_HEADER_RE = re.compile(r"^\s*Returns:\s*$")

ARG_RE = re.compile(
    r"^\s{4,}(\w+)\s*(?:\([^)]+\))?:\s*(.*)"
)

CONTINUATION_RE = re.compile(r"^\s{8,}(.*)")


def convert_google_to_sphinx(docstring: str) -> str:
    lines = docstring.splitlines()
    out = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # ---- Args ----
        if ARGS_HEADER_RE.match(line):
            i += 1
            while i < len(lines):
                match = ARG_RE.match(lines[i])
                if not match:
                    break

                name, desc = match.groups()
                full_desc = desc.strip()

                i += 1
                while i < len(lines):
                    cont = CONTINUATION_RE.match(lines[i])
                    if not cont:
                        break
                    full_desc += " " + cont.group(1).strip()
                    i += 1

                out.append(f":param {name}: {full_desc}")
            continue

        # ---- Returns ----
        if RETURNS_HEADER_RE.match(line):
            i += 1
            if i < len(lines) and lines[i].strip():
                out.append(f":return: {lines[i].strip()}")
                i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def process_file(path: Path):
    text = path.read_text(encoding="utf-8")

    docstring_re = re.compile(
        r'("""|\'\'\')([\s\S]*?)(\1)',
        re.MULTILINE
    )

    def replace(match):
        quote = match.group(1)
        body = match.group(2)
        converted = convert_google_to_sphinx(body)
        return f"{quote}{converted}{quote}"

    new_text = docstring_re.sub(replace, text)

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"Converted: {path}")


def process_folder(folder: Path):
    for py_file in folder.rglob("*.py"):
        process_file(py_file)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_docstrings.py <folder>")
        sys.exit(1)

    process_folder(Path(sys.argv[1]))
