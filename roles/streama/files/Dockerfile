FROM java:8-jre

ENV STREAMA_VERSION 1.9.2

RUN mkdir /streama
WORKDIR /streama

RUN wget https://github.com/streamaserver/streama/releases/download/v${STREAMA_VERSION}/streama-${STREAMA_VERSION}.jar && \
    mv streama-${STREAMA_VERSION}.jar streama.jar && \
    chmod +x streama.jar

#COPY application.yml /streama/base_application.yml

EXPOSE 8080
ENTRYPOINT ["java", "-Dgrails.env=mysql", "-jar", "streama.jar"]
