from fastapi import FastAPI

from app.api.customer import router as customer_router
from app.api.booking import router as booking_router

from app.db.database import Base, engine

from app.api.enquiry import router as enquiry_router
from app.models.enquiry import Enquiry

app = FastAPI(title="BizPart Bot")

Base.metadata.create_all(bind=engine)

app.include_router(customer_router)
app.include_router(booking_router)
app.include_router(enquiry_router)

@app.get("/")
def root():
    return {"message": "Welcome to BizPart Bot 🚀"}