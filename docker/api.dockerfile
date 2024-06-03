FROM python:3.12.3

# Create directory for the app user
RUN mkdir -p /home/app

# Create the app user
RUN groupadd app && useradd -g app app

# Create the home directory
ENV APP_HOME=/home/app/api
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY . .

# Instala as dependências do projeto com o Poetry
RUN pip install poetry && \
    python -m poetry config virtualenvs.create false && \
    python -m poetry install

# --without=dev

RUN chown -R app:app $APP_HOME
USER app

CMD ["python", "-Xfrozen_modules=off", "-m", "uvicorn","app.main:app","--host=0.0.0.0","--port=8000","--reload"]