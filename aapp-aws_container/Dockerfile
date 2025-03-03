FROM registry.access.redhat.com/ubi9/ubi-minimal AS builder

RUN microdnf -y update \
    && microdnf -y install \
                tar \
		gzip \
		wget \
		gfortran \
		cmake \
		make \
		gcc \
		g++ \
		perl \
		m4 \
		zlib \
		zlib-devel \
    && microdnf -y clean all

# Install ECCodes
RUN cd /tmp \
    && wget https://confluence.ecmwf.int/download/attachments/45757960/eccodes-2.32.1-Source.tar.gz \
    && tar -xzvf eccodes-2.32.1-Source.tar.gz \
    && mkdir -p eccodes_build \
    && cd /tmp/eccodes_build \
    && cmake \
       -DCMAKE_INSTALL_PREFIX=/opt/eccodes \
       -DCMAKE_Fortran_COMPILER=gfortran \
       -DENABLE_AEC=OFF \
       ../eccodes-2.32.1-Source \
    && make \
    && make install

# Install HDF5
RUN cd /tmp \
    && wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.1/src/hdf5-1.10.1.tar.gz \
    && tar -xzvf hdf5-1.10.1.tar.gz \
    && cd hdf5-1.10.1 \
    && mkdir /opt/hdf5 \
    && ./configure --prefix=/opt/hdf5 --enable-fortran \
    && make \
    && make install

# Install NetCDF4
RUN cd /tmp \
    && wget https://github.com/Unidata/netcdf-c/archive/refs/tags/v4.8.1.tar.gz \
    && tar -xzvf v4.8.1.tar.gz \
    && cd /tmp/netcdf-c-4.8.1 \
    && export LDFLAGS="-L/opt/hdf5/lib" \
    && export CPPFLAGS="-I/opt/hdf5/include" \
    && ./configure --prefix=/opt/hdf5 --disable-dap \
    && make \
    && make install

# Install NetCDF4-fortran
RUN cd /tmp \
    && wget https://github.com/Unidata/netcdf-fortran/archive/refs/tags/v4.5.3.tar.gz \
    && tar -xzvf v4.5.3.tar.gz \
    && cd /tmp/netcdf-fortran-4.5.3 \
    && export LD_LIBRARY_PATH=/opt/hdf5/lib \
    && export LDFLAGS="-L/opt/hdf5/lib" \
    && export CPPFLAGS="-I/opt/hdf5/include" \
    && ./configure --prefix=/opt/hdf5 \
    && make \
    && make install

# Install AAPP-AWS
COPY AAPP-AWS_20231031.tar /tmp
RUN cd /tmp \
    && tar -xvf AAPP-AWS_20231031.tar \
    && export ECCODES_INSTALL_DIR=/opt/eccodes \
    && export NETCDF_INSTALL_DIR=/opt/hdf5 \
    && export FC=gfortran \
    && cd AAPP-AWS/src \
    && ./configure_aapp_aws.sh \
    && make \
    && cp -r /tmp/AAPP-AWS/bin /opt

# Create the final container
FROM registry.access.redhat.com/ubi9/ubi-minimal

RUN microdnf -y update \
    && microdnf -y install zlib libgfortran \
    && microdnf -y clean all

COPY --from=builder /opt /opt
COPY entrypoint.sh /usr/bin/

RUN ls /opt/bin
ENTRYPOINT ["/usr/bin/entrypoint.sh"]
