FROM python:3.7-slim-buster

# Load and cache requirements
ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY ./ /app
EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "-b", "0.0.0.0", "ridesharing_fcm.wsgi"]