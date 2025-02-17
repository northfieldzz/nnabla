# Copyright 2019,2020,2021 Sony Corporation.
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


import nnabla as nn
import nnabla.function as _F
import nnabla.functions as F

from .backward_function import UnaryDataGrad


class SumPoolingDataGrad(UnaryDataGrad):

    def __init__(self, ctx, kernel, stride=None, ignore_border=True, pad=None,
                 channel_last=False, including_pad=True):
        super(SumPoolingDataGrad, self).__init__(ctx)
        self._func = _F.SumPooling(ctx, kernel, stride, ignore_border, pad,
                                   channel_last)


def sum_pooling_backward(inputs, kernel, stride=None,
                         ignore_border=True, pad=None, channel_last=False):
    """
    Args:
      inputs (list of nn.Variable): Incomming grads/inputs to/of the forward function.
      kwargs (dict of arguments): Dictionary of the corresponding function arguments.

    Return:
      list of Variable: Return the gradients wrt inputs of the corresponding function.
    """
    dy = inputs[0]
    x0 = inputs[1]
    ctx = nn.get_current_context()
    df = SumPoolingDataGrad(ctx, kernel, stride,
                            ignore_border, pad, channel_last)
    df.xshape = x0.shape
    dx0 = df(dy)
    return dx0


def sum_pooling_data_grad_backward(inputs, kernel, stride=None,
                                   ignore_border=True, pad=None, channel_last=False):
    """
    Args:
      inputs (list of nn.Variable): Incomming grads/inputs to/of the forward function.
      kwargs (dict of arguments): Dictionary of the corresponding function arguments.

    Return:
      list of Variable: Return the gradients wrt inputs of the corresponding function.
    """
    gdx = inputs[0]
    gdy = F.sum_pooling(gdx, kernel, stride, ignore_border, pad, channel_last)
    return gdy
