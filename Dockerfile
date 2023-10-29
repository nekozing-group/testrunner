FROM python:3.11.6-alpine3.18

RUN pip install pydantic

COPY . /testrunner

RUN chmod +x /testrunner/entrypoint.py
ENTRYPOINT ["python", "/testrunner/entrypoint.py"]