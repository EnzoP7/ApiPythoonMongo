from fastapi import APIRouter
from fastapi import HTTPException


from models.todo import Todo
from database import collection_name
from schema.schemas import get_Info
from bson import ObjectId

router = APIRouter()

# GET Request Method
@router.get("/")
async def get_todos():
    cursor = collection_name.find({})
    todos = get_Info(cursor)
    return todos

@router.get("/{id}")
async def found_todo(id:str):
    elTodo =  collection_name.find_one({"_id":ObjectId(id)})
    elTodo["_id"] = str(elTodo["_id"])
    return elTodo

#Post Method
@router.post("/")
async def post_todo(todo:Todo):
    existing_todo = collection_name.find_one({"name":todo.name})
    if existing_todo:
        raise HTTPException(status_code=400, detail="Mensaje de error")
    collection_name.insert_one(dict(todo))
    return "Ingresado Con exito"


    # PUT Method

@router.put("/{id}")
async def put_todo(id:str, todo:Todo):
    collection_name.find_one_and_update({"_id":ObjectId(id)},{"$set": dict(todo)})
    return "Modificado Con exito"


@router.put("/Check/{id}")
async def put_todo(id: str):
    existing_todo = collection_name.find_one({"_id": ObjectId(id)})

    if not existing_todo:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    current_state = existing_todo.get("complete", False)  # Obtener el estado actual (si no existe, se establece en False)
    new_state = not current_state  # Cambiar al estado contrario
    print("ID:", id)
    print("Estado Actual:", current_state)
    print("Nuevo Estado:", new_state)
    collection_name.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": {"complete": new_state}}  # Establecer el nuevo estado
    )
    
    return "Modificado con éxito"








@router.delete("/{id}")
async def delete_todo(id:str):
    collection_name.find_one_and_delete({"_id":ObjectId(id)})
    return "Eliminado Con exito"