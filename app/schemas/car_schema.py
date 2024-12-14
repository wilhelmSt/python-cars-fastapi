from pydantic import BaseModel, Field

class CarCreate(BaseModel):
    brand: str = Field(..., max_length=50)
    model: str = Field(..., max_length=50)
    year: int = Field(..., ge=1886, le=2100)
    price: float = Field(..., gt=0)
    mileage: float = Field(..., ge=0)
    color: str = Field(..., max_length=25)

class CarUpdate(BaseModel):
    brand: str = Field(None, max_length=50)
    model: str = Field(None, max_length=50)
    year: int = Field(None, ge=1886, le=2100)
    price: float = Field(None, gt=0)
    mileage: float = Field(None, ge=0)
    color: str = Field(None, max_length=25)
