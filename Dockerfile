FROM python:3.8-slim
WORKDIR /app
RUN mkdir -p /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python", "main.py"]
EXPOSE 80