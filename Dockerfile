FROM python:3.10-alpine
RUN adduser --disabled-password --uid 1000 infra && \
    apk add --update --no-cache yamllint


WORKDIR /infra
USER infra
COPY --chown=infra:infra . /infra

ENTRYPOINT ["/infra/bin/lint.sh", "/infra"]
