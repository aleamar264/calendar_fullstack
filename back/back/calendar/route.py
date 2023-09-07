from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from back.schemas.schemas import (ReserveModel, ReserveBotResponse,
                                DeleteEvent)

from back.functions.calendar import create_event, get_event, get_list_event
from back.functions.scheduler import scheduler
from datetime import datetime
from pytz import utc
import pickle

from random import random
import redis

redis_host = 'localhost'
redis_port = 6379
redis_db = 1

redis_pool_db_1 = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db)
calendar_cache = redis.StrictRedis(connection_pool=redis_pool_db_1)

redis_pool_summary = redis.ConnectionPool(host=redis_host, port=redis_port, db=2)
redis_summary = redis.StrictRedis(connection_pool=redis_pool_summary)

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

    response = {"id": event["id"], "status": event["status"],
                                 "summary": event["summary"]}

    redis_summary.hset(f'event:{event["summary"]}',mapping={**{'job_id': job_scheduled.id}, **response})

    return JSONResponse(content=response,
                            status_code=200)

def get_event_cache(event_id: str):
    # use pickle.dumps(data)
    cached_event = calendar_cache.get(f'event:{event_id}')
    print(cached_event)
    if cached_event is not None:
        return pickle.loads(cached_event)
    event = get_event(event_id=event_id)
    calendar_cache.set(f"event:{event_id}", pickle.dumps(event))
    return event

def get_list_event_cache(kwargs: dict):
    cached_events = calendar_cache.get('events')
    if cached_events:
        return pickle.loads(cached_events)
    events = list(get_list_event(kwargs=kwargs))
    calendar_cache.set('events', pickle.dumps(events))
    return events

@calendar.get('/reserved_bot/{summary}', status_code=200)
async def get_reserved_bots(summary: str, query: str = ""):
    eventId = redis_summary.hget(f'event:{summary}', 'id')
    if eventId is None:
        return HTTPException(detail={"message": "We can't find any meeting with this name"},
                             status_code=400)
    return get_event_cache(event_id=eventId.decode('utf-8'))

@calendar.get('/reserved_bot', status_code=200)
async def get_list_reserved_bots(query: str = "", single_events: bool = True):
    # return  get_list_event_cache({'singleEvents': single_events})
    return list(get_list_event(kwargs={'singleEvents': single_events}))
