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


@router.get("/suppliers/{supplier_id}/products")
async def get_products_for_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return crud.get_products_for_supplier(db, supplier_id)
