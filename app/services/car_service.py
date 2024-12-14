from app.models.car import Car
from pathlib import Path
from fastapi import HTTPException
from fastapi.responses import FileResponse

import hashlib
import zipfile
import pandas as pd
import csv
import logging

# --- CONSTANTS ---
CSV_FILE_PATH = (Path(__file__).parent / "../data/cars_file.csv").resolve()
ZIP_FILE_PATH = (Path(__file__).parent / "../data/cars_file.zip").resolve()
# -----------------

# --- LOGGING ---
logging.basicConfig(
    filename="api_operations.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_operation(message: str):
    logging.info(message)
# ---------------


# --- AUX FUNCTIONS ---
def create_cars_file():
    with open(CSV_FILE_PATH, mode="w", newline="", encoding="utf8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "model", "brand", "year", "color", "price", "mileage"])


def write_cars_file(car):
    with open(CSV_FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([car.id, car.model, car.brand, car.year, car.color, car.price, car.mileage])

       
def write_all_cars_file(cars):
    with open(CSV_FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "model", "brand", "year", "color", "price", "mileage"])
        writer.writeheader()
        writer.writerows(cars)
# ---------------------

def get_all_cars():
    try:
        data = pd.read_csv(CSV_FILE_PATH)
        cars = data.to_dict(orient="records")
        
        log_operation("Cars list has been retrieved")
        return cars
    except FileNotFoundError:
        create_cars_file()
        log_operation("Cars list not found, a new file has been created")
        return []
    except Exception as e:
        log_operation(f"Error on processing CSV file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo CSV: {str(e)}")


def get_car_by_id(car_id: int):
    cars = get_all_cars()
    
    for car in cars:
        if int(car["id"]) == car_id:
            log_operation(f"Car with id {car_id} has been retrieved")
            return car
    
    log_operation(f"Car with id {car_id} not found")
    raise HTTPException(status_code=404, detail="Car not found") 


def create_car(new_car: Car):
    cars_length = get_all_cars()
    car = Car(id=len(cars_length) + 1, **new_car.dict())

    if not CSV_FILE_PATH.exists():
        create_cars_file()
    
    try:
        write_cars_file(car)
        log_operation(f"New car has been created: {car}")
    except Exception as e:
        log_operation(f"Error on writing CSV file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao escrever no arquivo CSV: {str(e)}")

    return car


def update_car(car_id: int, updated_data: dict):
    cars = get_all_cars()
    
    try:
        for car in cars:
            if int(car["id"]) == car_id:
                car.update(updated_data.dict(exclude_unset=True))
                car["id"] = car_id
                
                log_operation(f"Car with id {car_id} has been updated: {car}")
                write_all_cars_file(cars)
                return car
    except Exception as e:
        log_operation(f"Error on writing CSV file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao escrever no arquivo CSV: {str(e)}")


def delete_car(car_id: int):
    cars = get_all_cars()
    
    filtered_cars = [car for car in cars if int(car["id"]) != car_id]
    
    if len(filtered_cars) == len(cars):
        log_operation(f"Car with id {car_id} not found")
        raise HTTPException(status_code=404, detail="Car not found")
    
    log_operation(f"Car with id {car_id} has been deleted")
    write_all_cars_file(filtered_cars)
    
    return {"message": f"Car with id {car_id} has been deleted"}


def handle_csv_backup():
    if not CSV_FILE_PATH.exists():
        log_operation("CSV file not found")
        raise HTTPException(status_code=404, detail="CSV file not found")

    try:
        with zipfile.ZipFile(ZIP_FILE_PATH, "w", zipfile.ZIP_DEFLATED) as zip_file:
            log_operation("Creating ZIP file")
            zip_file.write(CSV_FILE_PATH, arcname=CSV_FILE_PATH.name)
    except Exception as e:
        log_operation(f"Error on creating ZIP file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar o arquivo ZIP: {str(e)}")
    
    log_operation("ZIP file has been created")
    return FileResponse(ZIP_FILE_PATH, media_type="application/zip", filename=ZIP_FILE_PATH.name)


def handle_filter_cars(
    brand: str = None,
    model: str = None,
    min_year: int = None,
    max_year: int = None,
    min_price: float = None,
    max_price: float = None,
    min_mileage: float = None,
    max_mileage: float = None,
    color: str = None
):
    try:   
        cars = get_all_cars()
        
        filtered_cars = [
            car for car in cars
            if (
                (brand is None or brand == "" or car["brand"].lower() == brand.lower()) and
                (model is None or model == "" or car["model"].lower() == model.lower()) and
                (min_year is None or min_year == "" or car["year"] >= min_year) and
                (max_year is None or max_year == "" or car["year"] <= max_year) and
                (min_price is None or min_price == "" or car["price"] >= min_price) and
                (max_price is None or max_price == "" or car["price"] <= max_price) and
                (min_mileage is None or min_mileage == "" or car["mileage"] >= min_mileage) and
                (max_mileage is None or max_mileage == "" or car["mileage"] <= max_mileage) and
                (color is None or color == "" or car["color"].lower() == color.lower())
            )
        ]
        
        log_operation(f"Cars have been filtered: {filtered_cars}")
        return filtered_cars
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error on filter cars: {str(e)}")


def handle_cars_hash():
    try:
        sha_hash = hashlib.sha256()
        with open(CSV_FILE_PATH, "rb") as file:
            for byte_block in iter(lambda: file.read(4096), b""):
                sha_hash.update(byte_block)
            
            log_operation("Hash has been calculated")
            hash_key = sha_hash.hexdigest()
    except FileNotFoundError:
        log_operation("CSV file not found")
        raise HTTPException(status_code=404, detail="CSV file not found")
    except Exception as e:
        log_operation(f"Error on hash calculation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error on hash calculation: {str(e)}")
    
    return {"hash": hash_key}
