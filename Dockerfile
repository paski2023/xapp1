FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    git \
    python3.8 \
    python3-pip \
    protobuf-compiler

# install protobuf python module
RUN python3 -m pip install protobuf==3.20.* pandas 

# clone repo
RUN git clone https://github.com/paski2023/xapp1.git
WORKDIR /xapp1

# checkout mrn-base
RUN git checkout mrn-base

# synch submodules
RUN chmod +x submodule-sync.sh
RUN ./submodule-sync.sh

ENTRYPOINT ["/bin/bash"]
