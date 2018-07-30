FROM uisautomation/django:2.0

# Do everything relative to /usr/src/app which is where we install our
# application.
WORKDIR /usr/src/app

# Install development dependencies
RUN apk add --no-cache postgresql-client postgresql-dev bash

# Install any explicit requirements
ADD requirements*.txt ./
RUN pip install -r ./requirements_developer.txt

# Copy startup script
ADD ./compose/start-devserver.sh ./compose/wait-for-it.sh /tmp/

# The consent source will be mounted here as a volume
VOLUME /usr/src/app

EXPOSE 8000

# By default, use the Django development server to serve the application and use
# developer-specific settings.
#
# *DO NOT DEPLOY THIS TO PRODUCTION*
ENV DJANGO_SETTINGS_MODULE ucamoauth2consent.settings_developer
ENTRYPOINT ["/tmp/wait-for-it.sh", "development-db:5432", "--", "/tmp/start-devserver.sh"]
