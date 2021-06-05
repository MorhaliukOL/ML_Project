FROM tensorflow/tensorflow:2.4.0-jupyter

RUN apt-get update && apt-get install -y git
RUN /usr/bin/python3 -m pip install --upgrade pip

RUN mkdir -p /tf
WORKDIR /tf
ENV PYTHONPATH "${PYTHONPATH}:/tf"

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# enable jupyter notebook extensions
RUN jupyter contrib nbextension install --user
RUN jupyter nbextensions_configurator enable --user
RUN jupyter nbextension enable collapsible_headings/main
RUN jupyter nbextension enable varInspector/main