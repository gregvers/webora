FROM oraclelinux:latest
WORKDIR /webora

RUN yum -y install libaio
COPY ./oracle-instantclient19.3-basic-19.3.0.0.0-1.x86_64.rpm /root
RUN rpm -i /root/oracle-instantclient19.3-basic-19.3.0.0.0-1.x86_64.rpm
#COPY ./oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm /root
#RUN rpm -i /root/oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm
#COPY ./tns/* /usr/lib/oracle/19.3/client64/network/admin/
ENV ORACLE_HOME=/usr/lib/oracle/19.3/client64
ENV PATH=/usr/lib/oracle/19.3/client64/bin:$PATH

RUN yum -y install python-pip
RUN pip install Flask
RUN pip install cx_oracle

ADD webora.py /webora
RUN mkdir /webora/templates
ADD templates/index.html /webora/templates

EXPOSE 5000
ENTRYPOINT python webora.py