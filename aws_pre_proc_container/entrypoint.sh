#!/bin/bash

RAW_INPUT_DIR=/data/raw
L0_OUTPUT_DIR=/tmp
L1_OUTPUT_DIR=/data/L1

L0_JOBORDER=/opt/aws/JobOrder_L0.000.xml
L1_JOBORDER=/opt/aws/JobOrder_L1.001.xml
L0_JOBORDER_TEMPLATE=/opt/aws/AWSat/JobOrder_L0_template.xml
L1_JOBORDER_TEMPLATE=/opt/aws/AWSat/JobOrder_L1_template.xml

# The mission type can be given as environment variable. Default to "R".
# G - Global
# R - Regional
# L - Local

if [ "$MISSION_TYPE" == "" ]; then
    MISSION_TYPE="R"
fi

sed -i "s/MISSION_TYPE/$MISSION_TYPE/" $L0_JOBORDER_TEMPLATE
sed -i "s/MISSION_TYPE/$MISSION_TYPE/" $L1_JOBORDER_TEMPLATE

cd ${RAW_INPUT_DIR}
for f in *.*; do
    python3.9 /opt/aws/bin/DSDB_VCID_replace.py $f --replace-vcid 3 2
done

cd /opt/aws/

# Process RAW data to L0
python3.9 /opt/aws/bin/create_awsat_joborder.py -t $L0_JOBORDER_TEMPLATE -j $L0_JOBORDER -r $RAW_INPUT_DIR/*.*
/opt/aws/bin/IPF-AWS-L0 $L0_JOBORDER

# Process L0 to L1
python3.9 /opt/aws/bin/create_awsat_joborder.py -t $L1_JOBORDER_TEMPLATE -j $L1_JOBORDER -0 $L0_OUTPUT_DIR/*MWR* -n $L0_OUTPUT_DIR/*NAV*
/opt/aws/bin/IPF-AWS-L1 $L1_JOBORDER
