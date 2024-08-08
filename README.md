# ComfyUI on an On-Premise Kubernetes Cluster

## Prerequisites
- Install [Docker](https://docs.docker.com/engine/install/)
- Install [Kubectl](https://kubernetes.io/docs/tasks/tools/)
- Install [Minikube](https://minikube.sigs.k8s.io/docs/start)
- Login [GHCR](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic)

## Build ComfyUI (Optional)
```bash
make docker-build
make docker-push
make docker-run  # for testing
```

## Cluster Setup
```bash
MODEL_PATH=PATH_TO_MODELS make cluster
# Enable GPU Time-Slicing for multiple replicas.
helm install nvidia-device-plugin charts/nvidia-device-plugin -n kube-system
# Install Ingress.
kubectl create namespace ingress
helm install traefik charts/traefik -n ingress
```

## ComfyUI Service
```bash
helm install comfyui charts/comfyui
```

- Create a connection for testing in minikube: `make tunnel`
- open http://localhost/comfyui
- `cd test`
- `python main.py -s http://host-address/comfyui`

Result:
```bash
Generation started.
Generation not ready, sleep 1s ...
Generation not ready, sleep 1s ...
Generation finished.
Inference finished.
ClientID: 80e564e7-48ef-44cd-aae0-2a18fa091deb.
PromptID: 8882b193-d7d4-42e4-8003-7cdfe51a465d.
Num of images: 1.
Time spent: 2.17s.
------
```

NOTE:
- Set the proper host volume path in `charts/comfyui/values.yaml`

## ComfyUI + JupyterHub
```bash
helm install jupyterhub charts/jupyterhub
```

- `python main.py -s http://host-address/hub`
- login with `id: admin / pw: admin123!@#`

## References
### GPU Sharing on K8S
- https://github.com/NVIDIA/k8s-device-plugin?tab=readme-ov-file#with-cuda-time-slicing
- https://nyyang.tistory.com/198

### ComfyUI + K8S
- https://github.com/aws-samples/comfyui-on-eks

### Ingress
- https://doc.traefik.io/traefik/routing/services/?ref=traefik.io#sticky-sessions
- https://doc.traefik.io/traefik/routing/providers/kubernetes-ingress/

### JupyterHub
- https://z2jh.jupyter.org/en/stable/
- https://z2jh.jupyter.org/en/latest/administrator/services.html

### Jupyter Server Proxy
- https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html
- https://github.com/jupyterhub/jupyter-rsession-proxy/
