#!/bin/bash

echo "Installing Connector"
confluent-hub install --no-prompt debezium/debezium-connector-mysql:1.8.1

echo "Installing JDBC Connector"
confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:latest

echo "Download JDBC drivers"
cd /usr/share/confluent-hub-components/confluentinc-kafka-connect-jdbc/lib
curl https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.27/mysql-connector-java-8.0.27.jar -o mysql-connector-java-8.0.27.jar

echo "Launching Kafka Connect worker"
/etc/confluent/docker/run &

sleep infinity
