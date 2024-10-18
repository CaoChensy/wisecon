import unittest


class TestDuckDB(unittest.TestCase):
    def test_duckdb(self):
        """"""
        import duckdb
        r1 = duckdb.sql("SELECT 42 AS i")
        print(r1)
        duckdb.sql("SELECT i * 2 AS k FROM r1").show()

    def test_save(self):
        """"""
        import duckdb
        import pandas as pd
        from sqlalchemy import create_engine

        # 创建示例 DataFrame
        data = {'name': ['Alice', 'Bob', 'Charlie'], 'age': [25, 30, 35]}
        df = pd.DataFrame(data)

        # 创建 DuckDB 数据库连接
        engine = create_engine('duckdb:///my_database.duckdb')  # 或者使用 'duckdb:///path/to/my_database.duckdb'
        # engine = duckdb.connect('my_database.duckdb')

        # 使用 to_sql 将 DataFrame 存入 DuckDB
        df.to_sql('my_table', con=engine, if_exists='replace', index=False)

    def test_read(self):
        """"""
        import pandas as pd
        from sqlalchemy import create_engine

        # 创建 DuckDB 数据库连接
        engine = create_engine('duckdb:///my_database.duckdb')  # 或者使用 'duckdb:///path/to/my_database.duckdb'
        df = pd.read_sql("my_table", con=engine)
        print(df)

    def test_(self):
        """"""
        import pandas as pd
        from sqlalchemy import create_engine

        engine = create_engine('duckdb:////home/data/duckdb/valuation.db')
        df = pd.read_sql("industry", con=engine)
        print(df.shape)
        code = "016029"
        df_code = df[df.BOARD_CODE == code]
        df_code = df_code.sort_values("TRADE_DATE")

