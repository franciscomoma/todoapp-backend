"""
Una demo hecha con FastAPI para el módulo de Puesta en Producción
"""
import json
import os
import sys
import logging
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

FILE_NAME = os.path.join('data', 'todo.json')

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Todo(BaseModel):
    id: int | None = 0
    message: str
    isDone: bool | None = False


def get_items():
    todo_items = {}
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, 'r') as file:
                todo_items = json.loads(file.read())
        except Exception as e:
            pass
    
    return todo_items

@app.get("/api/todo")
async def todo_list() -> object:
    """
    Obtiene el listado de todas las tareas
    """
    todo_items_list = [value for value in get_items().values()]

    return todo_items_list

@app.post("/api/todo")
async def create_todo(item: Todo) -> Todo:
    """
    Permite la creación de tareas
    """
    todo_items = get_items()

    item.id = len(todo_items) + 1

    todo_items[item.id] = dict(item)
    with open(FILE_NAME, 'w') as file:
        file.write(json.dumps(todo_items))

    return item

@app.delete("/api/todo/{id:str}")
async def todo_delete(id) -> object:
    """
    Permite la eliminación de tareas
    """
    todo_items = get_items()

    if id in todo_items:
        del todo_items[id]

        with open(FILE_NAME, 'w') as file:
            file.write(json.dumps(todo_items))

    return {}

@app.put("/api/todo/{id:str}")
async def todo_update(id, item: Todo) -> object:
    """
    Permite la actualización de tareas
    """
    todo_items = get_items()

    if id in todo_items:
        todo_items[id] = dict(item)

        with open(FILE_NAME, 'w') as file:
            file.write(json.dumps(todo_items))

    return item

@app.get("/api/err")
async def err() -> object:
    """
    """
    raise Exception("Error procesando la petición")
