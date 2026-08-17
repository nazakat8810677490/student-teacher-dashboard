from fastapi import FastAPI , Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form
# from config.db import client
from config.db import students
from config.db import teachers
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "student_register.html"
        # "register.html",
        # {"request": request}
    )

@app.get("/student_login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
    request=request,
    name="student_login.html",
)
    # return templates.TemplateResponse(
    #     "login.html",
    #     {"request": request}
    # )

@app.post("/student_register")
def register(
    name: str = Form(...),
    roll_no: str = Form(...),
    id: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    user = students.find_one({"email": email})
    if user:
        return {
            "message": "Email is Allready Registered"
        }
    students.insert_one({
        "name": name,
        "roll_no": roll_no,
        "id": id,
        "email": email,
        "password": password
    })
    return RedirectResponse(
        "/student_login",
        status_code=303
    ) 
    # {
        # "message": "Registration Successfull" 
    # }


@app.post("/student_login")
def login(
    email: str = Form(...),
    password: str = Form(...)
):
    user = students.find_one({
        "email": email,
        "password": password
    })
    if user:
        return RedirectResponse (
            # "/dashboard",
            url=f"/student_dashboard?email={email}",
            status_code=303
        )
        # {
        #     "message": "Login Successfull",
        #     "name": user["name"]
        # }
    return RedirectResponse("/student_login", status_code=303)
    # {
    #     "message": "Invalid email or password"
    # }

@app.get("/student_dashboard", response_class=HTMLResponse)
def dashboard(request: Request, email: str):
    if email is None:
        return RedirectResponse("/student_login", status_code=303)
    student = students.find_one(
        {
            "email": email
        }
    )
    return templates.TemplateResponse(
        request = request,
        # student = student,
        name = "student_dashboard.html",
         context={
            "request": request,
            "student": student
        }
    )


# ------------------------------TEACHER------------------------------------------

@app.get("/teacher_login", response_class=HTMLResponse)
def teacher_page(request: Request):

    return templates.TemplateResponse(
        request = request,
        name= "teacher_login.html"
    )

@app.post("/teacher_login")
def teacher_login(
    request: Request,
    email:str = Form(...),
    password:str = Form(...)
  ):
    teacher = teachers.find_one({
        "email" : email,
        "password" : password
        })
    if teacher:
        # return {"message": "Successful Teacher login"}
        return RedirectResponse(
        #     "/teacher_dashboard",
            url=f"/teacher_dashboard?email={email}",
            status_code=303
        )
    return {"message": "Invalid Teacher login"}

@app.get("/teacher_dashboard", response_class=HTMLResponse)
def teacher_dashboard(request: Request, email:str):
    teacher = teachers.find_one({
        "email": email
    })

    if teacher is None:
        return RedirectResponse(
            "/teacher_login",
            status_code=303
        )

    all_students = list(
        students.find()
    )

    return templates.TemplateResponse(
        request= request,
        name="teacher_dashboard.html",
        context={
            "request": request,
            "teacher": teacher,
            "students": all_students
        }
    )


@app.get("/delete/{email}")
def delete(email:str):
    students.delete_one({
        "email": email
    })
    return RedirectResponse(
        # "/teacher_login",
        url=f"/teacher_dashboard?email={email}",
        status_code=303
    )

# add student by teacher
@app.post("/teacher_add_student")
def teacher_add_student(
    name: str = Form(...),
    roll_no: str = Form(...),
    id: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    user = students.find_one({
        "email": email
    })
    if user :
        return {"message": "User does  exit"}
    
    students.insert_one({
        "name": name,
        "roll_no": roll_no,
        "id": id,
        "email": email,
        "password": password
    })

    return RedirectResponse(
        # '/teacher_dashboard',
        url=f"/teacher_dashboard?email={email}",
        status_code=303
    )

@app.get("/update_student/{email}", response_class=HTMLResponse)
def update_page(request: Request, email: str, teacher_email: str):
    student = students.find_one({"email": email})
    teacher = teachers.find_one({"email": teacher_email})
    return templates.TemplateResponse(
        request=request,
        name="update_student.html",
        context={
            "request": request,
            "student": student,
            "teacher": teacher
        }
    )


@app.post("/update_student")
def update_page(
    old_email:str = Form(...),
    teacher_email:str = Form(...),
    name:str = Form(...),
    roll_no:str = Form(...),
    id:str = Form(...),
    email:str = Form(...),
    password:str = Form(...)
):
    student = students.update_one(
        {
            "email": old_email
        },
        {
            "$set": {
                "name": name,
                "roll_no": roll_no,
                "id": id,
                "email": email,
                "password": password
            }
        }
    )
    return RedirectResponse(
        url=f"/teacher_dashboard?email={teacher_email}",
        status_code=303
    )