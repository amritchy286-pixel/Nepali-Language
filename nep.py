import json
import os
import sys
import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


VERSION = "0.1.0"


def load_source(file_path):
    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


def validate_file(file_path):
    if not os.path.exists(file_path):
        raise RuntimeError(
            f"फाइल भेटिएन: {file_path}"
        )

    if not file_path.lower().endswith(".nep"):
        raise RuntimeError(
            "केवल .nep file प्रयोग गर्न मिल्छ।"
        )


def parse_source(
    source,
    file_name="<memory>"
):
    lexer = Lexer(
        source,
        file_name=file_name
    )

    tokens = lexer.tokenize()

    parser = Parser(
        tokens,
        file_name=file_name
    )

    return parser.parse()


def parse_file(file_path):
    source = load_source(
        file_path
    )

    return parse_source(
        source,
        file_name=file_path
    )


def get_project_main():
    config_path = os.path.join(
        os.getcwd(),
        "nep.json"
    )

    if not os.path.exists(config_path):
        raise RuntimeError(
            "nep.json भेटिएन। "
            "File दिनुहोस्: nep run <file.nep>"
        )

    try:
        with open(
            config_path,
            "r",
            encoding="utf-8"
        ) as file:
            config = json.load(file)

    except json.JSONDecodeError:
        raise RuntimeError(
            "nep.json सही JSON format मा छैन।"
        )

    main_file = config.get(
        "main"
    )

    if not main_file:
        raise RuntimeError(
            "nep.json मा 'main' सेट गरिएको छैन।"
        )

    return os.path.join(
        os.getcwd(),
        main_file
    )


def run_file(file_path):
    file_path = os.path.abspath(
        file_path
    )

    validate_file(
        file_path
    )

    statements = parse_file(
        file_path
    )

    interpreter = Interpreter(
        base_directory=os.path.dirname(
            file_path
        )
    )

    interpreter.run(
        statements
    )


def check_file(file_path):
    file_path = os.path.abspath(
        file_path
    )

    validate_file(
        file_path
    )

    parse_file(
        file_path
    )

    print(
        "ठीक छ: कुनै syntax त्रुटि भेटिएन।"
    )


def run_tests():
    loader = unittest.TestLoader()

    suite = loader.discover(
        start_dir="tests",
        pattern="test_*.py"
    )

    runner = unittest.TextTestRunner(
        verbosity=2
    )

    result = runner.run(
        suite
    )

    if not result.wasSuccessful():
        sys.exit(1)


def write_starter_file(main_file):
    starter_code = (
        'देखाऊ("नमस्ते नेपाल")\n'
    )

    with open(
        main_file,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(
            starter_code
        )


def create_project(project_name):
    if not project_name:
        raise RuntimeError(
            "Project name चाहिन्छ।"
        )

    project_path = os.path.abspath(
        project_name
    )

    if os.path.exists(project_path):
        raise RuntimeError(
            f"यो folder पहिले नै छ: {project_name}"
        )

    examples_path = os.path.join(
        project_path,
        "examples"
    )

    os.makedirs(
        examples_path
    )

    main_file = os.path.join(
        examples_path,
        "main.nep"
    )

    write_starter_file(
        main_file
    )

    config_file = os.path.join(
        project_path,
        "nep.json"
    )

    config = {
        "name": project_name,
        "version": VERSION,
        "main": "examples/main.nep"
    }

    with open(
        config_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            config,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Project बन्यो: {project_name}"
    )

    print(
        f"मुख्य file: {main_file}"
    )

    print(
        f"Config file: {config_file}"
    )

    print()
    print("चलाउन:")
    print(
        f'cd "{project_path}"'
    )
    print(
        "nep run"
    )


def init_project():
    project_path = os.getcwd()

    examples_path = os.path.join(
        project_path,
        "examples"
    )

    os.makedirs(
        examples_path,
        exist_ok=True
    )

    main_file = os.path.join(
        examples_path,
        "main.nep"
    )

    if not os.path.exists(main_file):
        write_starter_file(
            main_file
        )

    config_file = os.path.join(
        project_path,
        "nep.json"
    )

    if not os.path.exists(config_file):
        project_name = os.path.basename(
            project_path
        )

        config = {
            "name": project_name,
            "version": VERSION,
            "main": "examples/main.nep"
        }

        with open(
            config_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                config,
                file,
                ensure_ascii=False,
                indent=2
            )

    print(
        f"Project initialize भयो: {project_path}"
    )

    print(
        f"मुख्य file: {main_file}"
    )

    print(
        f"Config file: {config_file}"
    )

    print()
    print("चलाउन:")
    print(
        "nep run"
    )


def format_source(source):
    lines = source.splitlines()

    formatted_lines = []
    indent_level = 0
    indent_text = "    "

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            formatted_lines.append("")
            continue

        if line.startswith("}"):
            indent_level = max(
                0,
                indent_level - 1
            )

        formatted_lines.append(
            indent_text * indent_level
            + line
        )

        if line.endswith("{"):
            indent_level += 1

    return (
        "\n".join(
            formatted_lines
        ).rstrip()
        + "\n"
    )


def format_file(file_path):
    file_path = os.path.abspath(
        file_path
    )

    validate_file(
        file_path
    )

    source = load_source(
        file_path
    )

    formatted = format_source(
        source
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(
            formatted
        )

    print(
        f"Format भयो: {file_path}"
    )


def run_repl():
    print(
        f"Nepali Language REPL {VERSION}"
    )

    print(
        "बाहिर निस्कन: exit"
    )

    print()

    interpreter = Interpreter(
        base_directory=os.getcwd()
    )

    buffer = []
    brace_depth = 0

    while True:
        try:
            prompt = (
                "... "
                if buffer
                else "नेप> "
            )

            line = input(
                prompt
            )

            if (
                not buffer
                and line.strip() in (
                    "exit",
                    "quit",
                    "बन्द"
                )
            ):
                print(
                    "REPL बन्द भयो।"
                )
                break

            if (
                not line.strip()
                and not buffer
            ):
                continue

            buffer.append(
                line
            )

            brace_depth += line.count(
                "{"
            )

            brace_depth -= line.count(
                "}"
            )

            if brace_depth > 0:
                continue

            source = "\n".join(
                buffer
            )

            statements = parse_source(
                source,
                file_name="<REPL>"
            )

            interpreter.run(
                statements
            )

            buffer = []
            brace_depth = 0

        except KeyboardInterrupt:
            print()

            buffer = []
            brace_depth = 0

        except EOFError:
            print()
            print(
                "REPL बन्द भयो।"
            )
            break

        except Exception as error:
            print(
                f"त्रुटि: {error}"
            )

            buffer = []
            brace_depth = 0


def show_help():
    print(
        "Nepali Language CLI"
    )

    print()

    print(
        "प्रयोग:"
    )

    print(
        "  nep run [file.nep]"
    )

    print(
        "  nep check <file.nep>"
    )

    print(
        "  nep fmt <file.nep>"
    )

    print(
        "  nep test"
    )

    print(
        "  nep new <project-name>"
    )

    print(
        "  nep init"
    )

    print(
        "  nep repl"
    )

    print(
        "  nep version"
    )

    print(
        "  nep help"
    )


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    try:
        if command == "run":
            if len(sys.argv) >= 3:
                file_path = sys.argv[2]
            else:
                file_path = get_project_main()

            run_file(
                file_path
            )
            return

        if command == "check":
            if len(sys.argv) < 3:
                raise RuntimeError(
                    "check command लाई .nep file चाहिन्छ।"
                )

            check_file(
                sys.argv[2]
            )
            return

        if command == "fmt":
            if len(sys.argv) < 3:
                raise RuntimeError(
                    "fmt command लाई .nep file चाहिन्छ।"
                )

            format_file(
                sys.argv[2]
            )
            return

        if command == "test":
            run_tests()
            return

        if command == "new":
            if len(sys.argv) < 3:
                raise RuntimeError(
                    "new command लाई project name चाहिन्छ।"
                )

            create_project(
                sys.argv[2]
            )
            return

        if command == "init":
            init_project()
            return

        if command == "repl":
            run_repl()
            return

        if command == "version":
            print(
                f"Nepali Language {VERSION}"
            )
            return

        if command == "help":
            show_help()
            return

        if command.lower().endswith(
            ".nep"
        ):
            run_file(
                command
            )
            return

        raise RuntimeError(
            f"नचिनिएको command: {command}"
        )

    except Exception as error:
        print(
            f"त्रुटि: {error}"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()