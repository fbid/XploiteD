FROM alpine:3.7

WORKDIR /app
COPY requirements.txt .

RUN \
  apk add --no-cache python3 postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
  apk add --no-cache libffi-dev jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev && \
  python3 -m pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

COPY . /app

ENTRYPOINT ["python3"]
CMD ["run.py", "--host=0.0.0.0"]
