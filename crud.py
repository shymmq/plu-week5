from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload, load_only

import models


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
