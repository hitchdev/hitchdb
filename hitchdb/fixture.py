from hitchdb.utils import sqlformat


INSERT_INTO = """
INSERT INTO {table_name} ({column_list})
VALUES
    {value_list}
"""


VALUE_LINE = """({pk}, {row}),\n    """


LAST_VALUE_LINE = """({pk}, {row});\n"""


class Fixture:
    def __init__(self, fixture_dict, tbls_config):
        self._fix_dict = fixture_dict
        self._tbls_config = tbls_config

    def _value_list(self, table, data_dict, column_list):
        tbl = self._tbls_config._tbl_dict[table]
        sql_text = ""
        items = list(data_dict.items())

        for pk, data in items[:-1]:
            sql_text += VALUE_LINE.format(
                pk=sqlformat(pk),
                row=", ".join([sqlformat(x) for x in tbl.row_list(data)]),
            )

        pk, data = items[-1]
        sql_text += LAST_VALUE_LINE.format(
            pk=sqlformat(pk), row=", ".join([sqlformat(x) for x in tbl.row_list(data)])
        )

        return sql_text

    def sql(self):
        sql_text = ""

        for table, data_dict in self._fix_dict.items():
            column_list = self._tbls_config.column_list(table)
            sql_text += INSERT_INTO.format(
                table_name=table,
                column_list=", ".join(column_list),
                value_list=self._value_list(table, data_dict, column_list),
            )

        return sql_text
