from fastapi import FastAPI
from backend.user_routes import router as user_router
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.models import UserCreate, UserResponse
from backend.auth import login_user
import os

# This is your main FastAPI app
app = FastAPI()

# # Include your login route from user_routes.py, commenting this for now as we are not using the javascript to get tje data
# app.include_router(user_router) 

# Serve the static folder
from pathlib import Path

static_dir = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

#Jinja templates for displaying errors
jinja_templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "static"))

@app.get("/", response_class=HTMLResponse)
async def get_login_form(request: Request):
    return jinja_templates.TemplateResponse("index.html", {"request": request})

@app.post("/form-login", response_class=HTMLResponse)
async def user_login_form(request: Request,  
                          email: str = Form(...),
                          password: str = Form(...)):
    
    print("First Function")
    try:
    #after we get the data, lets create the user first

        user = UserCreate(
            email=email,
            password=password
        )

        print("user created")

        user_data = login_user(user=user)
        print("\n\n\n\n USER DATA: ", user_data)
        

        return RedirectResponse(url="/static/welcome.html", status_code=302) #this will redirect to the webpage that says welcome
    except Exception as e:
        return jinja_templates.TemplateResponse("index.html", {"request": request, "error": str(e)}) #t

