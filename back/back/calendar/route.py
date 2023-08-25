from fastapi import APIRouter
from fastapi.responses import JSONResponse
from back.schemas.schemas import (ReserveModel, ReserveBotResponse,
                                                        DeleteEvent)

from back.functions.calendar import create_event, get_event, get_list_event


calendar = APIRouter(prefix='/calendar', tags=['calendar'])

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
    return JSONResponse(content={"id": event["id"], "status": event["status"], "summary": event["summary"]},
                            status_code=200)

@calendar.get('/reserved_bot/{eventId}', status_code=200)
async def get_reserved_bots(eventId: str, query: str = ""):
    return get_event(event_id=eventId)
    
@calendar.get('/reserved_bot', status_code=200)
async def get_list_reserved_bots(query: str = ""):
    return list(get_list_event())

# @calendar.get('/reserved_bot/{id_calendar}', status_code=200, response_model=list[ReturnEvent])
# def get_reserved_bots(id_calendar: str = ""):
#     """
#     The function `get_reserved_bots` returns a list of events from a calendar, filtered by a query
#     string.
    
#     :param query: The `query` parameter is used to filter the events based on a specific query string.
#     It allows you to search for events that match a certain criteria
#     :type query: str
#     :return: The function `get_reserved_bots` returns a list of dictionaries. Each dictionary represents
#     an event and contains the following information: summary, start time, end time, timezone, and event
#     ID.
#     """
#     return _calendar.get_event(id_calendar)

# @calendar.post("/reserved_bot", status_code=200)
# def delete_event(id: DeleteEvent):
#     print(id)
#     kwargs = {"calendar_id": 'primary',
#           "event": id.id,
#           "sendNotifications": False}
#     event =  _calendar.delete_event(**kwargs)
#     # print(event)
#     # _calendar.delete_event(event)
#     # return {"event":{'summary': event.summary,
#     #                   'start': str(event.start),
#     #                   'end': str(event.end),
#     #                   'timezone': str(event.timezone),
#     #                   'id': event.id}}

# @calendar.patch('/reserved_bot', status_code=200, response_model=ReturnEvent)
# async def update_event():
#     pass
