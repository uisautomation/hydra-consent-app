# Use python alpine image to run webapp proper
FROM uisautomation/django:2.0-py3.6

# Ensure packages are up to date and install some useful utilities
RUN apk update && apk add --no-cache git vim postgresql-dev postgresql-client

# From now on, work in the application directory
WORKDIR /usr/src/app

# Copy Docker configuration and install any requirements. We install
# requirements/docker.txt last to allow it to override any versions in
# requirements/requirements.txt.
ADD ./requirements.txt ./requirements.txt
RUN pip install --upgrade --no-cache-dir -r requirements.txt

# Copy the remaining files over
ADD . .

# Default environment for image.  By default, we use the settings module bundled
# with this repo. Change DJANGO_SETTINGS_MODULE to install a custom settings.
#
# You probably want to modify the following environment variables:
#
# DJANGO_DB_ENGINE, DJANGO_DB_HOST, DJANGO_DB_PORT, DJANGO_DB_USER
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=ucamoauth2consent.settings.docker

# Collect static files. We provide placeholder values for required settings.
RUN DJANGO_SECRET_KEY=placeholder ./manage.py collectstatic -l

# Use gunicorn as a web-server after running migration command
CMD gunicorn \
	--name ucam-hydra-consent \
	--bind :8000 \
	--workers 3 \
	--log-level=info \
	--log-file=- \
	--access-logfile=- \
	--capture-output \
	ucamoauth2consent.wsgi
