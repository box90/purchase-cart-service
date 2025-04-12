FROM python:3.13-slim

WORKDIR /mnt

COPY /src /mnt/src
COPY /tests /mnt/tests
COPY /requirements.txt /mnt/requirements.txt

RUN ls -l /mnt/src

RUN pip install --no-cache-dir -r /mnt/requirements.txt

EXPOSE 9090

CMD ["/bin/bash"]