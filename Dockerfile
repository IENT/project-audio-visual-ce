ARG BASE_IMAGE=registry.git.rwth-aachen.de/jupyter/profiles/rwth-courses
FROM ${BASE_IMAGE}

RUN conda install --quiet --yes \
	'scipy==1.4.1' \
    'scikit-image==0.16.2' \
    'opencv==4.2.0' \
	'scikit-learn==0.23.2' \
	'Pillow==7.2.0' \
	'pandas==1.1.3' \
    'cython==0.29.15' && \
	conda clean --all

RUN pip install --upgrade \
'git+https://git.rwth-aachen.de/jupyter/rwth-nb@v0.1.4' \
'tensorflow==1.15' \
'python-sofa==0.2.0'

RUN jupyter labextension install \
    @lckr/jupyterlab_variableinspector@0.5.1

USER root
RUN apt-get update && \
	apt-get -y install \
		lame \
        libgl1-mesa-glx && \
	rm -rf /var/lib/apt/lists/*

USER ${NB_USER}