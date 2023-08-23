FROM python:3.7

LABEL org.opencontainers.image.source=https://github.com/avigailtaylor/GeneFEAST
LABEL org.opencontainers.image.description="GeneFEAST is a gene-centric functional enrichment analysis summarisation and visualisation tool implemented in Python."

RUN python3 -m pip install --upgrade pip

COPY . /opt

WORKDIR /opt

RUN pip install -e .

WORKDIR /

CMD ["gf"]


