FROM alpine:3.8

WORKDIR /app

RUN apk add python3-dev openssl-dev libffi-dev gcc musl-dev \
    && pip3 install --upgrade pip
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["run.py"]
