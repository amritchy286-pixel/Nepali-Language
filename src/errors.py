class NepaliLanguageError(Exception):
    def __init__(
        self,
        message,
        file_name=None,
        line=None,
        column=None
    ):
        self.message = message
        self.file_name = file_name
        self.line = line
        self.column = column

        super().__init__(self.format_message())

    def format_message(self):
        location_parts = []

        if self.file_name:
            location_parts.append(
                f"फाइल: {self.file_name}"
            )

        if self.line is not None:
            location_parts.append(
                f"लाइन: {self.line}"
            )

        if self.column is not None:
            location_parts.append(
                f"स्तम्भ: {self.column}"
            )

        if location_parts:
            location = " | ".join(location_parts)

            return (
                f"{self.message}\n"
                f"{location}"
            )

        return self.message


class LexerError(NepaliLanguageError):
    pass


class ParserError(NepaliLanguageError):
    pass


class RuntimeLanguageError(NepaliLanguageError):
    pass