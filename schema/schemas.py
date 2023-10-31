def get_Info(cursor):
    results=[]
    for todo in cursor:
        result = {
   "id":str(todo["_id"]),
        "name":str(todo["name"]),
        "description":str(todo["description"]),
        "complete":str(todo["complete"])
    }
        results.append(result)
    return results

def lista_Todos(todos) -> list:
    return [get_Info(todo) for todo in todos]