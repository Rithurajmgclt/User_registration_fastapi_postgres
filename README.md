
create a folder "static" in the root directory  
create virtual environment  and run "pip install -r requirements.txt'   
create a .env file in root directory please check "exmapleenvfile.txt" for that        
create a postgres database and add it in .env         
create tables in postgres db using  "alembic upgrade head"     
run application  "uvicorn main:app --reload"    
access api in "localhost/docs"  
