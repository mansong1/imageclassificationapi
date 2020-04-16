#!/bin/bash
#
# Creates tfserver based on saved model
# Author: Martin Ansong <martin.ansong@gmail.com>

"""
./tfserver resnet http://download.tensorflow.org/models/official/20181001_resnet/savedmodels/resnet_v2_fp32_savedmodel_NHWC_jpg.tar.gz
"""

MODEL=$1
URL=$2

mkdir -p /tmp/${MODEL}

# Download pretrained model
curl -s ${URL} | \
tar --strip-components=2 -C /tmp/${MODEL} -xvz

docker run -d --name serving_base tensorflow/serving
# Move model to base image
docker cp /tmp/resnet serving_base:/models/resnet
docker commit --change "ENV MODEL_NAME ${MODEL}" serving_base \
  $USER/resnet_serving
docker kill serving_base
docker rm serving_base