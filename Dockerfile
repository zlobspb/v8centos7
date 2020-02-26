FROM centos:7

RUN yum -y update \
    && yum install -y centos-release-scl \
    && yum install -y \
        git \
        rpm-build \
        make \
        glib2-devel \
        devtoolset-9-gcc \
        devtoolset-9-gcc-c++ \
        devtoolset-9-libatomic-devel \
    && yum clean all
