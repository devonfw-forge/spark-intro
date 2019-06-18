#
# Spark Dockerfile
#

FROM java:8

# Install Spark
RUN \
  wget http://d3kbcqa49mib13.cloudfront.net/spark-2.2.0-bin-hadoop2.7.tgz -O spark.tgz && \
  tar -xf spark.tgz && \
  rm spark.tgz && \
  mv spark-* ~/spark

# Install Elasticsearch-Hadoop adapter
RUN \
  cd ~/spark && \
  cd jars && \
  wget http://central.maven.org/maven2/org/elasticsearch/elasticsearch-hadoop/7.1.1/elasticsearch-hadoop-7.1.1.jar
