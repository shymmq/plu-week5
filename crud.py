from pydantic import PositiveInt
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload, load_only

import models
import schemas


def get_suppliers(db: Session):
    return db.query(models.Supplier.SupplierID, models.Supplier.CompanyName).all()


def get_supplier(db: Session, supplier_id: int):
    return db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()


def get_products_for_supplier(db: Session, supplier_id: int):
    return db.query(models.Product) \
        .options(load_only("ProductID", "ProductName", "Discontinued"),
                 joinedload(models.Product.Category).options(load_only("CategoryID", "CategoryName"))) \
        .filter(models.Product.SupplierID == supplier_id) \
        .order_by(models.Product.ProductID.desc()).all()


def insert_supplier(db: Session, supplier: schemas.SupplierCreate):
    supplier_id = db.query(models.Supplier).count() + 1
    db_supplier = models.Supplier(SupplierID=supplier_id, **supplier.dict())
    db.add(db_supplier)
    db.commit()
    return db_supplier


def update_supplier(db: Session, supplier_id: PositiveInt, new_supp: schemas.SupplierUpdate):
    supp = db.get(models.Supplier, supplier_id)
    for (k, v) in new_supp.dict().items():
        print(f"updating {k} {v}")
        setattr(supp, k, v)
    db.commit()
    return supp


def delete_supplier(db: Session, supplier_id: PositiveInt):
    db.delete(db.get(models.Supplier, supplier_id))
    db.commit()
