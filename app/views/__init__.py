from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta

templates = Jinja2Templates(directory="app/views")
templates.env.globals.update(datetime=datetime, timedelta=timedelta)
