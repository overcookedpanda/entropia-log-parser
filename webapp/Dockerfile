FROM python:3
ADD entropia-log-parser.py /
RUN mkdir -p /uploads
RUN mkdir -p /templates
COPY templates/index.html /templates/index.html
RUN pip install flask
EXPOSE 5000
CMD [ "python", "./entropia-log-parser.py" ]
