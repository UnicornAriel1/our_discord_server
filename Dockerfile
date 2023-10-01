FROM python:3.9.6

COPY requirements.txt
RUN pip install -r requirements.txt

COPY main.py .
RUN --mount=type=secret,id=token_id TOKEN_ID=$(cat /run/secrets/token_id)
CMD ["python","./main.py"]