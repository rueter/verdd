from django.db import models
from django.utils.encoding import smart_str


class BinaryCharField(models.CharField):
    ''' A field to use when using VARBINARY in MySQL.

    MySQL by default (even when using utf8) ignores accented letters when comparing/searching for text:
        https://stackoverflow.com/questions/43626573/duplicate-unicode-entry-error-on-the-unique-column-mysql
    Also, it ignores trailing spaces when applying unique constraints:
        https://stackoverflow.com/questions/11714534/mysql-database-with-unique-fields-ignored-ending-spaces

    A solution is to set the default collate of the table to utf8_bin and use VARBINARY as a field instead of VARCHAR.
    '''

    def to_python(self, value):
        if isinstance(value, str) or value is None:
            return value
        return smart_str(str(value))  # to support utf8_bin in MySQL databases
