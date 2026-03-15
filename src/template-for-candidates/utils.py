from contextlib import closing
import functools
from pathlib import Path
import sqlite3
from typing import Callable, TypeVar
from variables import STATEMENTS_PATH, OUTPUT_PATH

# Do not edit

FunctionType = TypeVar("FunctionType", bound=Callable)


def database_operation(function: FunctionType) -> FunctionType:
    """
    A decorator that provides a `sqlite3.Cursor` to the function it decorates, under the keyword `cursor`

    ```python
    @database_operation
    def my_function(cursor):
        cursor.execute("SELECT * FROM my_table")
        ...

    # Example usage
    if __name__ == "__main__":
        my_function()
    """

    @functools.wraps(function)
    def _wrapped(*args, **kwargs):
        with closing(sqlite3.connect(OUTPUT_PATH / "earthquakes.db")) as connection:
            with connection:
                return function(*args, **kwargs, cursor=connection.cursor())

    return _wrapped


def _load_statement_from_file(file: str) -> str:
    with open(STATEMENTS_PATH / file, encoding="utf-8") as f:
        return f.read()


def load_statements(
    *statement_args: str, **statement_kwargs: str
) -> Callable[[FunctionType], FunctionType]:
    """
    A decorator that loads SQL statements from files and provides it as a keyword argument to the function it decorates. Unless specified the keyword name is the name of the file, minus the `.sql` extension

    ```python
    # Default keyword name: filename minus the `.sql` extension
    @load_statements("sql/folder/statement.sql")
    def my_function_1(statement):
        print(statement)


    # Renamed keyword
    @load_statements(rename_the_keyword="sql/folder/statement.sql")
    def my_function_2(rename_the_keyword):
        print(rename_the_keyword)


    # Multiple statements
    @load_statements(
        "sql/folder/statement.sql",
        other_statement="sql/folder/statement_2.sql",
    )
    def my_function_3(statement, other_statement):
        print(statement, other_statement)


    # Usage
    if __name__ == "__main__":
        my_function_1()
        my_function_2()
        my_function_3()
    """
    statements_from_args = {
        Path(file).stem: _load_statement_from_file(file) for file in statement_args
    }
    statements_from_kwargs = {
        key: _load_statement_from_file(file) for key, file in statement_kwargs.items()
    }

    def _wrapper(function: FunctionType) -> FunctionType:
        @functools.wraps(function)
        def _wrapped(*args, **kwargs):
            return function(
                *args, **kwargs, **statements_from_args, **statements_from_kwargs
            )

        return _wrapped

    return _wrapper
