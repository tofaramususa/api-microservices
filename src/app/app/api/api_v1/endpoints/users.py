from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from motor.core import AgnosticDatabase

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.User)
async def create_user_profile(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(""),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = await crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="This username is not available.",
        )
    # Create user auth
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = await crud.user.create(db, obj_in=user_in)
    return user


@router.put("/", response_model=schemas.User)
async def update_user(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    obj_in: schemas.UserUpdate,
    current_user_id: str = Depends(deps.get_user_id),
) -> Any:
    """
    Update user.
    """
    current_user = await crud.user.get(db, id=current_user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if current_user.hashed_password and obj_in.original:
        user = await crud.user.authenticate(db, email=current_user.email, password=obj_in.original)
        if not user:
            raise HTTPException(status_code=400, detail="Unable to authenticate this update.")
    
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    
    if obj_in.password is not None:
        user_in.password = obj_in.password
    if obj_in.full_name is not None:
        user_in.full_name = obj_in.full_name
    if obj_in.email is not None:
        check_user = await crud.user.get_by_email(db, email=obj_in.email)
        if check_user and check_user.email != current_user.email:
            raise HTTPException(
                status_code=400,
                detail="This username is not available.",
            )
        user_in.email = obj_in.email
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/", response_model=schemas.User)
async def read_user(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    current_user_id: str = Depends(deps.get_user_id),
) -> Any:
    """
    Get current user.
    """
    current_user = await crud.user.get(db, id=current_user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user


@router.get("/all", response_model=List[schemas.User])
async def read_all_users(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    page: int = 0,
    is_admin: bool = Depends(deps.is_admin),
) -> Any:
    """
    Retrieve all current users.
    """
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await crud.user.get_multi(db=db, page=page)


@router.post("/toggle-state")
async def toggle_state(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    user_in: schemas.UserUpdate,
    is_admin: bool = Depends(deps.is_admin),
) -> Any:
    """
    Toggle user state (moderator function)
    """
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    response = await crud.user.toggle_user_state(db=db, obj_in=user_in)
    if not response:
        raise HTTPException(
            status_code=400,
            detail="Invalid request.",
        )
    return {"msg": "User state toggled successfully."}


@router.post("/create", response_model=schemas.User)
async def create_user(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    is_admin: bool = Depends(deps.is_admin),
) -> Any:
    """
    Create new user (moderator function).
    """
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await crud.user.create(db, obj_in=user_in)
    return user


@router.get("/tester")
async def test_endpoint() -> Any:
    """
    Test current endpoint.
    """
    return {"msg": "Message returned ok."}