FROM ubuntu:20.04 as builder

WORKDIR /opt
COPY aws-ipf-v3.1.1.zip /opt

RUN apt update -y \
    && TZ="UTC" apt install -y tzdata \
    && apt install -y unzip

RUN mkdir -p /opt/aws/AWSat \
    && cd /opt \
    && mkdir /opt/aws/for_container \
    && unzip aws-ipf-v3.1.1.zip \
    && mv aws-ipf-v3.1.1/* /opt/aws/for_container/

COPY JobOrder_L0_template.xml /opt/aws/for_container/AWSat/JobOrder_L0_template.xml
COPY JobOrder_L1_template.xml /opt/aws/for_container/AWSat/JobOrder_L1_template.xml
COPY create_awsat_joborder.py /opt/aws/for_container/bin/
COPY DSDB_VCID_replace.py /opt/aws/for_container/bin/

FROM ubuntu:20.04

RUN apt-get update -y \
    && apt install -y \
       libpugixml1v5 \
       libnetcdf15 \
       libnetcdf-c++4-1 \
       libgomp1 \
       python3.9 \
       libopenblas0

COPY --from=builder /opt/aws/for_container/ /opt/aws/
COPY entrypoint.sh /opt/aws/bin/

ENTRYPOINT ["/opt/aws/bin/entrypoint.sh"]
