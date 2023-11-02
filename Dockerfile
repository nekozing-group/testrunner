FROM shared:latest

COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /code

RUN chmod +x /code/entrypoint.py
ENTRYPOINT ["python", "/code/entrypoint.py"]