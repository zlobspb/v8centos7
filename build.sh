#!/bin/bash
set -xeuo pipefail
IFS=$'\n\t'

VERSION=${1:-8.0.426.25} #Chrome 80.0.3987.122

docker build -t v8centos7-builder -f Dockerfile .
docker run --rm -v $PWD:/v8 --name=v8centos7-builder-container v8centos7-builder \
    sh -c "V8_VERSION=$VERSION rpmbuild -bb /v8/v8_monolith.spec && cp /root/rpmbuild/RPMS/x86_64/v8_monolith-*.rpm /v8/"
