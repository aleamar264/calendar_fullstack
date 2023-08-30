from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from back.calendar.route import calendar


app = FastAPI(
    title="Calendar XXX",
    description="""Calendar to queue task on background using
        APSchedule using date to run only one""",
    version='0.0.0'
)

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

def my_task():
    print("Scheduled task executed!")
