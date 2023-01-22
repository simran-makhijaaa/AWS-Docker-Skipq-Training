FROM thoom/pyresttest

WORKDIR /usr/src/app

COPY ./tests /usr/src/app

ENTRYPOINT ["pyresttest"]

CMD ["https://6tekg52424.execute-api.us-east-2.amazonaws.com/", "restapi_tests.yml"]