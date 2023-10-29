FROM python:3.11.6-alpine3.18

RUN pip install -r requirement.txt

COPY . /code

RUN chmod +x /code/entrypoint.py
ENTRYPOINT ["python", "/code/entrypoint.py"]