# Building container for AWSat raw to Level1 processing

Copy the processor source code to this directory:

    cp ~/Downloads/aws-ipf-v2.0.0-repackaged-20230822.tar.7z .

If the processor version/package name changes, Dockerfile needs to be
adjusted accordingly.

Adjust the processing parameters in thejoborder XML files to match
your processing centre:

  * location (default: Stockholm)
  * organization (default: OHB)
  * etc.

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

Now `/tmp/L1` should contain the processed Level 1 data.
