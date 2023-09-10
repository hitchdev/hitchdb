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
