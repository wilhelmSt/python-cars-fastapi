from pydantic import BaseModel, Field

class Car(BaseModel):
    id: int
    brand: str = Field(..., max_length=50)
    model: str = Field(..., max_length=50)
    year: int = Field(..., ge=1886, le=2100)
    price: float = Field(..., gt=0)
    mileage: float = Field(..., ge=0)
    color: str = Field(..., max_length=25)
