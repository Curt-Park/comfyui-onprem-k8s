ARG BASE_IMAGE
FROM $BASE_IMAGE

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get upgrade --yes \
 && apt-get install --yes --no-install-recommends \
        ca-certificates \
        dnsutils \
        iputils-ping \
        tini \
        # requirement for nbgitpuller
        git \
 && rm -rf /var/lib/apt/lists/*

# install python packages.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /home/jovyan

# link comfyui user interactive directories to home
RUN rm -rf input output temp
RUN mkdir /home/jovyan/ComfyUI && cd /home/jovyan/ComfyUI && mkdir input output temp 
RUN ln -s /home/jovyan/ComfyUI/input /home/workspace/ComfyUI/input
RUN ln -s /home/jovyan/ComfyUI/output /home/workspace/ComfyUI/output
RUN ln -s /home/jovyan/ComfyUI/temp /home/workspace/ComfyUI/temp

RUN jupyter lab --generate-config

EXPOSE 8888
ENTRYPOINT ["tini", "--"]
CMD ["jupyter", "lab", "--ip", "0.0.0.0", "--port", "8888", "--allow-root"]
