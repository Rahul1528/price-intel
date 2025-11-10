import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
from sqlalchemy.sql import select

DB_FILENAME = os.path.join(os.path.dirname(__file__), "price_intel.db")
ENGINE = create_engine(f"sqlite:///{DB_FILENAME}", connect_args={"check_same_thread": False})
META = MetaData()

products = Table(
    "products", META,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("keyword", String, index=True),
    Column("title", String),
    Column("price", Float),
    Column("currency", String),
    Column("link", String),
    Column("source", String),
    Column("scraped_at", DateTime),
)

def init_db():
    META.create_all(ENGINE)

def insert_many(rows):
    with ENGINE.connect() as conn:
        conn.execute(products.insert(), rows)
        conn.commit()

def fetch_by_keyword(keyword):
    with ENGINE.connect() as conn:
        q = select(products).where(products.c.keyword == keyword)
        res = conn.execute(q).fetchall()
        return [dict(r) for r in res]

def clear_keyword(keyword):
    with ENGINE.connect() as conn:
        conn.execute(products.delete().where(products.c.keyword == keyword))
        conn.commit()
