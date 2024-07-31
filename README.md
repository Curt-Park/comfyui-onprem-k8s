# ComfyUI on an On-Premise Kubernetes Cluster

## Prerequisites
- Install [Docker](https://docs.docker.com/engine/install/)
- Install [Kubectl](https://kubernetes.io/docs/tasks/tools/)
- Install [Minikube](https://minikube.sigs.k8s.io/docs/start)

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
helm install traefik charts/traefik

# Install a ComfyUI service on the cluster.
helm install comfyui charts/comfyui
# Check the ComfyUI works.
kubectl get pods
```

## ComfyUI Test
```bash
make tunnel
```

### Browser
open http://localhost/comfyui

### Python Script
Under `test`,

Prerequisites:
```bash
conda create -n comfyui-test python=3.10 -y
conda activate comfyui-test
pip install -r requirements.txt
```

Run:
```bash
python main.py -s http://host-address/comfyui
```

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

## References
### GPU Time Slicing
- https://github.com/NVIDIA/k8s-device-plugin?tab=readme-ov-file#with-cuda-time-slicing
- https://nyyang.tistory.com/198

### ComfyUI + K8S
- https://github.com/aws-samples/comfyui-on-eks

### Ingress
- https://doc.traefik.io/traefik/routing/services/?ref=traefik.io#sticky-sessions
- https://doc.traefik.io/traefik/routing/providers/kubernetes-ingress/
