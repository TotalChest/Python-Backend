import re

import psycopg2

import config
from datatypes import Integer, Float, String, Text, Bool
import logger


logger = logger.get_logger(__name__)

def camel_to_snake_case(string):
    result = ''
    for s in re.split('([A-Z])', string):
        if s:
            if len(s) == 1 and s.isupper():
                result += '_' + s.lower()
            elif len(s) > 1 and s.islower():
                result += s
    return result.strip('_')



class SQLQuery:
    SELECT = '''
        SELECT {fields}
        FROM {table};
    '''
    SELECT_WHERE = '''
        SELECT {fields}
        FROM {table}
        WHERE {conds};
    '''
    SELECT_ID = '''
        SELECT {fields}
        FROM {table}
        WHERE id={id};
    '''
    DELETE = '''
        DELETE FROM {table}
        WHERE {conds};
    '''
    DELETE_ID = '''
        DELETE FROM {table}
        WHERE id={id};
    '''
    DROP = '''
        DROP TABLE IF EXISTS {table};
    '''
    UPDATE = '''
        UPDATE {table}
        SET {conds}
        WHERE id={id};
    '''
    INSERT = '''
        INSERT INTO {table} ({fields})
        VALUES ({values})
        RETURNING id;
    '''
    CREATE = '''
        CREATE TABLE {table} (
            {fields},
            id SERIAL PRIMARY KEY
        );
    '''
    EXISTS = '''
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name='{table}'
        AND table_type='BASE TABLE';
    '''

    @classmethod
    def select(cls, **kwargs):
        return cls.SELECT.format(**kwargs)

    @classmethod
    def select_where(cls, **kwargs):
        return cls.SELECT_WHERE.format(**kwargs)

    @classmethod
    def select_id(cls, **kwargs):
        return cls.SELECT_ID.format(**kwargs)

    @classmethod
    def delete(cls, **kwargs):
        return cls.DELETE.format(**kwargs)

    @classmethod
    def delete_id(cls, **kwargs):
        return cls.DELETE_ID.format(**kwargs)

    @classmethod
    def drop(cls, **kwargs):
        return cls.DROP.format(**kwargs)

    @classmethod
    def update(cls, **kwargs):
        return cls.UPDATE.format(**kwargs)

    @classmethod
    def insert(cls, **kwargs):
        return cls.INSERT.format(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        return cls.CREATE.format(**kwargs)

    @classmethod
    def exists(cls, **kwargs):
        return cls.EXISTS.format(**kwargs)


class TableExists(Exception):
    '''A table in a PostgreSQL database already exists'''
    pass


class TableNotFound(Exception):
    '''A table in a PostgreSQL database doesn't exist'''
    pass


class MethodUsageError(Exception):
    '''Wrong arguments instantiation, another method should be used'''
    pass

class NotNullFieldError(Exception):
    '''A field in a PostgreSQL database table is "NOT NULL"'''
    pass


class Connection:
    '''
    Class for connections to PostgreSQL databases.
    '''

    def __init__(self, **db_data):
        logger.info("Setting the connection to database...")
        self.db = psycopg2.connect(**db_data)
        self.cursor = self.db.cursor()
        logger.info("Connection setup done.")

    def execute(self, query):
        logged_query = query.replace('\n', ' ')
        while '  ' in logged_query:
            logged_query = logged_query.replace('  ', ' ')
        if len(logged_query) > 40:
            logged_query = f"{logged_query[:40]}..."
        logger.info(f"SQL query execution: {logged_query}")

        self.cursor.execute(query)
        self.db.commit()

    def close(self):
        self.db.close()
        logger.info("Connection closed.")


class MetaORM(type):
    '''
    Metaclass for PostgreSQL database ORMs.
    '''

    def __new__(cls, name, bases, attrs):
        attrs['_table_name'] = camel_to_snake_case(name)
        fields = dict()
        for field, value in attrs.items():
            if not field.startswith('_') and \
               isinstance(value, (Integer, Float, String, Text, Bool)):
                fields[field] = value
        attrs['_fields'] = fields
        return super().__new__(cls, name, bases, attrs)


class DatabaseORM(metaclass=MetaORM):
    '''
    Implementation for PostgreSQL database ORM.
    '''

    def __init__(self, **kwargs):
        self.conn = Connection(**config.db_data)
        self.id = None
        for key, val in self._fields.items():
            setattr(self, key, kwargs.get(key, val.default))
        logger.info("Table ORM initialized.")

    def create(self, force=False):
        query = SQLQuery.exists(table=self._table_name)
        self.conn.execute(query)
        exists = self.conn.cursor.fetchone()[0]
        if exists and not force:
            logger.error(f"Failed to create the table '{self._table_name}'.")
            raise TableExists(f'A table with name "{self._table_name}" '
                              'already exists.')
        fields = ',\n'.join(f'{key} {val.sql_datatype}'
                            for key, val in self._fields.items())
        query = SQLQuery.create(table=self._table_name, fields=fields)
        self.conn.execute(query)
        logger.info(f"Table '{self._table_name}' was created successfully.")

    def drop(self, silent=False):
        query = SQLQuery.exists(table=self._table_name)
        self.conn.execute(query)
        exists = self.conn.cursor.fetchone()[0]
        if not exists and not silent:
            logger.error(f"Failed to drop the table '{self._table_name}'.")
            raise TableNotFound(f'A table with name "{self._table_name}" '
                                'doesn\'t exist.')
        query = SQLQuery.drop(table=self._table_name)
        self.conn.execute(query)
        logger.info(f"Table '{self._table_name}' was dropped successfully.")

    def insert(self, **kwargs):
        obj = self.__class__(**kwargs)
        obj.save()
        logger.info(f"Inserted a row into the table '{self._table_name}'.")

    def insert_many(self, rows):
        for row in rows:
            self.insert(**row)

    def save(self):
        query = SQLQuery.exists(table=self._table_name)
        self.conn.execute(query)
        exists = self.conn.cursor.fetchone()[0]
        if not exists:
            logger.error(f"Failed to save the table '{self._table_name}'.")
            raise TableNotFound(f'A table with name "{self._table_name}" '
                                'doesn\'t exist.')
        if self.id is None:
            self._save()
        else:
            self._update()
        logger.info(f"Table '{self._table_name}' was saved successfully.")

    def delete(self, **kwargs):
        fields = ['id'] + list(self._fields.keys())
        conds = '\nAND '.join(f'{key}={"NULL" if val is None else repr(val)}'
                              for key, val in kwargs.items()
                              if key in fields)
        if conds:
            query = SQLQuery.delete(table=self._table_name, conds=conds)
        else:
            query = SQLQuery.delete_id(table=self._table_name, id=self.id)
        self.conn.execute(query)
        logger.info(f"Deleted rows from the table '{self._table_name}'.")

    def _save(self):
        fields = list(self._fields.keys())
        reprs = []
        for key in fields:
            val = getattr(self, key)
            if self._fields[key].not_null and val is None:
                logger.error(f"Attempted to save a row into the table "
                             f"'{self._table_name}' with None values for "
                             "keys which are \"NOT NULL\".")
                raise NotNullFieldError(f'The field "{key}" is not nullable.')
            reprs.append("NULL" if val is None else repr(val))
        values = ', '.join(reprs)
        query = SQLQuery.insert(table=self._table_name,
                                fields=', '.join(fields),
                                values=values)
        self.conn.execute(query)
        self.id = self.conn.cursor.fetchone()[0]

    def _update(self):
        conds = ',\n'.join(f'{key}={"NULL" if val is None else repr(val)}'
                           for key, val in self._fields.items())
        query = SQLQuery.update(table=self._table_name,
                                conds=conds,
                                id=self.id)
        self.conn.execute(query)

    def get(self, id=None, **kwargs):
        if id is not None:
            fields = list(self._fields.keys())
            query = SQLQuery.select_id(table=self._table_name,
                                       fields=', '.join(fields),
                                       id=self.id)
        else:
            fields = ['id'] + list(self._fields.keys())
            pairs = [(key, val)
                     for key, val in kwargs.items()
                     if key in self._fields.keys()]
            if not pairs:
                logger.error(f"Method get() used instead of all() "
                             f"for the table '{self._table_name}'.")
                raise MethodUsageError("No valid kwargs were forwarded to get().\n"
                                       "Try 'all' method if they're "
                                       "not supposed to be forwarded")
            conds = '\nAND '.join(f'{key}={"NULL" if val is None else repr(val)}'
                                  for key, val in pairs)
            query = SQLQuery.select_where(table=self._table_name,
                                          fields=', '.join(fields),
                                          conds=conds)
        self.conn.execute(query)
        result = self.conn.cursor.fetchone()
        obj = self.__class__.row_to_object(result, fields)
        if obj is not None:
            obj.id = id
        logger.info(f"Table '{self._table_name}' -> get().")
        return obj

    def all(self, **kwargs):
        fields = ['id'] + list(self._fields.keys())
        if kwargs:
            pairs = [(key, val)
                     for key, val in kwargs.items()
                     if key in self._fields.keys()]
            conds = '\nAND '.join(f'{key}={"NULL" if val is None else repr(val)}'
                                  for key, val in pairs)
            query = SQLQuery.select_where(table=self._table_name,
                                          fields=', '.join(fields),
                                          conds=conds)
        else:
            query = SQLQuery.select(table=self._table_name,
                                    fields=', '.join(fields))
        self.conn.execute(query)
        results = self.conn.cursor.fetchall()
        logger.info(f"Table '{self._table_name}' -> all().")
        for row in results:
            obj = self.__class__.row_to_object(row, fields)
            yield obj

    @classmethod
    def row_to_object(cls, row, fields):
        if row is not None:
            obj = cls()
            for i, field in enumerate(row):
                setattr(obj, fields[i], field)
            return obj

    def pretty_repr(self):
        return '\n'.join(f'{key}: {getattr(self, key)}'
                         for key in self._fields)
