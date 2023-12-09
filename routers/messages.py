import asyncio

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.upload_message import send_messages, \
    consume_messages
from db.database import get_async_session
from db.models import TextEntry
from shemas.shemas import ReadStringXCount, Text

router = APIRouter()


@router.post("/publish", status_code=201)
async def publish_message(text: Text, topic: str):
    asyncio.create_task(send_messages(text, topic))
    consume = asyncio.create_task(consume_messages(topic))
    await consume
    return {'message': 'Message published successfully'}


@router.get('/results', response_model=List[ReadStringXCount])
async def get_results(session: AsyncSession = Depends(get_async_session)):
    async with session as s:
        query = select(TextEntry)
        results = await s.execute(query)
        return results.scalars().all()
