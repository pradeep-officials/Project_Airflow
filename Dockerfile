FROM apache/airflow:2.7.1
USER root
#RUN pip3 install --no-cache-dir apache-airflow-providers-apache-spark==4.7.1
# RUN pip3 install Faker numpy boto3 botocore --no-cache-dir apache-airflow-providers-apache-spark==4.7.1

RUN apt-get update && apt-get install -y gcc python3-dev openjdk-11-jdk && apt-get clean

# Set JAVA_HOME environment variable
# ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-arm64
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
USER airflow
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" apache-airflow-providers-apache-spark==2.1.3
# FROM apache/airflow:2.7.1
# # install Java
# USER root
# RUN echo "PRADEEP" >> /etc/apt/sources.list  
# RUN echo "deb http://security.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list                                                   
# RUN mkdir -p /usr/share/man/man1 && \
#     apt-get update -y && \
#     apt-get install -y openjdk-8-jdk

# RUN apt-get install unzip -y && \
#     apt-get autoremove -y

# USER airflow
# ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
# RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" apache-airflow-providers-apache-spark==2.1.3