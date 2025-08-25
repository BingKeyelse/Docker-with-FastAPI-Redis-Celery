from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from celery.result import AsyncResult
import asyncio

from celery_config import celery
from tasks import execute_llm

# import multiprocessing
# multiprocessing.set_start_method("spawn", force=True)

# lệnh run 
# celery -A celery_config worker --loglevel=info --concurrency=1 -P gevent

# uvicorn main_api_v1:app
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "task_id": "", "user_input": "", "msg": ""})

@app.post("/submit")
async def submit(text_input: str = Form(...)):
    task = execute_llm.delay(text_input)
    return JSONResponse({"task_id": task.id})

@app.websocket("/ws/{task_id}") #TH chạy đơn thuần
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()
    task_result = AsyncResult(task_id, app=celery)

    max_wait = 60  # tối đa 60 giây
    counter = 0
    while not task_result.ready() and counter < max_wait:
        await asyncio.sleep(1)
        counter += 1

    if task_result.ready():
        await websocket.send_text(task_result.get())
    else:
        await websocket.send_text("Task timeout")

    await websocket.close()

# @app.websocket("/ws/{task_id}")
# async def websocket_endpoint(websocket: WebSocket, task_id: str):
#     await websocket.accept()
#     task_result = AsyncResult(task_id, app=celery)

#     max_wait = 60  # tối đa 60 giây
#     counter = 0

#     while not task_result.ready() and counter < max_wait:
#         await asyncio.sleep(1)
#         counter += 1

#     if task_result.ready():
#         # Lấy kết quả không block
#         result = task_result.result
#         if result is not None:
#             await websocket.send_text(result)
#         else:
#             await websocket.send_text("Task completed but no result found")
#     else:
#         await websocket.send_text("Task timeout")

#     await websocket.close()

