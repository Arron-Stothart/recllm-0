FROM python:3.10-slim

WORKDIR /code

ENV HUGGING_FACE_HUB_TOKEN=${HUGGING_FACE_HUB_TOKEN}

# Create cache directory with proper permissions
RUN mkdir -p /.cache && chmod 777 /.cache

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir huggingface_hub

COPY . /code

CMD ["uvicorn", "recllm.app:app", "--host", "0.0.0.0", "--port", "7860"] 