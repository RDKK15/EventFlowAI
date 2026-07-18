from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.database import Base, SessionLocal, engine
from app.startup.initialize import create_default_owner

# Import models
from app.models.customer import Customer
from app.models.enquiry import Enquiry
from app.models.quotation import Quotation
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.user import User
from app.models.business import Business
from app.models.business_user import BusinessUser
from app.models.business_sequence import BusinessSequence
from app.models.service_type import ServiceType
from app.models.requirement_definition import RequirementDefinition
from app.models.requirement_option import RequirementOption

# Import routers
from app.api.customer import router as customer_router
from app.api.dashboard import router as dashboard_router
from app.api.enquiry import router as enquiry_router
from app.api.quotation import router as quotation_router
from app.api.booking import router as booking_router
from app.api.payment import router as payment_router
from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.business import router as business_router
from app.api.business_configuration import router as business_configuration_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting BizPart AI...")

    # Create tables


    # Create default owner
    db = SessionLocal()
    try:
        create_default_owner(db)
    finally:
        db.close()

    print("✅ Startup complete.")

    yield

    print("🛑 Shutting down BizPart AI...")


app = FastAPI(
    title="BizPart AI",
    lifespan=lifespan,
)

app.include_router(customer_router)
app.include_router(enquiry_router)
app.include_router(quotation_router)
app.include_router(booking_router)
app.include_router(payment_router)
app.include_router(dashboard_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(business_router)
app.include_router(business_configuration_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to BizPart AI 🚀"
    }
