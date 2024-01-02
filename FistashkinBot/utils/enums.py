import datetime


class Color:
    def get_seasonal_color():
        now = datetime.datetime.now()
        if (now.month == 10 and now.day >= 31) or (now.month == 11 and now.day <= 2):
            return 0xE95230

        elif (
            25 <= now.day <= 31
            and now.month == 12
            or (1 <= now.day <= 15 and now.month == 1)
        ):
            return 0xFFFFFF

        else:
            return 0xA53143

    GRAY = 0x2F3136
    GREEN = 0x00FF00
    RED = 0xFF0000
    MAIN = get_seasonal_color()
    DARK_GRAY = 0x2B2D31


class Enum:
    def format_large_number(self, number):
        str_number = str(number)
        parts = str_number.split(".")
        integer_part = parts[0]
        groups = []
        while len(integer_part) > 0:
            groups.insert(0, integer_part[-3:])
            integer_part = integer_part[:-3]
        formatted_number = " ".join(groups)
        if len(parts) == 2:
            formatted_number += "." + parts[1]

        return formatted_number
