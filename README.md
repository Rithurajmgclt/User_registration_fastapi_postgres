# User_registration_fastapi_postgres 


################
***important****
create a folder "static" in the root directory
create virtualenv and run "pip install -r requirements.txt'
##################
****important***
create file ".env" in root directory and add the following details
DB_NAME_1 will be postgres database name 

""""
DB_NAME_1=
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/db_name
base_url = "http://127.0.0.1:8000"
"""""
###############
to create postgres table use "alembic upgrade head"
to run application use "uvicorn main:app --reload"
