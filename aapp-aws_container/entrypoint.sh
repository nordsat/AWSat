#!/bin/bash

L1_INPUT_DIR=/data/L1
L1C_OUTPUT_DIR=/data/L1c
CONFIG_DIR=/config

source /opt/bin/aapp_aws_env.sh

cd $L1_INPUT_DIR
for f in *nc; do
    out_fname=${f%.nc}.bufr
    out_fname=`echo $out_fname | sed -e "s/1B/1C/g"`
    /opt/bin/aws_netcdf_to_bufr_1c.exe -i $f -b 3 -n /config/aws_bufr.nl -a /config/aws_averaging.nl -o $L1C_OUTPUT_DIR/${out_fname}
done
