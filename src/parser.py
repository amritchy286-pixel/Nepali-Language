from src.errors import ParserError


class Node:
    def __init__(
        self,
        line=None,
        column=None,
        file_name=None
    ):
        self.line = line
        self.column = column
        self.file_name = file_name


class NumberExpression(Node):
    def __init__(
        self,
        value,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.value = value


class StringExpression(Node):
    def __init__(
        self,
        value,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.value = value


class BooleanExpression(Node):
    def __init__(
        self,
        value,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.value = value


class ListExpression(Node):
    def __init__(
        self,
        items,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.items = items


class MapExpression(Node):
    def __init__(
        self,
        items,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.items = items


class VariableExpression(Node):
    def __init__(
        self,
        name,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.name = name


class IndexExpression(Node):
    def __init__(
        self,
        target,
        index,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.target = target
        self.index = index


class InputExpression(Node):
    def __init__(
        self,
        prompt,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.prompt = prompt


class UnaryExpression(Node):
    def __init__(
        self,
        operator,
        expression,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.operator = operator
        self.expression = expression


class BinaryExpression(Node):
    def __init__(
        self,
        left,
        operator,
        right,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.left = left
        self.operator = operator
        self.right = right


class FunctionCallExpression(Node):
    def __init__(
        self,
        name,
        arguments,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.name = name
        self.arguments = arguments


class PrintStatement(Node):
    def __init__(
        self,
        expression,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.expression = expression


class VariableDeclaration(Node):
    def __init__(
        self,
        name,
        expression,
        data_type,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.name = name
        self.expression = expression
        self.data_type = data_type


class VariableAssignment(Node):
    def __init__(
        self,
        name,
        expression,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.name = name
        self.expression = expression


class IndexAssignment(Node):
    def __init__(
        self,
        target,
        index,
        expression,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.target = target
        self.index = index
        self.expression = expression


class IfStatement(Node):
    def __init__(
        self,
        condition,
        then_body,
        else_body=None,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body or []


class WhileStatement(Node):
    def __init__(
        self,
        condition,
        body,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.condition = condition
        self.body = body


class ForEachStatement(Node):
    def __init__(
        self,
        variable_name,
        iterable,
        body,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.variable_name = variable_name
        self.iterable = iterable
        self.body = body


class BreakStatement(Node):
    pass


class ContinueStatement(Node):
    pass


class FunctionParameter(Node):
    def __init__(
        self,
        name,
        data_type,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.name = name
        self.data_type = data_type


class FunctionDeclaration(Node):
    def __init__(
        self,
        name,
        parameters,
        body,
        return_type=None,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.name = name
        self.parameters = parameters
        self.body = body
        self.return_type = return_type


class FunctionCallStatement(Node):
    def __init__(
        self,
        call,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.call = call


class ReturnStatement(Node):
    def __init__(
        self,
        expression,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.expression = expression


class ImportStatement(Node):
    def __init__(
        self,
        path,
        line=None,
        column=None,
        file_name=None
    ):
        super().__init__(
            line,
            column,
            file_name
        )
        self.path = path


class Parser:
    def __init__(
        self,
        tokens,
        file_name=None
    ):
        self.tokens = tokens
        self.position = 0
        self.file_name = file_name

    def current_token(self):
        if self.position >= len(self.tokens):
            return None

        return self.tokens[self.position]

    def peek_token(self, offset=1):
        position = self.position + offset

        if position >= len(self.tokens):
            return None

        return self.tokens[position]

    def advance(self):
        self.position += 1

    def location(self, token):
        if token is None:
            return (
                None,
                None,
                self.file_name
            )

        return (
            getattr(
                token,
                "line",
                None
            ),
            getattr(
                token,
                "column",
                None
            ),
            self.file_name
        )

    def error(
        self,
        message,
        token=None
    ):
        if token is None:
            token = self.current_token()

        line = None
        column = None

        if token is not None:
            line = getattr(
                token,
                "line",
                None
            )

            column = getattr(
                token,
                "column",
                None
            )

        raise ParserError(
            message,
            file_name=self.file_name,
            line=line,
            column=column
        )

    def expect(self, token_type):
        token = self.current_token()

        if token is None:
            previous = None

            if self.position > 0:
                previous = self.tokens[
                    self.position - 1
                ]

            self.error(
                f"{token_type} चाहिएको थियो, तर code सकियो।",
                token=previous
            )

        if token.type != token_type:
            self.error(
                f"{token_type} चाहिएको थियो, "
                f"तर {token.type} भेटियो।",
                token=token
            )

        self.advance()
        return token

    def parse(self):
        statements = []

        while self.current_token() is not None:
            statements.append(
                self.parse_statement()
            )

        return statements

    def parse_statement(self):
        token = self.current_token()

        if token is None:
            self.error(
                "Statement चाहिएको थियो।"
            )

        if token.type == "IMPORT":
            return self.parse_import()

        if token.type in (
            "INTEGER_TYPE",
            "FLOAT_TYPE",
            "STRING_TYPE",
            "BOOLEAN_TYPE",
            "LIST_TYPE",
            "MAP_TYPE",
        ):
            return self.parse_variable_declaration()

        if token.type == "PRINT":
            return self.parse_print()

        if token.type == "IF":
            return self.parse_if()

        if token.type == "WHILE":
            return self.parse_while()

        if token.type == "FOR_EACH":
            return self.parse_for_each()

        if token.type == "BREAK":
            self.advance()

            line, column, file_name = (
                self.location(token)
            )

            return BreakStatement(
                line,
                column,
                file_name
            )

        if token.type == "CONTINUE":
            self.advance()

            line, column, file_name = (
                self.location(token)
            )

            return ContinueStatement(
                line,
                column,
                file_name
            )

        if token.type == "FUNCTION":
            return self.parse_function_declaration()

        if token.type == "RETURN":
            return self.parse_return()

        if token.type == "IDENTIFIER":
            next_token = self.peek_token()

            if (
                next_token is not None
                and next_token.type == "EQUALS"
            ):
                return self.parse_variable_assignment()

            if (
                next_token is not None
                and next_token.type == "LBRACKET"
            ):
                return self.parse_index_assignment()

            if (
                next_token is not None
                and next_token.type == "LPAREN"
            ):
                call = self.parse_function_call()

                return FunctionCallStatement(
                    call,
                    line=call.line,
                    column=call.column,
                    file_name=call.file_name
                )

        self.error(
            f"अज्ञात statement: {token.value}",
            token=token
        )

    def parse_import(self):
        start = self.expect(
            "IMPORT"
        )

        path = self.expect(
            "STRING"
        )

        line, column, file_name = (
            self.location(start)
        )

        return ImportStatement(
            path.value[1:-1],
            line,
            column,
            file_name
        )

    def parse_variable_declaration(self):
        start = self.current_token()

        data_type = self.parse_type()

        name = self.expect(
            "IDENTIFIER"
        )

        self.expect(
            "EQUALS"
        )

        expression = self.parse_expression()

        line, column, file_name = (
            self.location(start)
        )

        return VariableDeclaration(
            name.value,
            expression,
            data_type,
            line,
            column,
            file_name
        )

    def parse_type(self):
        token = self.current_token()

        if token is None:
            self.error(
                "Data type चाहिएको थियो, तर code सकियो।"
            )

        types = {
            "INTEGER_TYPE": "पूर्णाङ्क",
            "FLOAT_TYPE": "दशमलव",
            "STRING_TYPE": "पाठ",
            "BOOLEAN_TYPE": "सत्य",
            "LIST_TYPE": "सूची",
            "MAP_TYPE": "नक्सा",
        }

        if token.type in types:
            self.advance()
            return types[token.type]

        self.error(
            f"Data type चाहिएको थियो, "
            f"तर {token.value} भेटियो।",
            token=token
        )

    def parse_variable_assignment(self):
        name = self.expect(
            "IDENTIFIER"
        )

        self.expect(
            "EQUALS"
        )

        expression = self.parse_expression()

        line, column, file_name = (
            self.location(name)
        )

        return VariableAssignment(
            name.value,
            expression,
            line,
            column,
            file_name
        )

    def parse_index_assignment(self):
        name = self.expect(
            "IDENTIFIER"
        )

        line, column, file_name = (
            self.location(name)
        )

        target = VariableExpression(
            name.value,
            line,
            column,
            file_name
        )

        self.expect(
            "LBRACKET"
        )

        index = self.parse_expression()

        self.expect(
            "RBRACKET"
        )

        self.expect(
            "EQUALS"
        )

        expression = self.parse_expression()

        return IndexAssignment(
            target,
            index,
            expression,
            line,
            column,
            file_name
        )

    def parse_print(self):
        start = self.expect(
            "PRINT"
        )

        self.expect(
            "LPAREN"
        )

        expression = self.parse_expression()

        self.expect(
            "RPAREN"
        )

        line, column, file_name = (
            self.location(start)
        )

        return PrintStatement(
            expression,
            line,
            column,
            file_name
        )

    def parse_if(self):
        start = self.expect(
            "IF"
        )

        self.expect(
            "LPAREN"
        )

        condition = self.parse_expression()

        self.expect(
            "RPAREN"
        )

        then_body = self.parse_block()
        else_body = []

        token = self.current_token()

        if (
            token is not None
            and token.type == "ELSE"
        ):
            self.advance()
            else_body = self.parse_block()

        line, column, file_name = (
            self.location(start)
        )

        return IfStatement(
            condition,
            then_body,
            else_body,
            line,
            column,
            file_name
        )

    def parse_while(self):
        start = self.expect(
            "WHILE"
        )

        self.expect(
            "LPAREN"
        )

        condition = self.parse_expression()

        self.expect(
            "RPAREN"
        )

        body = self.parse_block()

        line, column, file_name = (
            self.location(start)
        )

        return WhileStatement(
            condition,
            body,
            line,
            column,
            file_name
        )

    def parse_for_each(self):
        start = self.expect(
            "FOR_EACH"
        )

        variable = self.expect(
            "IDENTIFIER"
        )

        self.expect(
            "IN"
        )

        iterable = self.parse_expression()

        body = self.parse_block()

        line, column, file_name = (
            self.location(start)
        )

        return ForEachStatement(
            variable.value,
            iterable,
            body,
            line,
            column,
            file_name
        )

    def parse_function_declaration(self):
        start = self.expect(
            "FUNCTION"
        )

        name = self.expect(
            "IDENTIFIER"
        )

        self.expect(
            "LPAREN"
        )

        parameters = []

        token = self.current_token()

        if (
            token is not None
            and token.type != "RPAREN"
        ):
            while True:
                type_token = (
                    self.current_token()
                )

                data_type = self.parse_type()

                parameter_name = self.expect(
                    "IDENTIFIER"
                )

                line, column, file_name = (
                    self.location(type_token)
                )

                parameters.append(
                    FunctionParameter(
                        parameter_name.value,
                        data_type,
                        line,
                        column,
                        file_name
                    )
                )

                token = self.current_token()

                if (
                    token is not None
                    and token.type == "COMMA"
                ):
                    self.advance()
                    continue

                break

        self.expect(
            "RPAREN"
        )

        return_type = None

        token = self.current_token()

        if (
            token is not None
            and token.type == "ARROW"
        ):
            self.advance()
            return_type = self.parse_type()

        body = self.parse_block()

        line, column, file_name = (
            self.location(start)
        )

        return FunctionDeclaration(
            name.value,
            parameters,
            body,
            return_type,
            line,
            column,
            file_name
        )

    def parse_return(self):
        start = self.expect(
            "RETURN"
        )

        expression = self.parse_expression()

        line, column, file_name = (
            self.location(start)
        )

        return ReturnStatement(
            expression,
            line,
            column,
            file_name
        )

    def parse_function_call(self):
        name = self.expect(
            "IDENTIFIER"
        )

        self.expect(
            "LPAREN"
        )

        arguments = []

        token = self.current_token()

        if (
            token is not None
            and token.type != "RPAREN"
        ):
            while True:
                arguments.append(
                    self.parse_expression()
                )

                token = self.current_token()

                if (
                    token is not None
                    and token.type == "COMMA"
                ):
                    self.advance()
                    continue

                break

        self.expect(
            "RPAREN"
        )

        line, column, file_name = (
            self.location(name)
        )

        return FunctionCallExpression(
            name.value,
            arguments,
            line,
            column,
            file_name
        )

    def parse_block(self):
        self.expect(
            "LBRACE"
        )

        statements = []

        while True:
            token = self.current_token()

            if token is None:
                previous = None

                if self.position > 0:
                    previous = self.tokens[
                        self.position - 1
                    ]

                self.error(
                    "} चाहिएको थियो, तर code सकियो।",
                    token=previous
                )

            if token.type == "RBRACE":
                self.advance()
                break

            statements.append(
                self.parse_statement()
            )

        return statements

    def parse_expression(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()

        while True:
            token = self.current_token()

            if (
                token is None
                or token.type != "OR"
            ):
                break

            operator_token = token
            self.advance()

            right = self.parse_and()

            line, column, file_name = (
                self.location(operator_token)
            )

            left = BinaryExpression(
                left,
                "OR",
                right,
                line,
                column,
                file_name
            )

        return left

    def parse_and(self):
        left = self.parse_comparison()

        while True:
            token = self.current_token()

            if (
                token is None
                or token.type != "AND"
            ):
                break

            operator_token = token
            self.advance()

            right = self.parse_comparison()

            line, column, file_name = (
                self.location(operator_token)
            )

            left = BinaryExpression(
                left,
                "AND",
                right,
                line,
                column,
                file_name
            )

        return left

    def parse_comparison(self):
        left = self.parse_addition()

        token = self.current_token()

        if (
            token is not None
            and token.type in (
                "GREATER",
                "LESS",
                "GREATER_EQUAL",
                "LESS_EQUAL",
                "EQUAL_EQUAL",
                "NOT_EQUAL",
            )
        ):
            operator_token = token
            operator = token.type
            self.advance()

            right = self.parse_addition()

            line, column, file_name = (
                self.location(operator_token)
            )

            return BinaryExpression(
                left,
                operator,
                right,
                line,
                column,
                file_name
            )

        return left

    def parse_addition(self):
        left = self.parse_multiplication()

        while True:
            token = self.current_token()

            if (
                token is None
                or token.type not in (
                    "PLUS",
                    "MINUS",
                )
            ):
                break

            operator_token = token
            operator = token.type
            self.advance()

            right = self.parse_multiplication()

            line, column, file_name = (
                self.location(operator_token)
            )

            left = BinaryExpression(
                left,
                operator,
                right,
                line,
                column,
                file_name
            )

        return left

    def parse_multiplication(self):
        left = self.parse_unary()

        while True:
            token = self.current_token()

            if (
                token is None
                or token.type not in (
                    "MULTIPLY",
                    "DIVIDE",
                    "MODULO",
                )
            ):
                break

            operator_token = token
            operator = token.type
            self.advance()

            right = self.parse_unary()

            line, column, file_name = (
                self.location(operator_token)
            )

            left = BinaryExpression(
                left,
                operator,
                right,
                line,
                column,
                file_name
            )

        return left

    def parse_unary(self):
        token = self.current_token()

        if (
            token is not None
            and token.type == "NOT"
        ):
            self.advance()

            expression = self.parse_unary()

            line, column, file_name = (
                self.location(token)
            )

            return UnaryExpression(
                "NOT",
                expression,
                line,
                column,
                file_name
            )

        if (
            token is not None
            and token.type == "MINUS"
        ):
            self.advance()

            expression = self.parse_unary()

            line, column, file_name = (
                self.location(token)
            )

            return UnaryExpression(
                "NEGATIVE",
                expression,
                line,
                column,
                file_name
            )

        return self.parse_power()

    def parse_power(self):
        left = self.parse_primary()

        token = self.current_token()

        if (
            token is not None
            and token.type == "POWER"
        ):
            operator_token = token
            self.advance()

            right = self.parse_unary()

            line, column, file_name = (
                self.location(operator_token)
            )

            return BinaryExpression(
                left,
                "POWER",
                right,
                line,
                column,
                file_name
            )

        return left

    def parse_primary(self):
        token = self.current_token()

        if token is None:
            previous = None

            if self.position > 0:
                previous = self.tokens[
                    self.position - 1
                ]

            self.error(
                "मान चाहिएको थियो, तर code सकियो।",
                token=previous
            )

        line, column, file_name = (
            self.location(token)
        )

        if token.type == "NUMBER":
            self.advance()

            if "." in token.value:
                value = float(
                    token.value
                )
            else:
                value = int(
                    token.value
                )

            expression = NumberExpression(
                value,
                line,
                column,
                file_name
            )

            return self.parse_postfix(
                expression
            )

        if token.type == "STRING":
            self.advance()

            expression = StringExpression(
                token.value[1:-1],
                line,
                column,
                file_name
            )

            return self.parse_postfix(
                expression
            )

        if token.type == "TRUE":
            self.advance()

            return BooleanExpression(
                True,
                line,
                column,
                file_name
            )

        if token.type == "FALSE":
            self.advance()

            return BooleanExpression(
                False,
                line,
                column,
                file_name
            )

        if token.type == "INPUT":
            self.advance()

            self.expect(
                "LPAREN"
            )

            prompt = self.expect(
                "STRING"
            )

            self.expect(
                "RPAREN"
            )

            return InputExpression(
                prompt.value[1:-1],
                line,
                column,
                file_name
            )

        if token.type == "LBRACKET":
            expression = self.parse_list()

            return self.parse_postfix(
                expression
            )

        if token.type == "LBRACE":
            expression = self.parse_map()

            return self.parse_postfix(
                expression
            )

        if token.type == "IDENTIFIER":
            next_token = self.peek_token()

            if (
                next_token is not None
                and next_token.type == "LPAREN"
            ):
                expression = (
                    self.parse_function_call()
                )

                return self.parse_postfix(
                    expression
                )

            self.advance()

            expression = VariableExpression(
                token.value,
                line,
                column,
                file_name
            )

            return self.parse_postfix(
                expression
            )

        if token.type == "LPAREN":
            self.advance()

            expression = self.parse_expression()

            self.expect(
                "RPAREN"
            )

            return self.parse_postfix(
                expression
            )

        self.error(
            f"Expression मा नचिनिएको मान: {token.value}",
            token=token
        )

    def parse_postfix(
        self,
        expression
    ):
        while True:
            token = self.current_token()

            if (
                token is None
                or token.type != "LBRACKET"
            ):
                break

            start = token
            self.advance()

            index = self.parse_expression()

            self.expect(
                "RBRACKET"
            )

            line, column, file_name = (
                self.location(start)
            )

            expression = IndexExpression(
                expression,
                index,
                line,
                column,
                file_name
            )

        return expression

    def parse_list(self):
        start = self.expect(
            "LBRACKET"
        )

        items = []

        token = self.current_token()

        if (
            token is not None
            and token.type != "RBRACKET"
        ):
            while True:
                items.append(
                    self.parse_expression()
                )

                token = self.current_token()

                if (
                    token is not None
                    and token.type == "COMMA"
                ):
                    self.advance()
                    continue

                break

        self.expect(
            "RBRACKET"
        )

        line, column, file_name = (
            self.location(start)
        )

        return ListExpression(
            items,
            line,
            column,
            file_name
        )

    def parse_map(self):
        start = self.expect(
            "LBRACE"
        )

        items = []

        token = self.current_token()

        if (
            token is not None
            and token.type != "RBRACE"
        ):
            while True:
                key = self.expect(
                    "STRING"
                )

                self.expect(
                    "COLON"
                )

                value = self.parse_expression()

                items.append(
                    (
                        key.value[1:-1],
                        value
                    )
                )

                token = self.current_token()

                if (
                    token is not None
                    and token.type == "COMMA"
                ):
                    self.advance()
                    continue

                break

        self.expect(
            "RBRACE"
        )

        line, column, file_name = (
            self.location(start)
        )

        return MapExpression(
            items,
            line,
            column,
            file_name
        )