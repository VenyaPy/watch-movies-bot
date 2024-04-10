FROM python:3.9-slim
WORKDIR /app
COPY main.py requirements.txt README.md config.py video.mp4 ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
CMD ["python", "main.py"]