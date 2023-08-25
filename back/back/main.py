from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from back.calendar.route import calendar


app = FastAPI()

origin = [
    '*'
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/')
async def main():
    return {"message":"I'm working"}

app.include_router(calendar)