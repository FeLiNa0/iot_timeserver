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


@app.get("/")
async def root():
    return {"message": "Hello World", "hostname": gethostname()}

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
    return {"timezones": list(pytz.all_timezones), "hostname": gethostname()}

@app.middleware("http")
async def add_hostname_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Timekeeper-ID"] = gethostname()
    return response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

