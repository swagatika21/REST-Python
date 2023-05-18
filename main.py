from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency: Database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Company(BaseModel):
    name: str = Field(min_length=1)
    location: str = Field(min_length=5, max_length=50)
   

# Routes
#Check service status
@app.get("/status")
def service_status():
    return {"status": "Service Up and running!"}

#Get company List
@app.get("/")
def read_companies(db: Session = Depends(get_db)):
    return db.query(models.Companies).all()

#Get company by company id
@app.get("/company/{company_id}")
def get_company(company_id: int, db: Session = Depends(get_db)):
    company_model = db.query(models.Companies).filter(models.Companies.id == company_id).first()

    if company_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Company with ID {company_id} not found"
        )

    return company_model

#Insert a new record 
@app.post("/")
def create_company(company: Company, db: Session = Depends(get_db)):
    company_model = models.Companies()

    company_model.name = company.name
    company_model.location = company.location

    db.add(company_model)
    db.commit()

    return company

#modify existing record
@app.put("/{company_id}")
def update_company(company_id: int, company: Company, db: Session = Depends(get_db)):
    company_model = db.query(models.Companies).filter(models.Companies.id == company_id).first()

    if company_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {company_id} does not exist"
        )

    company_model.name = company.name
    company_model.location = company.location
    

    db.add(company_model)
    db.commit()

    return company

#Compare comapany data
@app.get("/company/{company_id}/compare")
def compare_company(company_id: int, db: Session = Depends(get_db)):
    company_model = db.query(models.Companies).filter(models.Companies.id == company_id).first()

    if company_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Company with ID {company_id} not found"
        )
    original_company = {
        'name': company_model.name,
        'location': company_model.location
    }
    modified_company = {
        'name': company_model.name,
        'location': company_model.location
    }

    delta = {}
    for attribute in ['name', 'location']:
        if original_company[attribute] != modified_company[attribute]:
            delta[attribute] = {
                'original': original_company[attribute],
                'modified': modified_company[attribute]
            }

    return delta


