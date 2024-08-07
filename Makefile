MODEL_PATH ?= $(HOME)/models
COMFYUI_VERSION ?= 82cae45
COMFYUI_MANAGER_VERSION ?= 694a2fc


# Cluster
cluster:
	@[ -d "$(MODEL_PATH)" ] || { echo "Please set MODEL_PATH"; exit 1; }
	# minikube v1.32.0-beta.0 or later (docker driver only).
	minikube start --driver docker --container-runtime docker \
		--gpus all \
		--mount \
		--mount-string $(MODEL_PATH):/minikube-host/models
	# create a secret to pull docker images.
	minikube kubectl -- create secret generic ghcr-reg \
		--from-file=.dockerconfigjson=$(HOME)/.docker/config.json \
		--type=kubernetes.io/dockerconfigjson
	# we use custom nvidia-device-plugin helm chart to enable MPS.
	minikube addons disable nvidia-device-plugin

cluster-removal:
	minikube delete


# Docker
docker-build:
	docker build -t ghcr.io/curt-park/comfyui-onprem-k8s:comfyui-$(COMFYUI_VERSION) \
		--build-arg COMFYUI_VERSION=$(COMFYUI_VERSION) \
		--build-arg COMFYUI_MANAGER_VERSION=$(COMFYUI_MANAGER_VERSION) \
		.

docker-push:
	docker push ghcr.io/curt-park/comfyui-onprem-k8s:comfyui-$(COMFYUI_VERSION)

docker-run:
	docker run -it --gpus all -p 50000:50000 \
		-v $(HOME)/models:/home/workspace/ComfyUI/models \
		ghcr.io/curt-park/comfyui-onprem-k8s:comfyui-$(COMFYUI_VERSION)


# Utils
tunnel:
	minikube tunnel --bind-address="0.0.0.0"
