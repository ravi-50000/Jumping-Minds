# Jumping-Minds


**Overview**: This project provides a set of APIs for managing elevators in a building. The APIs allow users to create elevators, manage elevator requests, move elevators up or down, open or close the elevator door, mark elevators as working or not, and create elevator requests for various floors.



**Design Decisions** : Used Below Tech Stack to Design the Api's

1. **Django Framework**: Django is a robust and widely used web framework that provides a rich set of features for building web applications, including powerful ORM, built-in security, and a user-friendly admin interface.

2. **ViewSets** : ViewSets group similar actions in a single class. DRF automatically generates URL patterns for ViewSets.

3. **Serializers**: Serializers in Django help in converting complex data types, such as QuerySets and model instances, to Python data types like dictionaries.

4. **Pagination** : Pmplementing pagination in the APIs, we can provide data in smaller, manageable chunks(pages), improving API response times, reduce load on server and user experience.

5. **Postgresql** : PostgreSQL is an advanced, open-source, and powerful relational database management system. Postgresql suits for high traffic system like elevator management.(Used pgAdmin for testing)



**API Contract** : 9 Api's are created(4,8 not addressed in problem statement). 8,9 can be merged but to make it more concise created extra api(8)

1. **Create Elevators** :

   Description: Creates a specified number of elevators in the building.

   Method: POST

   Endpoint: /elevators/create_elevators/

   Request Body:
       {
        "number_of_elevators": 15
       }

   Response:
        {
         "message": "Successfully created Elevators"
        }

2. **Elevator Request** :

   Description: Create elevator requests for specific floor.

   Method: POST

   Endpoint: /elevators/save_elevator_request/

   Request Body:
       {
       "elevator_number": 1,
       "current_floor": 6,
       "destination_floor": 3
      }

   Response:
        {
        "message": "Successfully Created Request for Elevator"
        }


3. **Elevator Requests List**:

   Description: Displays Elevator requets made till now

   Method: POST

   Endpoint: /elevators/get_elevator_requests/

   Request Body:
       {
       "elevator_number": 2,
       "page_number": 1
      }

   Response:
        {
    "result": {
        "page_context": {
            "page_number": 1,
            "page_count": 1,
            "total_count": 1,
            "total_number_of_pages": 1
        },
        "requests_list": [
              {
                "source_floor" : 1,
                "destination_floor: : 4,
                "is_elevator_moving_up" : true,
                "id" : 1
             }
         ] 
     }

4. **Elevator Reached Destination**:

   Description: Extra Api to mark elevator current floor when reached destination.

   Method: POST

   Endpoint: /elevators/reached_elevator_destination/

   Request Body:
       {
       "elevator_number": 1,
       "id": 1,
       "destination_floor": 3
      }

   Response:
        {
        "message": "Succesfully Reached Destination"
        }

5. **Elevator Next Destination**:

   Description: It will show the Next Destination of Elevator if exists

   Method: POST

   Endpoint: /elevators/next_destination/

   Request Body:
       {
       "elevator_number": 1
      }

   Response: 3

6. **Elevator Moving Up or Down**:
 
   Description: It will Display Moving up if Elevator Moving up else Moving Down if Elevator Moving Down else Elevator is stable on floor 'x'

   Method: POST

   Endpoint: /elevators/moving_down_or_up/

   Request Body:
       {
       "elevator_number": 1
      }

   Response:
       {
       "message": "Moving Down"
       }

7. **Open or Close the Elevator door**:

   Description: Api will Open or Close the Elevator Based on input

   Method: POST

   Endpoint: /elevators/open_or_close_the_door/

   Request Body:
       {
       "elevator_number": 1,
       "open_door": false
      }

   Response:
       {
       "message": "Elevator Door Closed"
       }

8. **Mark Elevator Working**:

   Description: Api will mark the given Elevator as Working.(By Default all elevators are working)

   Method: POST

   Endpoint: /elevators/mark_elevator_working/

   Request Body:
       {
       "elevator_number": 1
      }

   Response:
       {
       "message": "Elevator Marked as Working"
       }

9. **Mark Elevator Not Working**:

   Description: Api will mark the given Elevator as Not Working.

   Method: POST

   Endpoint: /elevators/mark_elevator_not_working/

   Request Body:
       {
       "elevator_number": 1
      }

   Response:
       {
       "message": "Elevator Marked as Not Working"
       }



**Project SetUp:** :

1. Install Python
2. Install Virtual Env(pip install virtualenv)
3. Install Django(pip install django)
4. Create a Django Project in a folder(Type django-admin startproject project_name in terminal or any editor terminal)
5. Create a Virtual Env for the project(Type python -m venv virtual_env_name in terminal or any editor terminal)
6. Activate Virtual Env(Type source virtual_env_name/bin/activate in terminal or any editor terminal)
7. Install all the requirements(pip install -r requirements.txt)
8. Install pgAdmin for DB setup.
9. Install brew(https://brew.sh/) to install postgresql
10. Run this command to start DB server: pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
11. Login into postgres to create DB : psql postgres
12. CREATE DATABASE db_name;
13. CREATE USER ‘username’ with password ‘password’;
14. GRANT ALL PRIVILEGES ON DATABASE db_name TO username;
15. GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO username;
16. Create a django app to create elevator apis(python manage.py startapp app_name)
17. After Writing the Api run the local server(python manage.py runserver)



**Database modelling**: The Elevator Management APIs require an efficient database design to store and manage data related to elevators, elevator requests etc. For Every Elevator there can be 'n' number of requests so created a Foreign key relation for Elevator and Requests. Here is an overview of the database modelling for the Elevator Management system.
 
 **DataBase Name**: jumping_minds
 
 **Tables**: 
  1. elevator:
        created_at = models.DateTimeField(auto_now_add=True)
        modified_on = models.DateTimeField(auto_now=True)
        is_elevator_working = models.BooleanField(default=True)
        current_floor = models.IntegerField(default=1)
        is_door_opened = models.BooleanField(default=False)
        is_door_closed = models.BooleanField(default=True)

  2. requests:
        created_at = models.DateTimeField(auto_now_add=True)
        modified_on = models.DateTimeField(auto_now=True)
        elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name='requests')
        source_floor = models.IntegerField(null=True, blank=True)
        destination_floor = models.IntegerField(null=True, blank=True)
        is_elevator_moving_up = models.BooleanField()

   Note: We can use Prefetch_related to Optimize the Queries



**Deployment:** For Deployment we can choose EC2 in real-time and for running the Application we can configure the Web Server(Gunicorn etc). For Handling high amount of traffic we can configure the HTTP server(Nginx etc) which acts as Reverse-Proxy which will improve the Performance of the Application.



**Testing**: We can test all the Api's in Postman.

Ex:

<img width="1280" alt="Screenshot 2023-07-29 at 4 05 37 PM" src="https://github.com/ravi-50000/Jumping-Minds/assets/55268871/f6749bb1-f0a2-4291-98b0-a9d4c6f8bd16">




**Future Task:** Will send mail to the Admin or Selected Persons via Async Programming(Celery) when Elevator 'x' is not working.
