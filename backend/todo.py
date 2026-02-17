from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    title: str
    description: str | None = None
    is_completed: bool = False

app = FastAPI()

todos = []

## get all todos
@app.get("/todos")
async def read_todos():
    return todos 

## add a new todo/ create a todo
@app.post("/todo")
async def create_todo(todo: Todo):
    todos.append(todo)
    return todo

## update a todo
@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo: Todo):
    for i, t in enumerate(todos):
        if t.id == todo_id:
            todos[i] = todo
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

## delete a todo
@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int):
    for i, t in enumerate(todos):
        if t.id == todo_id:
            todos.pop(i)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")