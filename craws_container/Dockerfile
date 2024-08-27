FROM registry.access.redhat.com/ubi9/ubi-minimal AS builder

ENV MAMBA_ROOT_PREFIX=/opt/conda
ENV MAMBA_DISABLE_LOCKFILE=TRUE

COPY craws_main_20240821.tgz /tmp
COPY environment.yaml /tmp

RUN microdnf -y update && \
    microdnf -y install tar bzip2 gzip && \
    microdnf -y clean all

RUN mkdir /opt/conda && \
    curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj -C /usr/bin/ --strip-components=1 bin/micromamba && \
    micromamba shell init -s bash && \
    mv /root/.bashrc /opt/conda/.bashrc

RUN cd /tmp && \
    tar -xzvf craws_main_20240821.tgz && \
    mkdir /data && \
    cp tests/data/AWSat_example_orbit_6orb.nc /data/ && \
    cp tests/data/aws_remapping_weights.nc /data/ && \
    cp cfg/* /data/ && \
    echo "export REMAP_CONFIG=/data/remap_config.json" > /data/craws.cfg && \
    echo "export SCAN_CONFIG=/data/scan_config.json" >> /data/craws.cfg && \
    echo "export ORBIT_FILE=/data/AWSat_example_orbit_6orb.nc" >> /data/craws.cfg && \
    echo "export REMAP_WEIGHTS=/data" >> /data/craws.cfg

RUN source /opt/conda/.bashrc && \
    micromamba activate && \
    cd /tmp && \
    rm requirements.txt && \
    cat requirements.in | grep -v matplotlib > req.new && \
    mv req.new requirements.in && \
    micromamba install -y -f /tmp/environment.yaml && \
    pip install . && \
    pip cache purge && \
    micromamba remove -y --force pip && \
    micromamba clean -af -y && \
    chgrp -R 0 /opt/conda && \
    chmod -R g=u /opt/conda


# Create the final container
FROM registry.access.redhat.com/ubi9/ubi-minimal

RUN microdnf -y update \
    && microdnf -y clean all

COPY --from=builder /opt /opt
COPY --from=builder /data /data
COPY --from=builder /usr/bin/micromamba /usr/bin/
COPY entrypoint.sh /usr/bin/

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
