# Building container for AWSat raw to Level1 processing

Copy the pre-built processor library package to this directory:

    cp ~/Downloads/v3.1.1.zip .

If the processor version/package name changes, Dockerfile needs to be
adjusted accordingly.

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

Run the container with mounted directories:

    podman run \
    --mount type=bind,source=/tmp/raw,target=/data/raw \
    --mount type=bind,source=/tmp/L1,target=/data/L1 \
    --rm \
    localhost/aws_pre_proc

If this doesn't work, SELinux might prohibit bind mounts and the following
needs to be used instead:

    podman run \
    -v /tmp/raw:/data/raw:Z \
    -v /tmp/L1:/data/L1:Z \
    --rm \
    localhost/aws_pre_proc

After the processing completes `/tmp/L1` should contain the processed
Level 1 data.
