import psycopg2

from fastapi import FastAPI, Request
from dotenv import dotenv_values
from models.models import UserInput

env_vars = dotenv_values()

connection = psycopg2.connect(**env_vars)

app = FastAPI()



class Sql:
    '''Class to work with sql'''

    def work_with_sql(request: str, data: tuple = None):
        '''Func to work with sql requests'''

        with connection.cursor() as cursor:
            if data:
                cursor.execute(request, data)
                connection.commit()
                
                try:
                    response = cursor.fetchall()
                    return response
                
                except: return
            
            cursor.execute(request)
            connection.commit()

            try:
                    response = cursor.fetchall()
                    return response
                
            except: return


# Route to add task in db
@app.post('/add_task')
async def add_task(reqest: Request, data: UserInput):
    try:
        Sql.work_with_sql('''INSERT INTO todo(description, done)
                            VALUES (%s, false)
                            ''', (data.description,))
        
        return {'message': 'Task addeted successfully!'}
    
    except:
        return {'error': 'Something wrong!'}


# Route to del task in db
@app.delete('/del_task/{task_id}')
async def del_task(task_id: int):
    try:
        Sql.work_with_sql('''DELETE FROM todo
                            WHERE task_id = %s 
                            ''', (task_id,))
        
        return {'message': 'Task succesfully deleted'}
    
    except:
        return {'error': 'Something wrong'}
    

# Route to get task from db
@app.get('/get_task/{task_id}')
async def get_task(task_id: int):
    try:
        info = Sql.work_with_sql('''SELECT * 
                            FROM todo
                            WHERE task_id = %s 
                            ''', (task_id,))
        
        return {'task_id': info[0][0], 'description': info[0][1], 'done': info[0][2]}
    
    except:
        return {'error': 'Something wrong'}
    

# Route to get all tasks from db
@app.get('/get_all_tasks')
async def get_all_tasks(request: Request):
    try:
        info = Sql.work_with_sql('''SELECT * 
                            FROM todo
                            ''')
        
        return info
    
    except:
        return {'error': 'Something wrong'}
    

# Route to update task in db
@app.put('/put_task/{task_id}')
async def put_task(task_id: int, desc: str, done: bool):
    try:
        Sql.work_with_sql('''UPDATE todo
                            SET description = %s, done = %s
                            WHERE task_id = %s
                            ''', (desc, done, task_id))
        
        return {'message': 'Updated successfully'}
    
    except:
        return {'error': 'Something wrong'}
    

# Route to update task status in db
@app.put('/change_status/{task_id}')
async def change_status(task_id: int, done: bool):
    try:
        Sql.work_with_sql('''UPDATE todo
                            SET done = %s
                            WHERE task_id = %s
                            ''', (done, task_id))
        
        return {'message': 'Updated successfully'}
    
    except:
        return {'error': 'Something wrong'}