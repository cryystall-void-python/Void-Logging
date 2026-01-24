import re
import sys
from pathlib import Path


ARGS_HEADER_RE = re.compile(r"^(?P<indent>\s*)Args:\s*$")
RETURNS_HEADER_RE = re.compile(r"^(?P<indent>\s*)Returns:\s*$")

ARG_RE = re.compile(
    r"^(?P<indent>\s+)(?P<name>\w+)\s*(?:\([^)]+\))?:\s*(?P<desc>.*)"
)

CONT_RE = re.compile(r"^(?P<indent>\s+)(?P<text>.+)")


def convert_google_to_sphinx(docstring: str) -> str:
    lines = docstring.splitlines()
    out = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # ---------- Args ----------
        args_match = ARGS_HEADER_RE.match(line)
        if args_match:
            base_indent = args_match.group("indent")
            param_indent = base_indent
            cont_indent = base_indent + " " * 4
            i += 1

            while i < len(lines):
                arg_match = ARG_RE.match(lines[i])
                if not arg_match:
                    break

                name = arg_match.group("name")
                desc = arg_match.group("desc").strip()

                out.append(f"{param_indent}:param {name}: {desc}")
                i += 1

                # continuation lines
                while i < len(lines):
                    cont = CONT_RE.match(lines[i])
                    if not cont:
                        break
                    if len(cont.group("indent")) <= len(arg_match.group("indent")):
                        break

                    out.append(f"{cont_indent}{cont.group('text').strip()}")
                    i += 1
            continue

        # ---------- Returns ----------
        ret_match = RETURNS_HEADER_RE.match(line)
        if ret_match:
            base_indent = ret_match.group("indent")
            i += 1
            if i < len(lines) and lines[i].strip():
                out.append(f"{base_indent}:return: {lines[i].strip()}")
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
