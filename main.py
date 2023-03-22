from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import SessionLocal

import models

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    desc: str
    price: int
    on_offer: bool
    
    class config:
        orm_mode=True
        

db = SessionLocal()
        
        
@app.get("/items", status_code=status.HTTP_200_OK)
async def get_all_items():
    items = db.query(models.Item).all()
    return items

@app.get("/item/{item_id}", status_code=status.HTTP_200_OK)
async def get_an_item(item_id: int):
    item = db.query(models.Item).filter(models.Item.id==item_id).first()

    if item is None:
        raise HTTPException(detail="Item was not found", status_code=status.HTTP_204_NO_CONTENT)
    
    return item
    
@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_an_item(item: Item):
    
    db_item = db.query(models.Item).filter(models.Item.name==item.name).first()
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Item exists")
    
    new_item = models.Item(
        name = item.name,
        price = item.price,
        desc = item.desc,
        on_offer = item.on_offer
    )
    
    
    db.add(new_item)
    db.commit()
    return new_item

@app.put("/item/{item_id}", status_code=status.HTTP_200_OK)
async def update_an_item(item_id: int, item: Item):
    item_to_update = db.query(models.Item).filter(models.Item.id==item_id).first()
    
    if item_to_update is None:
        raise HTTPException(detail="Item was not found", status_code=status.HTTP_204_NO_CONTENT)
    
    item_to_update.name = item.name
    item_to_update.price = item.price
    item_to_update.desc = item.desc
    item_to_update.on_offer = item.on_offer
    
    db.commit()
    return item_to_update

@app.delete("/item/{item_id}")
async def delete_item(item_id: int):
    item_to_delete = db.query(models.Item).filter(models.Item.id==item_id).first()
    
    if item_to_delete is None:
        raise HTTPException(detail="Item was not found", status_code=status.HTTP_204_NO_CONTENT)
    
    db.delete(item_to_delete)
    db.commit()
    
    return item_to_delete