  
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3



conn=sqlite3.connect("database.db",check_same_thread=False)
cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, completed BOOLEAN)
""")
conn.commit()

app=FastAPI()

@app.get("/")
def home():
    return {"message": "sql connenx successfull"}


@app.get("/about")
def about():
    return {"message": "About Page"}


# @app.get("/users")
# def users():
#     return {"users":["mohit","ram","shyam"]    
        #    }

# @app.get("/users/{user_id}")
# def get_user(user_id:int):
#     return {"user_id":user_id}    

@app.get("/users")
def get_user(name: str = None):
    return {"Name":name} 
           

@app.get("/products")
def get_user(limit: int = 200, min_price: int = 100):
    return {
        "Limit":limit,
        "Min_price":min_price
        } 

# @app.post("/create_user")
# def create_user(name=str,age=int):
#     return{
#         "Name":name,
#         "Age":age
#     }


# @app.post("/create_user")
# def create_user(user:dict):
#     return{
#         "Message":"user created successfully",
#         "data":user
#     }

# class User(BaseModel):
#     name:str
#     age:int
#     city:str

# @app.post("/create_user")
# def create_user(user:User):
#     return{
#         "Message":"user created successfully",
#         "data":user
#     }

# 

todos =[]


class Todo(BaseModel):
    id:int
    title:str
    completed:bool


@app.post("/todos")
def create_todo(todo:Todo):
    todos.append(todo)
    return{"message":"Todo added successfully","data":todos}


@app.get("/todos")
def get_todos():
    return{"message":"Todos fetched successfully","data":todos}

@app.get("/todos/{todo_id}")    
def get_todo(todo_id:int):
    for todo in todos:
        if todo.id == todo_id:
            return{"message":"Todo fetched successfully","data":todo}
    return{"message":"Todo not found"}



@app.put("/todos/{todo_id}")
def update_todo(todo_id:int,updated_todo:Todo):
    for index,todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return{"message":"Todo updated successfully","data":todos}
    return{"message":"Todo not found"}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int):
    for index,todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return{"message":"Todo deleted successfully","data":todos}
    return{"message":"Todo not found"}


@app.middleware("http")
async def my_middleware(request, call_next):
    print("Request received")

    response = await call_next(request)

    print("Response sent")
    return response

