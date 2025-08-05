FROM ubuntu:20.04 as builder

WORKDIR /opt
COPY aws-ipf-v3.1.3_DEM_NOLSM.zip /opt

RUN apt update -y \
    && TZ="UTC" apt install -y tzdata \
    && apt install -y unzip

ARG sub_lsm_false='<parameter name="Use_Lsm" description="If true then Land/Sea Mask is used. If false then is not used" type="BOOLEAN">FALSE</parameter>'
ARG sub_lsm_true='<parameter name="Use_Lsm" description="If true then Land/Sea Mask is used. If false then is not used" type="BOOLEAN">TRUE</parameter>'

RUN mkdir -p /opt/aws/AWSat \
    && cd /opt \
    && mkdir /opt/aws/for_container \
    && unzip aws-ipf-v3.1.3_DEM_NOLSM.zip \
    && sed -i "s,$sub_lsm_false,$sub_lsm_true,g" aws-ipf-v3.1.3/conf/L1/AWS_L1_Configuration.xml \
    && rm -r aws-ipf-v3.1.3/example/Data \
    && rm -r aws-ipf-v3.1.3/example/conf \
    && rm -r aws-ipf-v3.1.3/example/ADF/AWS_AUX_DATA \
    && rm aws-ipf-v3.1.3/example/*.* \
    && mv aws-ipf-v3.1.3/* /opt/aws/for_container/

COPY JobOrder_L0_template.xml /opt/aws/for_container/AWSat/JobOrder_L0_template.xml
COPY JobOrder_L1_template.xml /opt/aws/for_container/AWSat/JobOrder_L1_template.xml
COPY create_awsat_joborder.py /opt/aws/for_container/bin/

FROM ubuntu:20.04

RUN apt-get update -y \
    && apt upgrade -y \
    && apt install -y \
       libpugixml1v5 \
       libnetcdf15 \
       libnetcdf-c++4-1 \
       libgomp1 \
       python3.9 \
       libopenblas0 \
    && apt clean

COPY --from=builder /opt/aws/for_container/ /opt/aws/
COPY entrypoint.sh /opt/aws/bin/

ENTRYPOINT ["/opt/aws/bin/entrypoint.sh"]
