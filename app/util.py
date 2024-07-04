import re


def regex_compile(command, text, pattern, flag):
    pattern = re.compile(pattern, flags=flag)
    match command:
        case "find":
            result = (re.findall(pattern, text) or [None])[0]

            if result is None:
                return False

            return "\n```\n" + str(result) + "\n```"

        case "findall":
            result = re.findall(pattern, text) or None

            if result is None:
                return False

            return "\n```\n" + "\n".join([str(i) for i in result]) + "\n```"
