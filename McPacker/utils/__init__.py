
def version_to_int(version: str) -> int:
    string = version.replace(".", "0")
    new_string = ""

    for char in string:
        to_add = char

        try:
            int(char)

        except Exception as err:
            char_int = {
                "a": "0",
                "b": "1",
                "c": "2"
            }.get(char)

            if char_int:
                to_add = char_int

        new_string += to_add

    try:
        new_string = new_string.split("-")[-1]
        new_string = new_string.split("+")[0]

        return int(new_string)

    except Exception as err:
        return 0
