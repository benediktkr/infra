FROM benediktkr/poetry:3.9

USER 0
RUN python3 -m pip install yamllint
COPY . /infra
WORKDIR /infra

CMD ["/infra/lint.sh", "/infra"]
