import polars as pl

import os

print(os.getcwd())

query = 'SELECT * FROM articles'
uri = 'sqlite:///kosha-deaths.db'

df = pl.read_database(
    query=query,
    connection_uri=uri,
    engine='adbc')

print(df)
