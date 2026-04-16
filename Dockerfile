FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

<<<<<<< HEAD
ENV PYTHONPATH=/app

CMD ["python", "run.py"]
=======
CMD ["python", "app.py"]
>>>>>>> c2257bda3a866f6bfe5d3332c4782393f6c54cf5
