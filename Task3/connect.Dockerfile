# Source:
# https://debezium.io/blog/2017/09/25/streaming-to-another-database/
# https://github.com/debezium/debezium-examples/blob/29c025335540e56b92b8121176ef9740c108be9b/unwrap-smt/debezium-jdbc/Dockerfile

FROM debezium/connect:2.0

# Deploy PostgreSQL JDBC Driver
RUN cd /kafka/libs && curl -sO https://jdbc.postgresql.org/download/postgresql-42.5.0.jar

# Deploy Kafka Connect JDBC
ENV KAFKA_CONNECT_JDBC_DIR=$KAFKA_CONNECT_PLUGINS_DIR/kafka-connect-jdbc
RUN mkdir $KAFKA_CONNECT_JDBC_DIR && cd $KAFKA_CONNECT_JDBC_DIR &&\
	curl -sO http://packages.confluent.io/maven/io/confluent/kafka-connect-jdbc/10.4.0/kafka-connect-jdbc-10.4.0.jar