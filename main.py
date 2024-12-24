from fastapi import FastAPI
from authentication.router import router as auth_router
from authentication import *
from courses.get_courses_by_params import router as course_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(course_router)
