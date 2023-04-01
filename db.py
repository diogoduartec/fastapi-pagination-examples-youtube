from sqlalchemy import Column, String, Integer, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///.db')
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = 'products'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String)
    price = Column('price', Float)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

session = SessionLocal()
session.add_all([
    ProductModel(name=f'Flamengo {n}', price=n * .1)
    for n in range(100)
])
session.commit()
session.close()
