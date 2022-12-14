FROM python:3.8
LABEL maintainer="StephanStu"
# command to create the working directory in container
WORKDIR /usr/src/techtrends
# command to copy everything (./) from "this-path/techtrends" into the WORKDIR
COPY ./techtrends ./
# command(s) to install dependencies
RUN pip install -r requirements.txt
RUN python init_db.py
# command to expose port 3111
EXPOSE 3111
# command to run on container start
CMD [ "python", "app.py" ]
