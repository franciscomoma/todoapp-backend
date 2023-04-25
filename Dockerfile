FROM python:3.11-slim
RUN pip install --upgrade pip
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
