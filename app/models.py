from sqlalchemy import Column,Integer,Float,String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, DateTime
from .database import Base
class StockData(Base):
    __tablename__= "stock_data"
    id=Column(Integer,primary_key=True,nullable=False)
    stock_name=Column(String,primary_key=False,unique=True,nullable=False)
    ltp=Column(Float,primary_key=False,unique=False,nullable=False)
    change=Column(Float,primary_key=False,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

