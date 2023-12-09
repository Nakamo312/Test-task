import asyncio
import json
from datetime import datetime

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from config import APACHE_SERVER
from db.database import AsyncSessionLocal
from db.models import TextEntry
from shemas.shemas import Text
from utils.file_parse import parse_paragraph_by_lines, calculate_x_avg_count_in_line



async def process_message(message, avg):
    session = AsyncSessionLocal()
    entry = TextEntry(**message)
    entry.x_avg_count_in_line = avg
    session.add(entry)
    await session.commit()
    await session.close()


async def consume_messages(topic):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=APACHE_SERVER,
                                value_deserializer=lambda x: json.loads(x.decode("utf-8")))
    await consumer.start()
    count = 0
    count_x_in_line = 0
    message: dict = {}
    async for msg in consumer:
        if not msg.value:
            await consumer.stop()
            break
        else:
            count_x_in_line += msg.value["text"].count("X")
            count += 1
            message = msg.value

    avg = count_x_in_line / count
    del message["text"]
    date_format = '%d.%m.%Y %H:%M:%S.%f'
    message["datetime"] = datetime.strptime(message["datetime"], date_format)
    await process_message(message, avg)


async def send_messages(data: Text, topic):
    producer = AIOKafkaProducer(bootstrap_servers=APACHE_SERVER,
                                value_serializer=lambda x: json.dumps(x).encode("utf-8"))
    await producer.start()
    async for string in parse_paragraph_by_lines(data.text):
        message = {'datetime': data.datetime,
                   'title': data.title,
                   'text': string
                   }
        await producer.send(topic, message)
    await producer.send(topic, value='')
    await producer.stop()
