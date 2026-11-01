from fastapi import FastAPI ,Depends,HTTPException
from schemas import Todo as TodoSchema ,TodoCreate
from sqlalchemy.orm import Session
from database import SessionLocal,Base,engine
from models import Todo
Base.metadata.create_all(bind=engine)
app=FastAPI()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
#post the table in db
@app.post("/todos",response_model=TodoSchema)
def create(todo: TodoCreate,db:Session =Depends(get_db)):
    db_todo=Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
#get whole table
@app.get("/todos",response_model=list[TodoSchema])
def read_todos(db: Session =Depends(get_db)):
    return db.query(Todo).all()
#get single item using id
@app.get("/todos/{todo_id}",response_model=TodoSchema)
def read_todo(todo_id: int,db :Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id ==todo_id).first()
    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    return todo
#update todo
@app.put("/todos/{todo_id}",response_model=TodoSchema)
def update_todo(todo_id:int,updated:TodoCreate,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    for key,value in updated.dict().items():
        setattr(todo,key,value)
    db.commit()
    db.refresh(todo)
    return todo 
#delete 
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message":"Todo deleted sucesssfully"}
