FROM python:3.12-slim

WORKDIR /project

RUN pip install --no-cache-dir --upgrade pip "poetry==2.2.1" &&\
    poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root

COPY . .

CMD ["uvicorn", "crm.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
# python manage.py migrate && python manage.py collectstatic --noinput &&
