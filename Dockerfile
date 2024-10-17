FROM python:3.12

LABEL org.opencontainers.image.description="GeneFEAST is a gene-centric functional enrichment analysis summarisation and visualisation tool implemented in Python."

RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip setuptools

COPY . /opt

WORKDIR /opt

RUN pip install -e .

WORKDIR /

CMD ["gf"]
