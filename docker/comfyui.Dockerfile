#FROM nvidia/cuda:12.1.0-runtime-ubuntu20.04
FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu22.04
ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /home/workspace

# python
RUN apt-get update 
    #&& apt-get install -y mesa-utils libgl1-mesa-dri libgtkgl2.0-dev libgtkglext1-dev git software-properties-common apt-utils \
RUN apt-get install -y build-essential curl python3-pip vim htop tmux
    #&& add-apt-repository ppa:deadsnakes/ppa \
    #a&& apt-get update \
    #&& apt install -y python3.10 python3.10-distutils curl \
    #&& apt install -y curl \
    #&& curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
    #&& htop python3-pip
#RUN apt-get install -y python3.10-dev

# torch and xformers
RUN pip install torch==2.6.0 torchvision==0.21 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu126 
#RUN pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --extra-index-url https://download.pytorch.org/whl/cu121

ARG COMFYUI_VERSION
ARG COMFYUI_MANAGER_VERSION

RUN apt install -y git
# clone ComfyUI
RUN git clone https://github.com/comfyanonymous/ComfyUI.git \
    && cd ComfyUI \
    && git checkout ${COMFYUI_VERSION}
RUN cd ComfyUI/custom_nodes \
    && git clone https://github.com/ltdrdata/ComfyUI-Manager.git \
    && cd ComfyUI-Manager \
    && git checkout ${COMFYUI_MANAGER_VERSION}

# install dependencies
RUN pip install -r ComfyUI/requirements.txt

# RUN
ENV PYTHON=python3
ENV COMFYUI_PATH=/home/workspace/ComfyUI
ENV PATH="$PATH:$COMFYUI_PATH"
WORKDIR $COMFYUI_PATH
CMD ["/bin/bash", "-c", "$PYTHON main.py --listen 0.0.0.0 --port 50000"]
