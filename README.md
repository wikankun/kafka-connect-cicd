# Kafka Connect CI/CD script and Secret Manager using File Config Provider

## Setup Environment

### Configuration files

- [Docker Compose File](./docker-compose.yaml)

    Add CONNECT_CONFIG_PROVIDERS and CONNECT_CONFIG_PROVIDERS_FILE_CLASS to environment
    ```
    kafka-connect:
        image: confluentinc/cp-kafka-connect:6.2.0
        hostname: kafka-connect
        ...
        environment:
            CONNECT_CONFIG_PROVIDERS: file
            CONNECT_CONFIG_PROVIDERS_FILE_CLASS: org.apache.kafka.common.config.provider.FileConfigProvider
    ```

- [Source Secret File](./secrets/source.properties)

    Add secret configuration `[key]:[value]`

    ```
    user=debezium
    password=dbz
    ```

- [Source File](./connectors/source.json)

    Call secret path configuration `${file:[path-to-file]:[key]}`

    ```
    "database.user": "${file:/secrets/source.properties:user}"
    ```

### Setup container

- Set container up and running

    ```
    docker-compose up -d
    ```

- Run cicd shell script

    ```
    . cicd.sh
    ```
    or run cicd python script

    ```
    python cicd.py
    ```

## Sources

- [Kafka Connect REST API Docs](https://docs.confluent.io/platform/current/connect/references/restapi.html)

- [Kafka Connect File Config Provider Docs](https://docs.confluent.io/platform/current/connect/security.html#fileconfigprovider)