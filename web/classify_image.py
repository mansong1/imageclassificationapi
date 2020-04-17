# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Send JPEG image to tensorflow_model_server loaded with ResNet model.
"""

from __future__ import print_function

# This is a placeholder for a Google-internal import.

import grpc
import json
import requests
import numpy as np
import tensorflow as tf

from absl import app
from absl import flags
from tensorflow_serving.apis import classification_pb2
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

# The image URL is the location of the image we should send to the server
IMAGE_URL = 'http://farm1.static.flickr.com/140/396480043_d41cc3940e.jpg'

FLAGS = flags.FLAGS
flags.DEFINE_string('server', 'tfserver:8500',
                    'PredictionService host:port')
flags.DEFINE_string('image', '', 'path to image in JPEG format')

def main(_):
  if FLAGS.image:
    with open(FLAGS.image, 'rb') as f:
      data = f.read()
  else:
    # Download the image since we weren't given one
    dl_request = requests.get(IMAGE_URL, stream=True)
    dl_request.raise_for_status()
    data = dl_request.content

  imagenet_class_index = json.load(open('imagenet_class_index.json'))
  channel = grpc.insecure_channel(FLAGS.server)
  stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
  # Send request
  # See prediction_service.proto for gRPC request/response details.
  request = predict_pb2.PredictRequest()
  request.model_spec.name = 'resnet'
  request.model_spec.signature_name = 'serving_default'
  request.inputs['image_bytes'].CopyFrom(
      tf.make_tensor_proto(data, shape=[1]))
  
  result = stub.Predict(request, 10.0)  # 10 secs timeout

  predicted_idx = str(result.outputs['classes'].int64_val[0]-1) # Get predicted index
  with open("text.txt", 'w') as f:
    f.write(imagenet_class_index[predicted_idx][1]) #Check against imagenet_class_index
    f.close()

if __name__ == '__main__':
  tf.compat.v1.app.run()