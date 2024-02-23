FROM mambaorg/micromamba:latest
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1
EXPOSE 8888
WORKDIR /workdir
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-leaflet

CMD ["jupyter", "lab", "--port", "8888", "--ip", "0.0.0.0", "--no-browser"]