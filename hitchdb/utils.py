from slugify import slugify
import re


def readable(name):
    """
    Formulate a readable equivalent of column and table
    names, whether they use camelCase or underscore_case.

    >>> readable("firstNameAndLastName")
    'first name and last name'

    >>> readable("first_name_and_last_name")
    'first name and last name'
    """
    return slugify(re.sub(re.compile("([a-z])([A-Z])"), r"\1 \2", name)).replace(
        "-", " "
    )


def sqlformat(scalar):
    """
    >>> sqlformat("hello")
    "'hello'"

    >>> sqlformat(45)
    '45'

    >>> sqlformat(45.3)
    '45.3'

    >>> sqlformat(True)
    'true'

    >>> sqlformat(False)
    'false'

    >>> sqlformat(None)
    'null'
    """
    if isinstance(scalar, str):
        return "'{}'".format(sqlescape(scalar))
    elif scalar is None:
        return "null"
    elif isinstance(scalar, bool):
        return "true" if scalar else "false"
    elif isinstance(scalar, int):
        return str(scalar)
    elif isinstance(scalar, float):
        return str(scalar)
    else:
        raise NotImplementedError(f"Unimplemented type: {type(scalar)}")


def sqlescape(sql):
    """
    Escape an SQL string.

    >>> sqlescape("O'Connor")
    "O''Connor"

    >>> sqlescape("\\n")
    '\\\\n'
    """
    return sql.translate(
        sql.maketrans(
            {
                "'": "''",
            }
        )
    )
