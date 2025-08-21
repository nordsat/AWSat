# Building AAPP-AWS container

Copy the AAPP source code to this directory:

    cp ~/Downloads/AAPP_8_15.tgz .

If the processor version/package name changes, Dockerfile needs to be
adjusted accordingly.

Build the container:

    podman build -t aapp-aws .

# Processing L1 data to L1c

Place L1 data in a directory and create an output directory for L1c
data, for example `/tmp/L1/` and `/tmp/L1c/`, respectively.

Create configuration files, for example to directory `/tmp/config/`:

    aws_bufr.nl
    aws_averaging.nl

Run the container with mounted directories:

    podman run \
    --mount type=bind,source=/tmp/L1,target=/data/L1 \
    --mount type=bind,source=/tmp/L1c,target=/data/L1c \
    --mount type=bind,source=/tmp/config,target=/config \
    --rm \
    localhost/aapp-aws

If this doesn't work, SELinux might prohibit bind mounts and the following
needs to be used instead:

    podman run \
    -v /tmp/L1:/data/L1:Z \
    -v /tmp/L1c:/data/L1c:Z \
    -v /tmp/config:/config:Z \
    --rm \
    localhost/aapp-aws

After the processing completes `/tmp/L1c` should contain one L1c BUFR
file for each of the L1 NetCDF4 files.
