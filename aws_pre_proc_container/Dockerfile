FROM ubuntu:20.04 as builder

WORKDIR /opt
COPY aws-ipf-v2.0.0-repackaged-20230822.tar.7z /opt

RUN apt update -y \
    && TZ="UTC" apt install -y tzdata \
    && apt install -y build-essential \
       rsync \
       p7zip-full \
       cmake \
       valgrind \
       git \
       python3 \
       python3-pip \
       libnetcdf-c++4-dev \
       libfmt-dev \
       libspdlog-dev \
       libpugixml-dev \
       libboost-dev \
       libgomp1 \
       libopenblas-dev \
       liblapack-dev \
       libpugixml1v5 \
       libnetcdf15 \
       libnetcdf-c++4-1 \
       libgomp1 \
       libopenblas0 \
       liblapack3 \
    && pip3 install cpplint

RUN cd /opt \
    && 7z x aws-ipf-v2.0.0-repackaged-20230822.tar.7z \
    && tar xvvf aws-ipf-v2.0.0-repackaged-20230822.tar \
    && mv /opt/aws-ipf-v2.0.0-repackaged-20230822/ /opt/aws/ \
    && cd /opt/aws/COTS/CPPEOCFI/V4.25/libraries/LINUX64/ \
    && rm libproj.so.14 \
    && ln -s libproj.so.14.0.2 libproj.so.14 \
    && /opt/aws/support/scripts/build.sh

RUN cd /opt/aws \
    && mkdir for_container \
    && mkdir AWSat \
    && mv lib/ bin/ conf/ ADF/ AWSat/ for_container/

COPY JobOrder_L0_template.xml /opt/aws/for_container/AWSat/JobOrder_L0_template.xml
COPY JobOrder_L1_template.xml /opt/aws/for_container/AWSat/JobOrder_L1_template.xml
COPY create_awsat_joborder.py /opt/aws/for_container/AWSat/

FROM ubuntu:20.04

RUN apt-get update -y \
    && apt install -y p7zip-full \
       libpugixml1v5 \
       libnetcdf15 \
       libnetcdf-c++4-1 \
       libgomp1 \
       python3.9 \
       libopenblas0

COPY --from=builder /opt/aws/for_container /opt/aws/
COPY entrypoint.sh /opt/aws/bin/
ENTRYPOINT ["/opt/aws/bin/entrypoint.sh"]
