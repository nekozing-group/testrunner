FROM python:3.11.6-alpine3.18

COPY . /code

RUN pip install -r /code/requirements.txt

RUN chmod +x /code/entrypoint.py
ENTRYPOINT ["python", "/code/entrypoint.py"]