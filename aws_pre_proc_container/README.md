# Building container for AWSat raw to Level1 processing

Copy the pre-built processor library package to this directory:

    cp ~/Downloads/aws-ipf-v3.1.1.zip .

If the processor version/package name changes, Dockerfile needs to be
adjusted accordingly.

Extract and copy auxiliary data to a directory on the host machine:

    export AUX_DIR=/data/AWS_AUX_DATA
    unzip -j aws-ipf-v3.1.3_DEM_NOLSM.zip aws-ipf-v3.1.3/example/ADF/AWS_AUX_DATA/AUX_DEM/*ACE2 -d $AUX_DIR/AUX_DEM
    unzip -j aws-ipf-v3.1.3_DEM_NOLSM.zip aws-ipf-v3.1.3/example/ADF/AWS_AUX_DATA/GeoData/* -d $AUX_DIR/GeoData
    cp ~/Downloads/scdb_1.8.0.nc -d $AUX_DIR/SCDB/

The land/sea mask NetCDF4 files should be put to `$AUX_DIR/AUX_LSM` directory.

Copy also the Python script that changes the VCID to the build directory:

    cp ~/Downloads/20250303/DSDB_VCID_replace.py .

Adjust the processing parameters in the joborder XML files to match
your processing centre:

  * Processing_Station (default: Sodankyla)
  * location (default: Sodankyla)
  * organizator (default: FMI)
  * originator (default: FMI)

Leave other parts intact.

Build the container:

    podman build -t aws_pre_proc .

# Processing raw data to L1

Place raw data in a directory and create an output directory for L1
data, for example `/tmp/raw/` and `/tmp/L1/`, respectively.

The mission type can be set via environment variable (see commands below). There are three
valid options:

  * L - Local
  * R - Regional (default if not given)
  * G - Global

Run the container with mounted directories:

    podman run \
    -e MISSION_TYPE=R \
    --mount type=bind,source=/tmp/raw,target=/data/raw \
    --mount type=bind,source=/tmp/L1,target=/data/L1 \
    --mount type=bind,source=$AUX_DIR,target=/opt/aws/example/ADF/AWS_AUX_DATA \
    --rm \
    localhost/aws_pre_proc

If this doesn't work, SELinux might prohibit bind mounts and the following
needs to be used instead:

    podman run \
    -e MISSION_TYPE=R \
    -v /tmp/raw:/data/raw:Z \
    -v /tmp/L1:/data/L1:Z \
    -v $AUX_DIR:/opt/aws/example/ADF/AWS_AUX_DATA:Z \
    --rm \
    localhost/aws_pre_proc

After the processing completes `/tmp/L1` should contain the processed
Level 1 data.
