import asyncio
from datetime import datetime

import aiohttp
from transliterate import translit


async def parse_text_by_paragraphs(file_path):
    with open(file_path, encoding='utf-8-sig', mode='r') as file:
        paragraphs = []
        count_void_lines = 0
        for line in file:
            line = line.strip()
            if line:
                count_void_lines = 0
                paragraphs.append(line)
            elif count_void_lines > 2:
                yield {
                    'datetime': datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S.%f"),
                    'title': paragraphs[0],
                    'text': '\n'.join(paragraphs[1:])
                }
                paragraphs = []
                count_void_lines = 0
            else:
                count_void_lines += 1
        if paragraphs:
            yield {
                'datetime': datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S.%f"),
                'title': paragraphs[0],
                'text': '\n'.join(paragraphs[1:])
            }


async def parse_paragraph_by_lines(paragraph):
    for line in paragraph.split('\n'):
        yield line


async def file_parse(file_path, url):
    async with aiohttp.ClientSession() as session:
        async for paragraph in parse_text_by_paragraphs(file_path):
            try:
                table = str.maketrans("", "", "'!@#$%^&*+|+\/:;[]{}<>")
                topic = translit(paragraph["title"], language_code='ru', reversed=True).replace(" ", "_").translate(
                    table)
                params = {"topic": topic}
                async with session.post(url,
                                        params=params,
                                        json={"datetime": paragraph["datetime"],
                                              "title": paragraph["title"],
                                              "text": paragraph["text"]}) as response:
                    print(response.status)
                await asyncio.sleep(3)
            except aiohttp.ClientError as ex:
                print(ex)


def calculate_x_avg_count_in_line(text):
    count = 0
    for line in text.split('\n'):
        count += line.count('X')
    avg_count = count / len(text.split('\n'))
    return avg_count
