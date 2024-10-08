# https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/main/images/singleuser-sample/Dockerfile
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
COPY docker/requirements-jupyter.txt requirements.txt
RUN pip install -r requirements.txt

# jupyter extensions.
COPY extensions /home/extensions
RUN pip install /home/extensions/jupyter_comfyui_proxy/.

WORKDIR /home/user
EXPOSE 8888
ENTRYPOINT ["tini", "--"]
CMD ["jupyter", "lab", "--ip", "0.0.0.0", "--port", "8888", "--allow-root"]
