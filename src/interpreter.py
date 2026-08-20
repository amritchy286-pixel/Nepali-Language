import json
import os

from src.errors import RuntimeLanguageError
from src.lexer import Lexer
from src.parser import Parser


class ReturnSignal:
    def __init__(self, value):
        self.value = value


class BreakSignal:
    pass


class ContinueSignal:
    pass


class Interpreter:
    def __init__(self, base_directory=None):
        self.variables = {}
        self.variable_types = {}
        self.functions = {}

        if base_directory is None:
            base_directory = os.getcwd()

        self.base_directory = os.path.abspath(
            base_directory
        )

        self.imported_files = set()

    def runtime_error(
        self,
        message,
        node=None
    ):
        file_name = None
        line = None
        column = None

        if node is not None:
            file_name = getattr(
                node,
                "file_name",
                None
            )

            line = getattr(
                node,
                "line",
                None
            )

            column = getattr(
                node,
                "column",
                None
            )

        raise RuntimeLanguageError(
            message,
            file_name=file_name,
            line=line,
            column=column
        )

    def run(self, statements):
        for statement in statements:
            result = self.execute(
                statement
            )

            if isinstance(
                result,
                ReturnSignal
            ):
                return result.value

            if isinstance(
                result,
                BreakSignal
            ):
                self.runtime_error(
                    "रोक loop बाहिर प्रयोग गर्न मिल्दैन।",
                    statement
                )

            if isinstance(
                result,
                ContinueSignal
            ):
                self.runtime_error(
                    "जारी loop बाहिर प्रयोग गर्न मिल्दैन।",
                    statement
                )

    def execute(self, statement):
        class_name = (
            statement.__class__.__name__
        )

        if class_name == "ImportStatement":
            self.import_file(
                statement.path,
                statement
            )
            return None

        if class_name == "VariableDeclaration":
            value = self.evaluate(
                statement.expression
            )

            self.check_type(
                statement.name,
                value,
                statement.data_type,
                statement
            )

            self.variables[
                statement.name
            ] = value

            self.variable_types[
                statement.name
            ] = statement.data_type

            return None

        if class_name == "VariableAssignment":
            if (
                statement.name
                not in self.variables
            ):
                self.runtime_error(
                    f"Variable भेटिएन: {statement.name}",
                    statement
                )

            value = self.evaluate(
                statement.expression
            )

            data_type = self.variable_types[
                statement.name
            ]

            self.check_type(
                statement.name,
                value,
                data_type,
                statement
            )

            self.variables[
                statement.name
            ] = value

            return None

        if class_name == "IndexAssignment":
            target = self.evaluate(
                statement.target
            )

            index = self.evaluate(
                statement.index
            )

            value = self.evaluate(
                statement.expression
            )

            if isinstance(target, list):
                if (
                    isinstance(index, bool)
                    or not isinstance(
                        index,
                        int
                    )
                ):
                    self.runtime_error(
                        "सूचीको index पूर्णाङ्क हुनुपर्छ।",
                        statement.index
                    )

                if (
                    index < 0
                    or index >= len(target)
                ):
                    self.runtime_error(
                        f"Index सीमा बाहिर छ: {index}",
                        statement.index
                    )

                target[index] = value
                return None

            if isinstance(target, dict):
                if not isinstance(
                    index,
                    str
                ):
                    self.runtime_error(
                        "नक्साको key पाठ हुनुपर्छ।",
                        statement.index
                    )

                target[index] = value
                return None

            self.runtime_error(
                "Index assignment गर्न सूची वा नक्सा चाहिन्छ।",
                statement
            )

        if class_name == "PrintStatement":
            value = self.evaluate(
                statement.expression
            )

            self.print_value(value)

            return None

        if class_name == "IfStatement":
            condition = self.evaluate(
                statement.condition
            )

            if not isinstance(
                condition,
                bool
            ):
                self.runtime_error(
                    "यदि को condition सही वा गलत हुनुपर्छ।",
                    statement.condition
                )

            if condition:
                body = statement.then_body
            else:
                body = statement.else_body

            for inner_statement in body:
                result = self.execute(
                    inner_statement
                )

                if isinstance(
                    result,
                    (
                        ReturnSignal,
                        BreakSignal,
                        ContinueSignal
                    )
                ):
                    return result

            return None

        if class_name == "WhileStatement":
            while True:
                condition = self.evaluate(
                    statement.condition
                )

                if not isinstance(
                    condition,
                    bool
                ):
                    self.runtime_error(
                        "जब को condition सही वा गलत हुनुपर्छ।",
                        statement.condition
                    )

                if not condition:
                    break

                should_continue = False

                for inner_statement in statement.body:
                    result = self.execute(
                        inner_statement
                    )

                    if isinstance(
                        result,
                        ReturnSignal
                    ):
                        return result

                    if isinstance(
                        result,
                        BreakSignal
                    ):
                        return None

                    if isinstance(
                        result,
                        ContinueSignal
                    ):
                        should_continue = True
                        break

                if should_continue:
                    continue

            return None

        if class_name == "ForEachStatement":
            iterable = self.evaluate(
                statement.iterable
            )

            if isinstance(
                iterable,
                dict
            ):
                iterable = list(
                    iterable.keys()
                )

            if not isinstance(
                iterable,
                (list, str)
            ):
                self.runtime_error(
                    "हरेक loop मा सूची, पाठ वा नक्सा चाहिन्छ।",
                    statement.iterable
                )

            variable_name = (
                statement.variable_name
            )

            had_old_value = (
                variable_name
                in self.variables
            )

            old_value = self.variables.get(
                variable_name
            )

            had_old_type = (
                variable_name
                in self.variable_types
            )

            old_type = self.variable_types.get(
                variable_name
            )

            try:
                for item in iterable:
                    self.variables[
                        variable_name
                    ] = item

                    self.variable_types[
                        variable_name
                    ] = self.get_data_type(
                        item
                    )

                    should_continue = False

                    for inner_statement in statement.body:
                        result = self.execute(
                            inner_statement
                        )

                        if isinstance(
                            result,
                            ReturnSignal
                        ):
                            return result

                        if isinstance(
                            result,
                            BreakSignal
                        ):
                            return None

                        if isinstance(
                            result,
                            ContinueSignal
                        ):
                            should_continue = True
                            break

                    if should_continue:
                        continue

            finally:
                if had_old_value:
                    self.variables[
                        variable_name
                    ] = old_value
                else:
                    self.variables.pop(
                        variable_name,
                        None
                    )

                if had_old_type:
                    self.variable_types[
                        variable_name
                    ] = old_type
                else:
                    self.variable_types.pop(
                        variable_name,
                        None
                    )

            return None

        if class_name == "BreakStatement":
            return BreakSignal()

        if class_name == "ContinueStatement":
            return ContinueSignal()

        if class_name == "FunctionDeclaration":
            self.functions[
                statement.name
            ] = statement

            return None

        if class_name == "FunctionCallStatement":
            self.evaluate(
                statement.call
            )

            return None

        if class_name == "ReturnStatement":
            value = self.evaluate(
                statement.expression
            )

            return ReturnSignal(
                value
            )

        self.runtime_error(
            f"चलाउन नसकिने statement: {class_name}",
            statement
        )

    def resolve_import_path(
        self,
        path,
        import_node=None
    ):
        if not isinstance(path, str):
            self.runtime_error(
                "प्रयोग मा file path पाठ हुनुपर्छ।",
                import_node
            )

        path = path.strip()

        if not path:
            self.runtime_error(
                "प्रयोग मा खाली module name दिन मिल्दैन।",
                import_node
            )

        candidates = []

        # 1. Existing relative/absolute import behavior.
        if os.path.isabs(path):
            candidates.append(
                os.path.abspath(path)
            )
        else:
            candidates.append(
                os.path.abspath(
                    os.path.join(
                        self.base_directory,
                        path
                    )
                )
            )

            if not path.lower().endswith(".nep"):
                candidates.append(
                    os.path.abspath(
                        os.path.join(
                            self.base_directory,
                            path + ".nep"
                        )
                    )
                )

        # 2. Short standard-library import:
        #    प्रयोग "गणित"
        #    -> <project>/stdlib/गणित.nep
        simple_module_name = (
            not os.path.isabs(path)
            and "/" not in path
            and "\\" not in path
        )

        if simple_module_name:
            module_file = (
                path
                if path.lower().endswith(".nep")
                else path + ".nep"
            )

            current = os.path.abspath(
                self.base_directory
            )

            while True:
                candidates.append(
                    os.path.join(
                        current,
                        "stdlib",
                        module_file
                    )
                )

                parent = os.path.dirname(
                    current
                )

                if parent == current:
                    break

                current = parent

            # Also support stdlib beside this interpreter's project root.
            language_root = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

            candidates.append(
                os.path.join(
                    language_root,
                    "stdlib",
                    module_file
                )
            )

        seen = set()

        for candidate in candidates:
            candidate = os.path.abspath(
                candidate
            )

            if candidate in seen:
                continue

            seen.add(candidate)

            if (
                os.path.isfile(candidate)
                and candidate.lower().endswith(".nep")
            ):
                return candidate

        self.runtime_error(
            f"Import file वा module भेटिएन: {path}",
            import_node
        )

    def import_file(
        self,
        path,
        import_node=None
    ):
        if not isinstance(
            path,
            str
        ):
            self.runtime_error(
                "प्रयोग मा file path पाठ हुनुपर्छ।",
                import_node
            )

        full_path = self.resolve_import_path(
            path,
            import_node
        )

        if full_path in self.imported_files:
            return

        self.imported_files.add(
            full_path
        )

        try:
            with open(
                full_path,
                "r",
                encoding="utf-8"
            ) as file:
                source = file.read()

            lexer = Lexer(
                source,
                file_name=full_path
            )

            tokens = lexer.tokenize()

            parser = Parser(
                tokens,
                file_name=full_path
            )

            statements = parser.parse()

            old_base_directory = (
                self.base_directory
            )

            self.base_directory = os.path.dirname(
                full_path
            )

            try:
                for statement in statements:
                    result = self.execute(
                        statement
                    )

                    if isinstance(
                        result,
                        ReturnSignal
                    ):
                        self.runtime_error(
                            "फर्काऊ function बाहिर प्रयोग गर्न मिल्दैन।",
                            statement
                        )

                    if isinstance(
                        result,
                        BreakSignal
                    ):
                        self.runtime_error(
                            "रोक loop बाहिर प्रयोग गर्न मिल्दैन।",
                            statement
                        )

                    if isinstance(
                        result,
                        ContinueSignal
                    ):
                        self.runtime_error(
                            "जारी loop बाहिर प्रयोग गर्न मिल्दैन।",
                            statement
                        )

            finally:
                self.base_directory = (
                    old_base_directory
                )

        except Exception:
            self.imported_files.discard(
                full_path
            )
            raise

    def evaluate(self, expression):
        class_name = (
            expression.__class__.__name__
        )

        if class_name == "NumberExpression":
            return expression.value

        if class_name == "StringExpression":
            return expression.value

        if class_name == "BooleanExpression":
            return expression.value

        if class_name == "ListExpression":
            return [
                self.evaluate(item)
                for item in expression.items
            ]

        if class_name == "MapExpression":
            result = {}

            for (
                key,
                value_expression
            ) in expression.items:
                result[key] = self.evaluate(
                    value_expression
                )

            return result

        if class_name == "InputExpression":
            return input(
                expression.prompt
            )

        if class_name == "VariableExpression":
            if (
                expression.name
                not in self.variables
            ):
                self.runtime_error(
                    f"Variable भेटिएन: {expression.name}",
                    expression
                )

            return self.variables[
                expression.name
            ]

        if class_name == "IndexExpression":
            target = self.evaluate(
                expression.target
            )

            index = self.evaluate(
                expression.index
            )

            if isinstance(target, list):
                if (
                    isinstance(index, bool)
                    or not isinstance(
                        index,
                        int
                    )
                ):
                    self.runtime_error(
                        "सूचीको index पूर्णाङ्क हुनुपर्छ।",
                        expression
                    )

                if (
                    index < 0
                    or index >= len(target)
                ):
                    self.runtime_error(
                        f"Index सीमा बाहिर छ: {index}",
                        expression
                    )

                return target[index]

            if isinstance(target, str):
                if (
                    isinstance(index, bool)
                    or not isinstance(
                        index,
                        int
                    )
                ):
                    self.runtime_error(
                        "पाठको index पूर्णाङ्क हुनुपर्छ।",
                        expression
                    )

                if (
                    index < 0
                    or index >= len(target)
                ):
                    self.runtime_error(
                        f"Index सीमा बाहिर छ: {index}",
                        expression
                    )

                return target[index]

            if isinstance(target, dict):
                if not isinstance(
                    index,
                    str
                ):
                    self.runtime_error(
                        "नक्साको key पाठ हुनुपर्छ।",
                        expression
                    )

                if index not in target:
                    self.runtime_error(
                        f"नक्सामा key भेटिएन: {index}",
                        expression
                    )

                return target[index]

            self.runtime_error(
                "Index प्रयोग गर्न सूची, पाठ वा नक्सा चाहिन्छ।",
                expression
            )

        if class_name == "UnaryExpression":
            value = self.evaluate(
                expression.expression
            )

            if (
                expression.operator
                == "NOT"
            ):
                if not isinstance(
                    value,
                    bool
                ):
                    self.runtime_error(
                        "होइन प्रयोग गर्न सही वा गलत मान चाहिन्छ।",
                        expression
                    )

                return not value

            if (
                expression.operator
                == "NEGATIVE"
            ):
                if (
                    isinstance(value, bool)
                    or not isinstance(
                        value,
                        (int, float)
                    )
                ):
                    self.runtime_error(
                        "ऋणात्मक चिन्ह संख्या मा मात्र प्रयोग गर्न मिल्छ।",
                        expression
                    )

                return -value

            self.runtime_error(
                f"नचिनिएको unary operator: {expression.operator}",
                expression
            )

        if class_name == "BinaryExpression":
            if expression.operator == "AND":
                left = self.evaluate(
                    expression.left
                )

                if not isinstance(
                    left,
                    bool
                ):
                    self.runtime_error(
                        "र operator को बायाँ मान सही वा गलत हुनुपर्छ।",
                        expression
                    )

                if not left:
                    return False

                right = self.evaluate(
                    expression.right
                )

                if not isinstance(
                    right,
                    bool
                ):
                    self.runtime_error(
                        "र operator को दायाँ मान सही वा गलत हुनुपर्छ।",
                        expression
                    )

                return (
                    left and right
                )

            if expression.operator == "OR":
                left = self.evaluate(
                    expression.left
                )

                if not isinstance(
                    left,
                    bool
                ):
                    self.runtime_error(
                        "वा operator को बायाँ मान सही वा गलत हुनुपर्छ।",
                        expression
                    )

                if left:
                    return True

                right = self.evaluate(
                    expression.right
                )

                if not isinstance(
                    right,
                    bool
                ):
                    self.runtime_error(
                        "वा operator को दायाँ मान सही वा गलत हुनुपर्छ।",
                        expression
                    )

                return (
                    left or right
                )

            left = self.evaluate(
                expression.left
            )

            right = self.evaluate(
                expression.right
            )

            try:
                if expression.operator == "PLUS":
                    return left + right

                if expression.operator == "MINUS":
                    return left - right

                if expression.operator == "MULTIPLY":
                    return left * right

                if expression.operator == "DIVIDE":
                    if right == 0:
                        self.runtime_error(
                            "शून्यले भाग गर्न मिल्दैन।",
                            expression
                        )

                    return left / right

                if expression.operator == "MODULO":
                    if right == 0:
                        self.runtime_error(
                            "शून्यले modulo गर्न मिल्दैन।",
                            expression
                        )

                    return left % right

                if expression.operator == "POWER":
                    return left ** right

                if expression.operator == "GREATER":
                    return left > right

                if expression.operator == "LESS":
                    return left < right

                if expression.operator == "GREATER_EQUAL":
                    return left >= right

                if expression.operator == "LESS_EQUAL":
                    return left <= right

                if expression.operator == "EQUAL_EQUAL":
                    return left == right

                if expression.operator == "NOT_EQUAL":
                    return left != right

            except TypeError:
                self.runtime_error(
                    "यो operation यी दुई मानमा प्रयोग गर्न मिल्दैन।",
                    expression
                )

            self.runtime_error(
                f"नचिनिएको operator: {expression.operator}",
                expression
            )

        if class_name == "FunctionCallExpression":
            return self.call_function(
                expression
            )

        self.runtime_error(
            f"नचिनिएको expression: {class_name}",
            expression
        )

    def call_function(self, call):
        if call.name == "पूर्णाङ्कमा":
            self.check_argument_count(
                call,
                1
            )

            value = self.evaluate(
                call.arguments[0]
            )

            try:
                return int(value)

            except (
                ValueError,
                TypeError
            ):
                self.runtime_error(
                    f"'{value}' लाई पूर्णाङ्कमा बदल्न सकिएन।",
                    call
                )

        if call.name == "दशमलवमा":
            self.check_argument_count(
                call,
                1
            )

            value = self.evaluate(
                call.arguments[0]
            )

            try:
                return float(value)

            except (
                ValueError,
                TypeError
            ):
                self.runtime_error(
                    f"'{value}' लाई दशमलवमा बदल्न सकिएन।",
                    call
                )

        if call.name == "पाठमा":
            self.check_argument_count(
                call,
                1
            )

            value = self.evaluate(
                call.arguments[0]
            )

            if value is True:
                return "सही"

            if value is False:
                return "गलत"

            return str(value)

        if call.name == "लम्बाइ":
            self.check_argument_count(
                call,
                1
            )

            value = self.evaluate(
                call.arguments[0]
            )

            if not isinstance(
                value,
                (list, str, dict)
            ):
                self.runtime_error(
                    "लम्बाइ() मा सूची, पाठ वा नक्सा चाहिन्छ।",
                    call
                )

            return len(value)

        if call.name == "थप":
            self.check_argument_count(
                call,
                2
            )

            target = self.evaluate(
                call.arguments[0]
            )

            value = self.evaluate(
                call.arguments[1]
            )

            if not isinstance(
                target,
                list
            ):
                self.runtime_error(
                    "थप() को पहिलो argument सूची हुनुपर्छ।",
                    call
                )

            target.append(
                value
            )

            return None

        if call.name == "हटाऊ":
            self.check_argument_count(
                call,
                2
            )

            target = self.evaluate(
                call.arguments[0]
            )

            value = self.evaluate(
                call.arguments[1]
            )

            if not isinstance(
                target,
                list
            ):
                self.runtime_error(
                    "हटाऊ() को पहिलो argument सूची हुनुपर्छ।",
                    call
                )

            if value not in target:
                self.runtime_error(
                    f"सूचीमा '{value}' भेटिएन।",
                    call
                )

            target.remove(
                value
            )

            return None

        if call.name == "छकि":
            self.check_argument_count(
                call,
                2
            )

            target = self.evaluate(
                call.arguments[0]
            )

            value = self.evaluate(
                call.arguments[1]
            )

            if isinstance(
                target,
                dict
            ):
                return value in target

            if isinstance(
                target,
                (list, str)
            ):
                return value in target

            self.runtime_error(
                "छकि() मा सूची, पाठ वा नक्सा चाहिन्छ।",
                call
            )

        if call.name == "फाइललेख":
            self.check_argument_count(
                call,
                2
            )

            path = self.evaluate(
                call.arguments[0]
            )

            content = self.evaluate(
                call.arguments[1]
            )

            if not isinstance(
                path,
                str
            ):
                self.runtime_error(
                    "फाइललेख() को पहिलो argument फाइल path हुनुपर्छ।",
                    call
                )

            if not isinstance(
                content,
                str
            ):
                content = str(
                    content
                )

            full_path = os.path.join(
                self.base_directory,
                path
            )

            try:
                with open(
                    full_path,
                    "w",
                    encoding="utf-8"
                ) as file:
                    file.write(
                        content
                    )

            except OSError as error:
                self.runtime_error(
                    f"फाइल लेख्न सकिएन: {error}",
                    call
                )

            return None

        if call.name == "फाइलपढ":
            self.check_argument_count(
                call,
                1
            )

            path = self.evaluate(
                call.arguments[0]
            )

            if not isinstance(
                path,
                str
            ):
                self.runtime_error(
                    "फाइलपढ() मा फाइल path चाहिन्छ।",
                    call
                )

            full_path = os.path.join(
                self.base_directory,
                path
            )

            try:
                with open(
                    full_path,
                    "r",
                    encoding="utf-8"
                ) as file:
                    return file.read()

            except FileNotFoundError:
                self.runtime_error(
                    f"फाइल भेटिएन: {path}",
                    call
                )

            except OSError as error:
                self.runtime_error(
                    f"फाइल पढ्न सकिएन: {error}",
                    call
                )

        if call.name == "फाइलछकि":
            self.check_argument_count(
                call,
                1
            )

            path = self.evaluate(
                call.arguments[0]
            )

            if not isinstance(
                path,
                str
            ):
                self.runtime_error(
                    "फाइलछकि() मा फाइल path चाहिन्छ।",
                    call
                )

            full_path = os.path.join(
                self.base_directory,
                path
            )

            return os.path.exists(
                full_path
            )

        if call.name == "JSONबनाऊ":
            self.check_argument_count(
                call,
                1
            )

            value = self.evaluate(
                call.arguments[0]
            )

            try:
                return json.dumps(
                    value,
                    ensure_ascii=False
                )

            except (
                TypeError,
                ValueError
            ):
                self.runtime_error(
                    "यो मानलाई JSON मा बदल्न सकिएन।",
                    call
                )

        if call.name == "JSONपढ":
            self.check_argument_count(
                call,
                1
            )

            value = self.evaluate(
                call.arguments[0]
            )

            if not isinstance(
                value,
                str
            ):
                self.runtime_error(
                    "JSONपढ() मा JSON पाठ चाहिन्छ।",
                    call
                )

            try:
                return json.loads(
                    value
                )

            except json.JSONDecodeError:
                self.runtime_error(
                    "JSON पाठ सही छैन।",
                    call
                )

        if call.name not in self.functions:
            self.runtime_error(
                f"काम भेटिएन: {call.name}",
                call
            )

        function = self.functions[
            call.name
        ]

        if (
            len(call.arguments)
            != len(function.parameters)
        ):
            self.runtime_error(
                f"काम '{call.name}' लाई "
                f"{len(function.parameters)} वटा argument चाहिन्छ।",
                call
            )

        argument_values = [
            self.evaluate(argument)
            for argument in call.arguments
        ]

        old_variables = (
            self.variables.copy()
        )

        old_variable_types = (
            self.variable_types.copy()
        )

        try:
            for (
                parameter,
                value
            ) in zip(
                function.parameters,
                argument_values
            ):
                self.check_type(
                    parameter.name,
                    value,
                    parameter.data_type,
                    call
                )

                self.variables[
                    parameter.name
                ] = value

                self.variable_types[
                    parameter.name
                ] = parameter.data_type

            returned = False
            return_value = None

            for statement in function.body:
                result = self.execute(
                    statement
                )

                if isinstance(
                    result,
                    ReturnSignal
                ):
                    returned = True
                    return_value = result.value
                    break

                if isinstance(
                    result,
                    BreakSignal
                ):
                    self.runtime_error(
                        "रोक function भित्र loop बाहिर प्रयोग गर्न मिल्दैन।",
                        statement
                    )

                if isinstance(
                    result,
                    ContinueSignal
                ):
                    self.runtime_error(
                        "जारी function भित्र loop बाहिर प्रयोग गर्न मिल्दैन।",
                        statement
                    )

            if (
                function.return_type
                is not None
            ):
                if not returned:
                    self.runtime_error(
                        f"काम '{function.name}' ले "
                        f"{function.return_type} फर्काउनुपर्छ।",
                        function
                    )

                self.check_type(
                    f"{function.name} को फर्काइएको मान",
                    return_value,
                    function.return_type,
                    function
                )

                return return_value

            if returned:
                return return_value

            return None

        finally:
            self.variables = (
                old_variables
            )

            self.variable_types = (
                old_variable_types
            )

    def check_argument_count(
        self,
        call,
        expected
    ):
        if (
            len(call.arguments)
            != expected
        ):
            self.runtime_error(
                f"{call.name}() लाई "
                f"{expected} वटा argument चाहिन्छ।",
                call
            )

    def get_data_type(
        self,
        value
    ):
        if isinstance(
            value,
            bool
        ):
            return "सत्य"

        if isinstance(
            value,
            int
        ):
            return "पूर्णाङ्क"

        if isinstance(
            value,
            float
        ):
            return "दशमलव"

        if isinstance(
            value,
            str
        ):
            return "पाठ"

        if isinstance(
            value,
            list
        ):
            return "सूची"

        if isinstance(
            value,
            dict
        ):
            return "नक्सा"

        return None

    def check_type(
        self,
        name,
        value,
        data_type,
        node=None
    ):
        if data_type == "पूर्णाङ्क":
            if (
                isinstance(
                    value,
                    bool
                )
                or not isinstance(
                    value,
                    int
                )
            ):
                self.runtime_error(
                    f"पूर्णाङ्क '{name}' मा पूर्णाङ्क मान मात्र राख्न मिल्छ।",
                    node
                )

        elif data_type == "दशमलव":
            if (
                isinstance(
                    value,
                    bool
                )
                or not isinstance(
                    value,
                    (int, float)
                )
            ):
                self.runtime_error(
                    f"दशमलव '{name}' मा संख्या मात्र राख्न मिल्छ।",
                    node
                )

        elif data_type == "पाठ":
            if not isinstance(
                value,
                str
            ):
                self.runtime_error(
                    f"पाठ '{name}' मा पाठ मान मात्र राख्न मिल्छ।",
                    node
                )

        elif data_type == "सत्य":
            if not isinstance(
                value,
                bool
            ):
                self.runtime_error(
                    f"सत्य '{name}' मा सही वा गलत मात्र राख्न मिल्छ।",
                    node
                )

        elif data_type == "सूची":
            if not isinstance(
                value,
                list
            ):
                self.runtime_error(
                    f"सूची '{name}' मा सूची मात्र राख्न मिल्छ।",
                    node
                )

        elif data_type == "नक्सा":
            if not isinstance(
                value,
                dict
            ):
                self.runtime_error(
                    f"नक्सा '{name}' मा नक्सा मात्र राख्न मिल्छ।",
                    node
                )

        else:
            self.runtime_error(
                f"नचिनिएको data type: {data_type}",
                node
            )

    def print_value(
        self,
        value
    ):
        if value is True:
            print("सही")
            return

        if value is False:
            print("गलत")
            return

        if value is None:
            print("खाली")
            return

        if isinstance(
            value,
            list
        ):
            formatted_items = [
                self.format_value(item)
                for item in value
            ]

            print(
                "["
                + ", ".join(
                    formatted_items
                )
                + "]"
            )

            return

        if isinstance(
            value,
            dict
        ):
            formatted_items = []

            for (
                key,
                item
            ) in value.items():
                formatted_items.append(
                    f'"{key}": '
                    f"{self.format_value(item)}"
                )

            print(
                "{"
                + ", ".join(
                    formatted_items
                )
                + "}"
            )

            return

        print(value)

    def format_value(
        self,
        value
    ):
        if value is True:
            return "सही"

        if value is False:
            return "गलत"

        if value is None:
            return "खाली"

        if isinstance(
            value,
            str
        ):
            return value

        if isinstance(
            value,
            list
        ):
            return (
                "["
                + ", ".join(
                    self.format_value(item)
                    for item in value
                )
                + "]"
            )

        if isinstance(
            value,
            dict
        ):
            return (
                "{"
                + ", ".join(
                    f'"{key}": '
                    f"{self.format_value(item)}"
                    for (
                        key,
                        item
                    ) in value.items()
                )
                + "}"
            )

        return str(value)