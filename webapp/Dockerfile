FROM python:3
ADD entropia-log-parser.py /
RUN pip install flask
EXPOSE 80
CMD [ "python", "./entropia-log-parser.py" ]
