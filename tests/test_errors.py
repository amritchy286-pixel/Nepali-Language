import unittest

from src.errors import RuntimeLanguageError
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


class NepaliLanguageErrorTests(unittest.TestCase):
    def run_nep(
        self,
        source,
        file_name="error-test.nep"
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

        statements = parser.parse()

        interpreter = Interpreter()

        interpreter.run(
            statements
        )

        return interpreter

    def test_division_by_zero(self):
        with self.assertRaises(
            RuntimeLanguageError
        ) as context:
            self.run_nep(
                """
दशमलव नतिजा = 10 / 0
"""
            )

        message = str(
            context.exception
        )

        self.assertIn(
            "शून्यले भाग गर्न मिल्दैन",
            message
        )

        self.assertIn(
            "error-test.nep",
            message
        )

    def test_modulo_by_zero(self):
        with self.assertRaises(
            RuntimeLanguageError
        ) as context:
            self.run_nep(
                """
पूर्णाङ्क नतिजा = 10 % 0
"""
            )

        message = str(
            context.exception
        )

        self.assertIn(
            "शून्यले modulo गर्न मिल्दैन",
            message
        )

        self.assertIn(
            "error-test.nep",
            message
        )

    def test_list_index_out_of_range(self):
        with self.assertRaises(
            RuntimeLanguageError
        ) as context:
            self.run_nep(
                """
सूची फलहरू = ["स्याउ", "केरा"]
पाठ फल = फलहरू[10]
"""
            )

        message = str(
            context.exception
        )

        self.assertIn(
            "Index सीमा बाहिर छ",
            message
        )

        self.assertIn(
            "error-test.nep",
            message
        )

    def test_missing_import(self):
        with self.assertRaises(
            RuntimeLanguageError
        ) as context:
            self.run_nep(
                """
प्रयोग "योमोड्युलछैन"
"""
            )

        message = str(
            context.exception
        )

        self.assertIn(
            "Import file वा module भेटिएन",
            message
        )

        self.assertIn(
            "error-test.nep",
            message
        )


if __name__ == "__main__":
    unittest.main()