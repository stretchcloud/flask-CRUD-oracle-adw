FROM oraclelinux:7-slim

# set working directory
WORKDIR /app

# set variable for Oracle Instant Client
ARG release=19
ARG update=3

# Install Oracle Instant Client
RUN  yum -y install oracle-release-el7 && yum-config-manager --enable ol7_oracle_instantclient && \
     yum -y install oracle-instantclient${release}.${update}-basic oracle-instantclient${release}.${update}-devel oracle-instantclient${release}.${update}-sqlplus && \
     rm -rf /var/cache/yum

# Install Python 3.6
RUN yum install -y oracle-softwarecollection-release-el7 && \
    yum-config-manager --enable software_collections && \
    yum-config-manager --enable ol7_latest ol7_optional_latest && \
    yum install -y scl-utils rh-python36 && \
    scl enable rh-python36 bash && \
    yum install -y python-pip 

## add instant client to path
ENV PATH=$PATH:/usr/lib/oracle/${release}.${update}/client64/bin
ENV TNS_ADMIN=/usr/lib/oracle/${release}.${update}/client64/lib/network/admin

# add wallet files
ADD ./wallet /usr/lib/oracle/${release}.${update}/client64/lib/network/admin/

# add files for python api
ADD ./createtable.py ./importcsv.py ./requirements.txt ./titanic.csv ./app.py /app/
RUN mkdir static
COPY static/swagger.yml static/swagger.yml

# Install required libraries
RUN /opt/rh/rh-python36/root/usr/bin/python3.6 -m pip install --upgrade pip
RUN /opt/rh/rh-python36/root/usr/bin/python3.6 -m pip install -r requirements.txt

# Create the Database Table and Inject the CSV Data
RUN /opt/rh/rh-python36/root/usr/bin/python3.6 createtable.py
RUN /opt/rh/rh-python36/root/usr/bin/python3.6 importcsv.py

### Expose the flask app port and run the main app#####
EXPOSE 5000
ENTRYPOINT ["/opt/rh/rh-python36/root/usr/bin/python3.6"]
CMD ["app.py"]
#######################################################