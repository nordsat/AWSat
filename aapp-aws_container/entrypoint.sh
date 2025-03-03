#!/bin/bash

L1_INPUT_DIR=/data/L1
L1C_OUTPUT_DIR=/data/L1c

source /opt/bin/aapp-aws_env.sh

cd $L1_INPUT_DIR
for f in *nc; do
    /opt/bin/aws_netcdf_to_bufr_1c.exe -i $f -o $L1C_OUTPUT_DIR/${f%.nc}.bufr
done
