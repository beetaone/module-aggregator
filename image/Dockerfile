FROM python:3.8-slim
WORKDIR /app
RUN mkdir -p /app
COPY ./image/requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
SHELL ["/bin/bash", "-c"]
COPY ./image/entrypoint.sh /entrypoint.sh
RUN ["chmod", "+x", "/entrypoint.sh"]
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 80