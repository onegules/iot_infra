from pydantic import BaseModel, Field
from typing import Optional

class EnvironmentBase(BaseModel):
    id: int
    serial: int
    event_time: string
    temperature: float
    humidity: float
    air_pressure: float   

class EnvironmentCreate(EnvironmentBase):
    temperature: Optional[float] = Field(default=None)
    humidity: Optional[float] = Field(default=None)
    air_pressure: Optional[float] = Field(default=None)
    
    @model_validator(model="after")
    def validate_xor(cls, values):
        if sum([bool(v) for v in values.values()]) != 1:
            raise ValueError('Either id or txt must be set.')
        return values


class EnvironmentRead(EnvironmentBase):
    class Config:
        orm_mode = True
