# Building container for CRAWS AWS Level1c processing

Copy the processor source code to this directory:

    cp ~/Downloads/craws_main_20240821.tgz .

If the processor version/package name changes, Dockerfile needs to be
adjusted accordingly.

Build the container:

    podman build -t craws .

# Processing Level 1 data to Level 1c

Place Level1 data in a directory and create an output directory for Level 1c
data, for example `/tmp/level1b/` and `/tmp/level1c/`, respectively.

Run the container with mounted directories:

    podman run \
    --mount type=bind,source=/tmp/level1b,target=/level1b \
    --mount type=bind,source=/tmp/level1b,target=/level1c \
    --rm \
    localhost/craws

After the processing completes (in 10-20 seconds) `/tmp/level1c`
should contain the processed Level 1c data.
