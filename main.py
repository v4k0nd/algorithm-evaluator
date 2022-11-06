import json
import database

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    results = await get_all()
    return templates.TemplateResponse("index.html", {"request": request, "results": results})
    # return await get_page(offset=0, limit=100)
    
@app.get('/api/results')
async def get_all():
    return await get_page(offset=0, limit=100)

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
