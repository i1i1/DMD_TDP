FROM python

RUN apt update \
    && apt install -y --no-install-recommends \
        libmariadb-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /src

RUN pip3 install -r /src/requirements.txt

COPY ./entrypoint /entrypoint

ENTRYPOINT [ "/entrypoint" ]

