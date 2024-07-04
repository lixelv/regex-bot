import json
import re

re.compile

re_flags = {
    "default": 0,  # Не учитывать флаги по умолчанию
    "ignore_case": re.IGNORECASE,  # Игнорирование регистра (например, 'a' будет совпадать с 'A')
    "multiline": re.MULTILINE,  # Многострочный режим (символ ^ совпадает с началом каждой строки, а $ с концом каждой строки)
    "dot_all": re.DOTALL,  # Символ . будет совпадать с любым символом, включая новую строку
    "verbose": re.VERBOSE,  # Позволяет использовать расширенные регулярные выражения (с комментариями и пробелами)
    "unicode": re.UNICODE,  # Позволяет использовать правила Юникода для \w, \W, \b, \B, \d, \D, \s и \S (включено по умолчанию в Python 3)
    "ascii": re.ASCII,  # Использует ASCII-совместимые правила для \w, \W, \b, \B, \d, \D, \s и \S (в Python 3)
    "locale": re.LOCALE,  # Использует правила текущей локали для \w, \W, \b, \B, \s и \S (в Python 2 и 3)
}

with open(".env", "r", encoding="utf-8") as f:
    environment = dict()

    for line in f.readlines():
        if line.strip() != "":
            key = line.split("=")[0].strip()
            value = line.split("=")[1].strip()

            environment[key] = value


class Lexicon:
    def __init__(self):
        with open("lexicon.json", "r", encoding="utf-8") as f:
            self.lexicon = json.load(f)

    def get(self, key, lang):
        return (self.lexicon.get(lang) or self.lexicon.get("en"))[key]
