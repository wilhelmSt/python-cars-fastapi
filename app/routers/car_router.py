from fastapi import APIRouter
from app.schemas.car_schema import CarCreate, CarUpdate
from app.services.car_service import (
    get_all_cars, get_car_by_id, create_car, update_car, delete_car, handle_csv_backup, handle_filter_cars,
    handle_cars_hash
)
from app.models.car import Car
from fastapi.responses import FileResponse
from typing import Optional

router = APIRouter()

@router.get("/cars", response_model=list[Car])
async def list_cars():
    return get_all_cars()


@router.get("/cars/{car_id}", response_model=Car)
def retrieve_car(car_id: int):
    return get_car_by_id(car_id)


@router.post("/cars", response_model=Car, status_code=201)
def add_car(car: CarCreate):
    return create_car(car)


@router.put("/cars/{car_id}", response_model=Car)
def modify_car(car_id: int, car_data: CarUpdate):
    return update_car(car_id, car_data)


@router.delete("/cars/{car_id}")
def remove_car(car_id: int):
    return delete_car(car_id)


@router.get("/cars-quantity")
def count_cars():
    cars = get_all_cars()
    
    return {"quantity": len(cars)}


@router.get("/cars-backup", response_class=FileResponse)
def backup_csv():
    return handle_csv_backup()


@router.get("/cars-filter", response_model=list[Car])
def filter_cars(
    brand: Optional[str] = None,
    model: Optional[str] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_mileage: Optional[float] = None,
    max_mileage: Optional[float] = None,
    color: Optional[str] = None
):
    return handle_filter_cars(
        brand, model, min_year, max_year, min_price, max_price, min_mileage, max_mileage, color
    )
    

@router.get("/cars-hash", response_model=dict)
def get_cars_hash():
    return handle_cars_hash()

