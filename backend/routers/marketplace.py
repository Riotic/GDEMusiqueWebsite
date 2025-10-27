from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import MarketplaceItem, User, RoleEnum
from backend.schemas import MarketplaceItemResponse, MarketplaceItemCreate
from backend.routers.auth import get_current_user, require_role

router = APIRouter()

@router.get("/", response_model=List[MarketplaceItemResponse])
async def get_marketplace_items(
    include_sold: bool = False,
    db: Session = Depends(get_db)
):
    """Retourne tous les objets en vente (non vendus par défaut)"""
    query = db.query(MarketplaceItem)
    if not include_sold:
        query = query.filter(MarketplaceItem.is_sold == False)
    
    items = query.order_by(MarketplaceItem.created_at.desc()).all()
    return items

@router.get("/{item_id}", response_model=MarketplaceItemResponse)
async def get_marketplace_item(item_id: int, db: Session = Depends(get_db)):
    """Retourne un objet de la marketplace par son ID"""
    item = db.query(MarketplaceItem).filter(MarketplaceItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", response_model=MarketplaceItemResponse, status_code=status.HTTP_201_CREATED)
async def create_marketplace_item(
    item: MarketplaceItemCreate,
    current_user: User = Depends(require_role([RoleEnum.ADMIN])),
    db: Session = Depends(get_db)
):
    """Créer un objet à vendre (ADMIN uniquement)"""
    db_item = MarketplaceItem(
        **item.dict(),
        seller_id=current_user.id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/{item_id}", response_model=MarketplaceItemResponse)
async def update_marketplace_item(
    item_id: int,
    item_update: MarketplaceItemCreate,
    current_user: User = Depends(require_role([RoleEnum.ADMIN])),
    db: Session = Depends(get_db)
):
    """Modifier un objet à vendre (ADMIN uniquement)"""
    db_item = db.query(MarketplaceItem).filter(MarketplaceItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item_update.dict().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.patch("/{item_id}/mark-sold", response_model=MarketplaceItemResponse)
async def mark_item_as_sold(
    item_id: int,
    current_user: User = Depends(require_role([RoleEnum.ADMIN])),
    db: Session = Depends(get_db)
):
    """Marquer un objet comme vendu (ADMIN uniquement)"""
    db_item = db.query(MarketplaceItem).filter(MarketplaceItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.is_sold = True
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_marketplace_item(
    item_id: int,
    current_user: User = Depends(require_role([RoleEnum.ADMIN])),
    db: Session = Depends(get_db)
):
    """Supprimer un objet de la marketplace (ADMIN uniquement)"""
    db_item = db.query(MarketplaceItem).filter(MarketplaceItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return None
