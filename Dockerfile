# start by pulling the python image
FROM python:3.11-alpine

# copy the requirements file into the image
COPY requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# upgrade pip
RUN apk add py3-pip

# install postgre client
RUN apk add postgresql-client

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY ./app/*.py /app/app/
COPY ./app/.env /app/app/
COPY ./app/admin/*.py /app/app/admin/
COPY ./app/browse/*.py /app/app/browse/
COPY ./app/login/*.py /app/app/login/
COPY ./app/templates/*.html /app/app/templates/

# set flask env config
ENV FLASK_ENV "development"
ENV FLASK_APP "app:create_app('development')"

# run the app
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
#ENTRYPOINT [ "python3" ]