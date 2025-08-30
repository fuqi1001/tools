FROM registry.access.redhat.com/ubi9/ubi-minimal:latest

RUN microdnf -y update && \
    microdnf -y install vim-minimal python3 python3-pip python3-virtualenv ca-certificates && \
    microdnf clean all

RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --upgrade pip
ENV PATH="/opt/venv/bin:${PATH}"

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
COPY . /app

CMD ["bash"]


# docker build -t my-vi-image -f Dockerfile .
# docker run -it --rm my-vi-image vi --version