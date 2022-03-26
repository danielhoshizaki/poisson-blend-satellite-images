FROM python:3.8.2-buster

RUN apt-get update && \
    apt-get install -y tzdata && \
    apt install -y \
      python3-gdal \
      python3-pip \
      libgl1-mesa-glx \
      libsuitesparse-dev \
      swig

RUN pip install -U \
      rasterio \
      scipy \
      scikit-learn \
      opencv-python \
      scikit-umfpack

WORKDIR /main