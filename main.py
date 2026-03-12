from fastapi import FastAPI
from db.models import Base
from db.database import engine
from api.routes import router

# Generate database tables based on our SQLAlchemy models
Base.metadata.create_all(bind=engine)

app=FastAPI(title='Mitul Bhai Backend API')

app.include_router(router)