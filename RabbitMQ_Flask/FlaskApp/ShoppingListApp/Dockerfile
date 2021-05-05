FROM python:3.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . ./ShoppingListApp

#just for documentation, has no effect
EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0"]