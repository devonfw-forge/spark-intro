FROM python:3

WORKDIR /usr/src/app

# Install required libraries
COPY ./config/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./data/* ./

CMD ["python", "dump_titanic_data.py"]

# CMD [ "python", "./your-daemon-or-script.py" ]