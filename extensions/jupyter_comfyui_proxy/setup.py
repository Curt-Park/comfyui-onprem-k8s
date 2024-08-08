import setuptools

setuptools.setup(
    name="jupyter-comfyui-proxy",
    version="0.1.0",
    url="https://github.com/curt-park/comfyui-onprem-k8s",
    author="Curt Park",
    description="Jupyter extension to proxy ComfyUI",
    install_requires=["jupyter-server-proxy>=3.2.3,!=4.0.0,!=4.1.0"],
    entry_points={
        "jupyter_serverproxy_servers": ["ComfyUI = jupyter_comfyui_proxy:setup_comfyui_server"]
    },
    package_data={
        "jupyter_comfyui_proxy": ["icons/comfyui.svg"],
    },
)
