import sqlalchemy
from sqlalchemy.orm import sessionmaker
from model import create_tables, Publisher, Book, Stock, Shop, Sale
import json
import psycopg2

from config import DSN

engine = sqlalchemy.create_engine(DSN)


create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

with open('venv/fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

session.close()

def finde_publisher():
    name_publ = input("Введите имя автора) : ")
    for c in session.query(Publisher).filter(Publisher.name.like(name_publ)).all():
        return c

# print(finde_publisher())

def finde_shop(conn):
    name_publ = input("Введите имя автора) : ")
    with conn.cursor() as cur:
        cur.execute("""SELECT sh.name FROM shop sh
               JOIN stock st ON st.id_shop = sh.id
               JOIN book b ON st.id_book = b.id
               JOIN publisher p ON b.id_publisher = p.id
               WHERE p.name=%s; """, (name_publ,))
        print(cur.fetchone())


with psycopg2.connect(database="HW_BD_6", user="postgres", password="Sergey12") as conn:
    finde_shop(conn)

conn.close()
