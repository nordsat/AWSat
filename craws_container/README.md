# Building container for CRAWS AWS Level1c processing

Clone the CRAWS repositorythis directory:

    git clone <craws repo url>

Build the container:

    podman build -t craws .

# Processing Level 1 data to Level 1c

Place Level1 data in a directory and create an output directory for Level 1c
data, for example `/tmp/level1b/` and `/tmp/level1c/`, respectively.

Run the container with mounted directories:

    podman run \
    --mount type=bind,source=/tmp/level1b,target=/level1b \
    --mount type=bind,source=/tmp/level1c,target=/level1c \
    --rm \
    localhost/craws

If this doesn't work, SELinux might prohibit bind mounts and the following
needs to be used instead:

    podman run \
    -v /tmp/level1b:/level1b:Z \
    -v /tmp/level1c:/level1c:Z \
    --rm \
    localhost/craws

After the processing completes (in 10-20 seconds) `/tmp/level1c`
should contain the processed Level 1c data.
