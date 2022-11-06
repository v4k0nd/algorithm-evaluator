import json
from fastapi import Request, FastAPI
import database

app = FastAPI()


@app.post('/api/result')
async def post(request: Request):
    return database.post(await request.json())


@app.get('/api/result/page/offset/{offset}/limit/{limit}')
async def get_page(offset: int, limit: int):
    return database.get(offset, limit)


@app.get('/api/result/id/{uuid}')
async def get_by_id(uuid):
    return database.get_by_id(uuid)


@app.delete('/api/result/id/{uuid}')
async def delete_by_id(uuid):
    return database.delete_by_id(uuid)
