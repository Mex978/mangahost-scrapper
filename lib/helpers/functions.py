import unidecode


class Functions:
    @staticmethod
    def slugify(value, special_to_space=False) -> str:
        value = unidecode.unidecode(value)

        if special_to_space:
            value = (
                value.replace("'", " ")
                .replace("!", " ")
                .replace("?", " ")
                .replace("’", " ")
                .replace(":", " ")
                .replace(",", " ")
                .replace("(", " ")
                .replace(")", " ")
            )
        else:
            value = (
                value.replace("'", "")
                .replace("!", "")
                .replace("?", "")
                .replace(":", "")
                .replace(",", "")
                .replace("(", "")
                .replace(")", "")
            )

        return "-".join(value.lower().split(" "))
