import time
import pytz
import datetime
from fastapi import FastAPI, Request
from typing import Annotated
from socket import gethostname

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

TIME_FORMAT = '%Y/%m/%d %H:%M:%S.%f'

app = FastAPI()


@app.get("/timekeeper/time")
async def get_time_at_timezone(timezone: str | None=None):
    if not timezone:
        tz = None
    else:
        tz = pytz.timezone(timezone)
    dt = datetime.datetime.now(tz=tz).astimezone()
    return {"time": time.time(), "datetime": dt.strftime(TIME_FORMAT), "timezone": dt.strftime("%Z")}

@app.get("/timekeeper/timezones")
async def get_timezones():
    return {"timezones": list(pytz.all_timezones)}

@app.middleware("http")
async def add_hostname_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Timekeeper-ID"] = gethostname()
    return response
