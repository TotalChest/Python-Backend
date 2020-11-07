import logger


logger = logger.get_logger(__name__)

class Integer:
    def __init__(self, not_null=False, non_negative=False, default=None):
        self.not_null = not_null
        self.non_negative = non_negative
        self.default = default
        self.sql_datatype = 'INT' + (' NOT NULL' if not_null else '')

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value is not None:
            if not isinstance(value, int):
                logger.error(f"Field '{self.name}' should be integer!")
                raise ValueError('Value should be integer.')
            if self.non_negative and value < 0:
                logger.error(f"Field '{self.name}' should be non-negative!")
                raise ValueError('Value should be non-negative.')
        instance.__dict__[self.name] = value


class Float:
    def __init__(self, not_null=False, non_negative=False, default=None):
        self.not_null = not_null
        self.non_negative = non_negative
        self.default = default
        self.sql_datatype = 'FLOAT' + (' NOT NULL' if not_null else '')

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value is not None:
            if not isinstance(value, float):
                logger.error(f"Field '{self.name}' should be float!")
                raise ValueError('Value should be float.')
            if self.non_negative and value < 0:
                logger.error(f"Field '{self.name}' should be non-negative!")
                raise ValueError('Value should be non-negative.')
        instance.__dict__[self.name] = value


class String:
    def __init__(self, max_len=255, not_null=False, default=None):
        self.max_len = max_len
        self.not_null = not_null
        self.default = default
        self.sql_datatype = f'CHAR({self.max_len})' + \
                            (' NOT NULL' if not_null else '')

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value is not None:
            if not isinstance(value, str):
                logger.error(f"Field '{self.name}' should be string!")
                raise ValueError('Value should be string.')
            if len(value) > self.max_len:
                logger.error(f"Length of field '{self.name}' cannot exceed "
                               f"{self.max_len}!")
                raise ValueError('Length of value cannot exceed '
                                 f'{self.max_len}.')
        instance.__dict__[self.name] = value


class Text:
    def __init__(self, not_null=False, default=None):
        self.not_null = not_null
        self.default = default
        self.sql_datatype = 'TEXT' + (' NOT NULL' if not_null else '')

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value is not None:
            if not isinstance(value, str):
                logger.error(f"Field '{self.name}' should be text!")
                raise ValueError('Value should be text.')
        instance.__dict__[self.name] = value


class Bool:
    def __init__(self, not_null=False, default=None):
        self.not_null = not_null
        self.default = default
        self.sql_datatype = 'BOOLEAN' + (' NOT NULL' if not_null else '')

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value is not None:
            if not isinstance(value, bool):
                logger.error(f"Field '{self.name}' should be boolean!")
                raise ValueError('Value should be boolean.')
        instance.__dict__[self.name] = value
