FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code

CMD ["uvicorn", "recllm.app:app", "--host", "0.0.0.0", "--port", "7860"] 