# Aviator

Aviator is a simple airport management system made using Django 4.

### Features

- Users can create `passenger` or `staff` accounts to access the database.
- `Passengers` can book flights and view their bookings using a simplified portal.
- `Staff` users may add flights to the network conveniently as the database takes care of flight congestion at the connecting airports.
- The availability of flights is automatically updated after each transaction.
- Database transactions are fail-proof and privacy is guaranteed due to the use of inbuilt Django modules.

### Setting up the project locally

1. Install `Python 3.10`, `Django 4.x`, `MySQL`.
2. Run `pip install mysqlconnector`.
3. Fork this repository and download it's source code by using the `git clone` command.
4. Run `cd Aviator/Aviator` to open your terminal in the root of the Django project. It must be noted that all the subsequent commands must be executed from a terminal with it's root in this directory only.
5. Create a new `MySQL` database by the name of `AVIATOR_DB` and run the MySQL server in the background.
6. Open the file `djangoproject/settings.py` and edit the lines `77-87` with your credentials for the MySQL setup.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'AVIATOR_DB',
        'USER': <USERNAME>,
        'PASSWORD': <PASSWORD OF THE USER>,
        'HOST': <HOST FOR THE MySQL SERVER> || <BY DEAFULT IT SHOULD BE "localhost">,
        'PORT': <PORT OF DEPLOYMENT OF MySQL SERVER> || <BY DEFAULT IT SHOULD BE "3306">,
    }
}
```

6. Create a `superuser` to access the Django Admin panel.
   You can do so by running `python manage.py createsuperuser` and following the onscreen instructions.

   Recommended `username` and `password` for the same is `admin` and `admin` for easy access.

7. Log in with your `superuser` and use it to set the `Delta` field in the `CongestionIndex` table (it specifies the maximum number of flights that can be scheduled in an interval on an airport).
   You can also create new `adminKeys` in the `Admin Keys` table, which could be later used by the staff members to register themselves as staff.

8. Run the following commands.

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

9. Now you can to the `/admin` route to view all the database information, and populate the database.
   Regular users can visit the site by accessing `localhost:8000` route.

### Project URL's

- `/` -> Home Page
- `/login` -> Login page for `staff` as well as `passengers`
- `/register` -> Register page for `passengers`

- `/flights` -> All available flights
- `/mybookings` -> Details of tickets booked by a passenger
- `/book/<int:flight_id>` -> Gateway for booking a ticket to the respective `flight_id`
- `/add_flight` -> Add a flight (for the staff)
- `/admin` -> Access the admin panel

### Schema of the Project

#### Aircraft

Keeps track of the types of Aircrafts and their basic details.

- `model_id` -> Model ID of the aircraft
- `name` -> Name of the aircraft
- `seats` -> Total number of seats on the aircraft
- `a_stat` -> Status of the aircraft (Operational/Suspended/Maintainance)
- `remarks` -> Any remarks for the pilot

#### Flight

Represents an actual flight that will be undertaken by an `Aircraft` for passengers.

- `aircraft` -> Aircraft ID of the flight (Foreign key to `aircraft`)
- `airline` -> Name of the airline (Foreign key to `airline`)
- `dep_airport` -> Departure airport of the flight (Foreign key to `airport`)
- `arr_airport` -> Arrival airport of the flight (Foreign key to `airport`
- `dep_time` -> Departure time of the flight
- `arr_time` -> Arrival time of the flight
- `fare` -> Fare of the flight
- `fl_status` -> Status of the flight

#### Booking

Represents a flight ticket issued to a passenger.

- `user` -> User ID of the passenger
- `fl_id` -> Flight ID of the flight (Foreign key to `flight`)
- `seat_n` -> Seat number
- `total_fare` -> Total fare of booking
- `status` -> Status of the booking (Confirmed/Pending)

#### Airline

Represents the airline that is operating a flight.

- `name` -> Name of the airline

#### Airport

Represents an airport for flights to arrive and depart from.

- `city` -> City of the airport
- `run_c` -> Independent runway count at the airport

#### CongestionIndex

A table to keep track of the congestion at an airport.

- `delta` -> At every airport, in any time interval of duration 'delta', there must be at most `run_c` flights departing or arriving at that airport.

#### CongestionIndex

A table to keep track of the congestion at an airport.

- `delta` -> At every airport, in any time interval of duration 'delta', there must be at most `run_c` flights departing or arriving at that airport.
