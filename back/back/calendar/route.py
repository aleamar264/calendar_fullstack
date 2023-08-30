from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from back.schemas.schemas import (ReserveModel, ReserveBotResponse,
                                DeleteEvent)

from back.functions.calendar import create_event, get_event, get_list_event
from back.functions.scheduler import scheduler
from datetime import datetime
from pytz import utc

from random import random

calendar = APIRouter(prefix='/calendar', tags=['calendar'])

def ansible_run(x: str, y: int) -> None:
    print(f"""the atual id of the job is{x}\
          - and a random number {y} -----> Printing now""")


@calendar.post('/reserve_bot', status_code=200, response_model=ReserveBotResponse)
async def reserve_bot(reserve_bot: ReserveModel):
    """
    The function `reserve_bot` creates an event using the data from a `ReserveModel` object.

    :param reserve_bot: An instance of the ReserveModel class
    :type reserve_bot: ReserveModel
    :return: the result of calling the `create_event` function with the arguments unpacked from the
    `model_dump` method of the `reserve_bot` object.
    """
    event = create_event(reserve_bot.model_dump())
    start_time = datetime.strptime(event['start']['dateTime'],
                                   "%Y-%m-%dT%H:%M:%S%z").astimezone(utc)
    if  start_time < datetime.now(utc):
        raise HTTPException(status_code=400, detail="Cannot schedule a task in the past")

    job_scheduled = scheduler.add_job(ansible_run, trigger='date', run_date=event['start']['dateTime'],
                                      timezone=utc, args=("sdase2343fa", random()*10,))

    return JSONResponse(content={"id": event["id"], "status": event["status"],
                                 "summary": event["summary"]},
                            status_code=200)

@calendar.get('/reserved_bot/{eventId}', status_code=200)
async def get_reserved_bots(eventId: str, query: str = ""):
    return get_event(event_id=eventId)

@calendar.get('/reserved_bot', status_code=200)
async def get_list_reserved_bots(query: str = ""):
    return list(get_list_event())
