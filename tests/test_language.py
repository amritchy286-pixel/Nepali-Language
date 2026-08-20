import os
import tempfile
import unittest

from src.errors import RuntimeLanguageError
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


class NepaliLanguageTests(unittest.TestCase):
    def run_nep(
        self,
        source,
        file_name="test.nep",
        base_directory=None
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

        interpreter = Interpreter(
            base_directory=base_directory
        )

        interpreter.run(
            statements
        )

        return interpreter

    def test_integer_variable(self):
        interpreter = self.run_nep(
            """
पूर्णाङ्क संख्या = 10
"""
        )

        self.assertEqual(
            interpreter.variables["संख्या"],
            10
        )

    def test_addition(self):
        interpreter = self.run_nep(
            """
पूर्णाङ्क क = 10
पूर्णाङ्क ख = 20
पूर्णाङ्क जम्मा = क + ख
"""
        )

        self.assertEqual(
            interpreter.variables["जम्मा"],
            30
        )

    def test_modulo(self):
        interpreter = self.run_nep(
            """
पूर्णाङ्क क = 10 % 3
पूर्णाङ्क ख = 20 % 2
पूर्णाङ्क ग = 7 % 2
"""
        )

        self.assertEqual(
            interpreter.variables["क"],
            1
        )

        self.assertEqual(
            interpreter.variables["ख"],
            0
        )

        self.assertEqual(
            interpreter.variables["ग"],
            1
        )

    def test_power_operator(self):
        interpreter = self.run_nep(
            """
पूर्णाङ्क क = 2 ^ 3
पूर्णाङ्क ख = 5 ^ 2
पूर्णाङ्क ग = 10 ^ 0
पूर्णाङ्क घ = 2 ^ 3 ^ 2
"""
        )

        self.assertEqual(
            interpreter.variables["क"],
            8
        )

        self.assertEqual(
            interpreter.variables["ख"],
            25
        )

        self.assertEqual(
            interpreter.variables["ग"],
            1
        )

        self.assertEqual(
            interpreter.variables["घ"],
            512
        )

    def test_boolean(self):
        interpreter = self.run_nep(
            """
सत्य सक्रिय = सही
"""
        )

        self.assertTrue(
            interpreter.variables["सक्रिय"]
        )

    def test_list(self):
        interpreter = self.run_nep(
            """
सूची फलहरू = ["स्याउ", "केरा"]
"""
        )

        self.assertEqual(
            interpreter.variables["फलहरू"],
            ["स्याउ", "केरा"]
        )

    def test_list_index(self):
        interpreter = self.run_nep(
            """
सूची फलहरू = ["स्याउ", "केरा"]
पाठ फल = फलहरू[1]
"""
        )

        self.assertEqual(
            interpreter.variables["फल"],
            "केरा"
        )

    def test_map(self):
        interpreter = self.run_nep(
            """
नक्सा प्रयोगकर्ता = {
    "नाम": "अमृत",
    "उमेर": 25
}
"""
        )

        self.assertEqual(
            interpreter.variables[
                "प्रयोगकर्ता"
            ]["नाम"],
            "अमृत"
        )

        self.assertEqual(
            interpreter.variables[
                "प्रयोगकर्ता"
            ]["उमेर"],
            25
        )

    def test_function(self):
        interpreter = self.run_nep(
            """
काम जोड(
    पूर्णाङ्क क,
    पूर्णाङ्क ख
) -> पूर्णाङ्क {
    फर्काऊ क + ख
}

पूर्णाङ्क नतिजा = जोड(10, 20)
"""
        )

        self.assertEqual(
            interpreter.variables["नतिजा"],
            30
        )

    def test_while_loop(self):
        interpreter = self.run_nep(
            """
पूर्णाङ्क संख्या = 0

जब (संख्या < 3) {
    संख्या = संख्या + 1
}
"""
        )

        self.assertEqual(
            interpreter.variables["संख्या"],
            3
        )

    def test_for_each_loop(self):
        interpreter = self.run_nep(
            """
सूची अंकहरू = [1, 2, 3]
पूर्णाङ्क जम्मा = 0

हरेक अंक मा अंकहरू {
    जम्मा = जम्मा + अंक
}
"""
        )

        self.assertEqual(
            interpreter.variables["जम्मा"],
            6
        )

    def test_else_natra(self):
        interpreter = self.run_nep(
            """
पूर्णाङ्क संख्या = 5
पाठ नतिजा = "खाली"

यदि (संख्या > 10) {
    नतिजा = "ठूलो"
} नत्र {
    नतिजा = "सानो"
}
"""
        )

        self.assertEqual(
            interpreter.variables["नतिजा"],
            "सानो"
        )

    def test_else_anyatha(self):
        interpreter = self.run_nep(
            """
पूर्णाङ्क उमेर = 25
पाठ नतिजा = "खाली"

यदि (उमेर >= 18) {
    नतिजा = "वयस्क"
} अन्यथा {
    नतिजा = "नाबालक"
}
"""
        )

        self.assertEqual(
            interpreter.variables["नतिजा"],
            "वयस्क"
        )

    def test_runtime_error_location(self):
        source = """
देखाऊ(नभएकोVariable)
"""

        with self.assertRaises(
            RuntimeLanguageError
        ) as context:
            self.run_nep(
                source,
                file_name="runtime-test.nep"
            )

        message = str(
            context.exception
        )

        self.assertIn(
            "Variable भेटिएन",
            message
        )

        self.assertIn(
            "runtime-test.nep",
            message
        )

    def test_import(self):
        with tempfile.TemporaryDirectory() as temp:
            math_file = os.path.join(
                temp,
                "गणित.nep"
            )

            with open(
                math_file,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(
                    """
काम जोड(
    पूर्णाङ्क क,
    पूर्णाङ्क ख
) -> पूर्णाङ्क {
    फर्काऊ क + ख
}
"""
                )

            source = """
प्रयोग "गणित.nep"

पूर्णाङ्क नतिजा = जोड(5, 7)
"""

            interpreter = self.run_nep(
                source,
                file_name=os.path.join(
                    temp,
                    "main.nep"
                ),
                base_directory=temp
            )

            self.assertEqual(
                interpreter.variables["नतिजा"],
                12
            )

    def test_number_standard_library(self):
        project_root = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                ".."
            )
        )

        source = """
प्रयोग "संख्या"

सत्य क = जोर(10)
सत्य ख = जोर(7)
सत्य ग = बिजोर(7)
सत्य घ = बिजोर(10)
"""

        interpreter = self.run_nep(
            source,
            file_name=os.path.join(
                project_root,
                "number-stdlib-test.nep"
            ),
            base_directory=project_root
        )

        self.assertTrue(
            interpreter.variables["क"]
        )

        self.assertFalse(
            interpreter.variables["ख"]
        )

        self.assertTrue(
            interpreter.variables["ग"]
        )

        self.assertFalse(
            interpreter.variables["घ"]
        )

    def test_math_standard_library_power(self):
        project_root = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                ".."
            )
        )

        source = """
प्रयोग "गणित"

पूर्णाङ्क क = घात(2, 3)
पूर्णाङ्क ख = घात(5, 2)
पूर्णाङ्क ग = घात(10, 0)
"""

        interpreter = self.run_nep(
            source,
            file_name=os.path.join(
                project_root,
                "math-stdlib-test.nep"
            ),
            base_directory=project_root
        )

        self.assertEqual(
            interpreter.variables["क"],
            8
        )

        self.assertEqual(
            interpreter.variables["ख"],
            25
        )

        self.assertEqual(
            interpreter.variables["ग"],
            1
        )


if __name__ == "__main__":
    unittest.main()