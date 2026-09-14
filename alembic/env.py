from app.core.db import Base

from app.models.user import SQUser
from app.models.admin import SQMainAdmin
from app.models.theater_admin import SQTheaterAdmin
from app.models.city import SQcity
from app.models.movies import SQmovies
from app.models.languages import SQlanguages
from app.models.theaters import SQtheaters
from app.models.screens import SQscreens
from app.models.seats import SQseats
from app.models.shows import SQshows
from app.models.show_seats import SQshow_seats
from app.models.booking_section import SQbooking_section
from app.models.booking_item import SQbooking_items
from app.models.payments import SQpayments
from app.models.tickets import SQtickets

target_metadata = Base.metadata