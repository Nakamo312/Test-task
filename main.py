import asyncio

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI

from config import HOST, PORT, NAME
from routers.messages import router as messages
from utils.file_parse import file_parse


def create_app():
    app = FastAPI(title='Text_broker', docs_url='/')
    app.include_router(
        router=messages,
        prefix="/message",
        tags=["Message"],
    )

    @app.on_event("startup")
    async def startup_event():
        url = f'http://localhost:{PORT}/message/publish'
        asyncio.create_task(file_parse('./O_Genri_Testovaya_20_vmeste (1).txt', url))

    return app


def main():
    uvicorn.run(
        f'{NAME}:create_app',
        host=HOST, port=PORT
    )


if __name__ == '__main__':
    main()
