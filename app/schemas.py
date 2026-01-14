from pydantic import BaseModel


class DataOut(BaseModel):
    ltp:float
    stock_name:str
    change:float