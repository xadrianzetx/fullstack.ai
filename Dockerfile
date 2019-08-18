FROM python:3
WORKDIR /fullstack.ai
COPY . /fullstack.ai
RUN apt-get update && pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 4242
CMD ["python", "app.py"]
