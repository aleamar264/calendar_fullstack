from back.calendar.get_services import get_calendar_service
from back.responses.json_response import response_json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from tzlocal import get_localzone_name
from back.functions.date_time_util import to_localized_iso

from fastapi.responses import JSONResponse

service = get_calendar_service()

def create_event(template: dict, calendar_id:str = 'primary'):
    """
    The function creates an event in a Google Calendar using a provided template.

    :param template: The `template` parameter is a dictionary that contains the details of the event you
    want to create. It should include properties such as `summary` (event title), `start` (event start
    time), `end` (event end time), and any other relevant information
    :type template: dict
    :param calendar_id: The `calendar_id` parameter is the ID of the calendar where you want to create
    the event. By default, it is set to `'primary'`, which refers to the primary calendar of the
    authenticated user. However, you can specify a different calendar ID if you want to create the event
    in a, defaults to primary
    :type calendar_id: str (optional)
    :return: the response from the API call to create an event in the specified calendar.
    """
    try:
        response = service.events().insert(calendarId=calendar_id,
                                body=template).execute()
        return response
    except Exception as e:
        return response_json(message=e.message, status=500)

def get_event(event_id: str, calendar_id:str = 'primary') -> dict | JSONResponse:
    """
    The function `get_event` retrieves a specific event from a calendar using its event ID.

    :param event_id: The `event_id` parameter is a string that represents the unique identifier of the
    event you want to retrieve from the calendar
    :type event_id: str
    :param calendar_id: The `calendar_id` parameter is the ID of the calendar from which you want to
    retrieve the event. By default, it is set to `'primary'`, which refers to the primary calendar of
    the authenticated user. However, you can provide a different calendar ID if you want to retrieve the
    event from, defaults to primary
    :type calendar_id: str (optional)
    :return: the response from the Google Calendar API when retrieving an event.
    """
    try:
        response = service.events().get(calendarId=calendar_id,
                                eventId=event_id).execute()
        return response
    except Exception as e:
        return response_json(message=e.message, status=500)

def delete_event(event_id: str, calendar_id:str = 'primary'):
    """
    The function `delete_event` deletes an event from a calendar using the Google Calendar API.

    :param event_id: The event_id parameter is a string that represents the unique identifier of the
    event that you want to delete from the calendar
    :type event_id: str
    :param calendar_id: The `calendar_id` parameter is the ID of the calendar from which you want to
    delete the event. By default, it is set to `'primary'`, which refers to the primary calendar of the
    authenticated user. However, you can specify a different calendar ID if you want to delete the event
    from, defaults to primary
    :type calendar_id: str (optional)
    :return: the response from the API call to delete the event.
    """
    try:
        response = service.events().delete(calendarId=calendar_id,
                                eventId=event_id).execute()
        return response
    except Exception as e:
        return response_json(message=e.message, status=500)

def update_event(event_id: str,
                 template: dict,
                 calendar_id:str = 'primary'):
    """
    The function `update_event` updates an event in a calendar using the Google Calendar API.

    :param event_id: The event_id parameter is a string that represents the unique identifier of the
    event that you want to update in the calendar. This identifier is typically obtained when creating
    or retrieving an event from the calendar
    :type event_id: str
    :param template: The `template` parameter is a dictionary that contains the updated information for
    the event. It should include the fields and values that you want to update for the event
    :type template: dict
    :param calendar_id: The `calendar_id` parameter is the ID of the calendar where the event is
    located. By default, it is set to `'primary'`, which refers to the primary calendar of the
    authenticated user. However, you can specify a different calendar ID if you want to update an event
    in a different calendar, defaults to primary
    :type calendar_id: str (optional)
    :return: the response from the `service.events().update()` method.
    """

    try:
        response = service.events().update(calendarId=calendar_id,
                                eventId=event_id,
                                body = template).execute()
        return response
    except Exception as e:
        return response_json(message=e.message, status=500)

def get_list_event(calendar_id:str = 'primary',
                    time_min: date| datetime | str= None,
                    time_max: date| datetime | str= None,
                    timezone: str = get_localzone_name(),
                   kwargs: dict = {}):
    """
    The function `get_list_event` retrieves a list of events from a calendar within a specified time
    range.

    :param calendar_id: The calendar ID is a unique identifier for a specific calendar. It can be the
    primary calendar of a user or a specific calendar created by the user. By default, the value is set
    to 'primary', which refers to the primary calendar of the authenticated user, defaults to primary
    :type calendar_id: str (optional)
    :param time_min: The `time_min` parameter is used to specify the minimum start time for the events
    you want to retrieve. It can be a `date`, `datetime`, or `str` object representing a specific date
    and time. If not provided, it defaults to the current time
    :type time_min: date| datetime | str
    :param time_max: The `time_max` parameter is used to specify the maximum date and time for the
    events you want to retrieve from the calendar. It can be specified as a `date` object, `datetime`
    object, or a string in ISO 8601 format. If not provided, it defaults to the
    :type time_max: date| datetime | str
    :param timezone: The `timezone` parameter is used to specify the timezone for the time range of
    events to be retrieved. It defaults to the local timezone obtained from the `get_localzone_name()`
    function
    :type timezone: str
    :param kwargs: The `kwargs` parameter is a dictionary that allows you to pass additional optional
    parameters to the `events().list()` method. These parameters can include things like `maxResults`,
    `orderBy`, `q`, etc. You can refer to the Google Calendar API documentation for a full list of
    available parameters and
    :type kwargs: dict
    """
    time_min = time_min or datetime.now()
    time_max = time_max or time_min + relativedelta(years=1)

    time_min = to_localized_iso(time_min, timezone)
    time_max = to_localized_iso(time_max, timezone)

    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id,
                                       pageToken=page_token,
                                       timeMin=time_min,
                                       timeMax=time_max,
                                       **kwargs).execute()
        for event in events['items']:
            yield event
        page_token = events.get('nextPageToken')
        if not page_token:
            break