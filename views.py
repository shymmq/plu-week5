from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

import crud
import schemas
from db import get_db

router = APIRouter()


@router.get("/suppliers/{supplier_id}", response_model=schemas.SupplierFull)
async def get_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.get("/suppliers", response_model=List[schemas.SupplierShort])
async def get_suppliers(db: Session = Depends(get_db)):
    db_suppliers = crud.get_suppliers(db)

    return db_suppliers


@router.post("/suppliers", status_code=201, response_model=schemas.SupplierFull)
async def insert_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    return crud.insert_supplier(db, supplier)


@router.put("/suppliers/{supplier_id}", status_code=200, response_model=schemas.SupplierFull)
async def update_supplier(supplier_id, new_props: schemas.SupplierUpdate, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return crud.update_supplier(db, supplier_id, new_props)


@router.delete("/suppliers/{supplier_id}", status_code=204)
async def delete_supplier(supplier_id, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    crud.delete_supplier(db, supplier_id)


@router.get("/suppliers/{supplier_id}/products")
async def get_products_for_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return crud.get_products_for_supplier(db, supplier_id)
