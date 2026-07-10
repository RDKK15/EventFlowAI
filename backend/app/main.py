from fastapi import FastAPI

from app.db.database import Base, engine

# Import models (IMPORTANT)
from app.models.customer import Customer
from app.models.enquiry import Enquiry
from app.models.quotation import Quotation
from app.models.booking import Booking
from app.models.payment import Payment

# Import routers
from app.api.customer import router as customer_router
from app.api.dashboard import router as dashboard_router
from app.api.enquiry import router as enquiry_router
from app.api.quotation import router as quotation_router
from app.api.booking import router as booking_router
from app.api.payment import router as payment_router

from app.models.user import User

from app.api.auth import router as auth_router
from app.api.user import router as user_router

app = FastAPI(title="BizPart Bot")

Base.metadata.create_all(bind=engine)

app.include_router(customer_router)
app.include_router(enquiry_router)
app.include_router(quotation_router)
app.include_router(booking_router)
app.include_router(payment_router)
app.include_router(dashboard_router)
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Welcome to BizPart Bot 🚀"}