from database import Base, engine
from models import Item

print("Creating db")

Base.metadata.create_all(engine)