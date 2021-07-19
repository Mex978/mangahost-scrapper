import unidecode


class Functions:
    @staticmethod
    def slugify(value) -> str:
        value = unidecode.unidecode(value)

        value = (
            value.replace("'", "")
            .replace("’", "")
            .replace("!", "")
            .replace("?", "")
            .replace(":", "")
            .replace(",", "")
            .replace("(", "")
            .replace(")", "")
        )

        return "-".join(value.lower().split(" "))
