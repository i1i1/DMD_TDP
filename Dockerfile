FROM python

RUN apt update \
    && apt install -y --no-install-recommends \
        libmariadb-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

COPY . /src

COPY ./entrypoint /entrypoint

ENTRYPOINT [ "/entrypoint" ]

