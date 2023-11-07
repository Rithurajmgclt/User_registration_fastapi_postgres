
import os
import re
import bcrypt
from fastapi import APIRouter, UploadFile,File,Form,Depends,Request
from users.schema import UserDetail
from users.models import User,Profile
from pydantic import ValidationError, EmailStr
from fastapi import Form
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from users.database import get_db
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

user_router = APIRouter()
base_url = os.getenv("base_url")
PASSWORD_REGEX = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@#$%^&+=]{8,}$"




@user_router.get("/users/{user_id}", response_model=UserDetail)
async def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    """
    function for user get
    """
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    image_url = f"{base_url}/{user.profile.image_path}"
    
    user_detail = UserDetail(
        id=user.id,
        fullname=user.fullname,
        email=user.email,
        phone =user.phone,
        image_url= image_url
    )
    return user_detail
@user_router.get("/users/list/", response_model=list[UserDetail])
async def get_user(db: Session = Depends(get_db)):
    """
    function for user list 
    """
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users created")

    user_list = []
    for user in users:
        image_url = f"{base_url}/{user.profile.image_path}" if user.profile and user.profile.image_path else None  
        user_with_image = UserDetail(
            id=user.id,
            fullname=user.fullname,
            email=user.email,
            phone=user.phone,
            image_url=image_url
        )
        user_list.append(user_with_image)

    return user_list


def save_uploaded_file(file: UploadFile, file_path: str):
    """
    function to read image
    """
    
    with open(file_path, "wb") as buffer:
        while True:
            chunk = file.file.read(1024)
            if not chunk:
                break
            buffer.write(chunk)


@user_router.post("/users/create")
async def create_item(fullname: str = Form(...),
    email: EmailStr = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)):

    """
    function to create user
    input attributes  email,phone,password,uploaded iamge
    """
    try:

        if not re.match(PASSWORD_REGEX, password):
            return {'message': 'Password must be at least 8 characters long and contain at least one letter and one digit'}   
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User(
            fullname=fullname,
            email=email,
            phone=phone,
            password=hashed_password,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        if image and new_user.id:
            upload_folder = "static/images"
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, image.filename)
            save_uploaded_file(image, file_path)

            profile = Profile(user_id=new_user.id, image_path=file_path)
            db.add(profile)
            db.commit()

        return {"message": "User created successfully", "user_id": new_user.id}

    except (ValidationError, IntegrityError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    




