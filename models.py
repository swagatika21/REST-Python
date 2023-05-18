from sqlalchemy import Column,Integer,String
from database import Base

#comapany base model
class Companies(Base):
    __tablename__ = "Companies"
    
    id=Column(Integer, primary_key=True,index=True)
    name=Column(String)
    location=Column(String)
    
    