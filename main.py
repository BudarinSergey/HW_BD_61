import sqlalchemy
from sqlalchemy.orm import sessionmaker
from model import create_tables, Publisher, Book, Stock, Shop, Sale
import json

DSN = 'postgresql://postgres:Sergey12@localhost:5432/HW_BD_6'
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

print(finde_publisher())

