# Copyright 2017,2018,2019,2020,2021 Sony Corporation.
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

import pytest
import numpy as np
import nnabla.functions as F
from nbla_test_utils import list_context

ctxs = list_context('HuberLoss')


def ref_huber_loss(x0, x1, delta):
    grad = (x0 - x1)
    q = np.minimum(np.abs(grad), delta)
    l = np.abs(grad) - q
    return q ** 2 + 2 * delta * l


@pytest.mark.parametrize("ctx, func_name", ctxs)
@pytest.mark.parametrize("seed", [313])
@pytest.mark.parametrize("delta", [0.5, 1.0, 2.0])
def test_huber_loss_forward_backward(seed, ctx, func_name, delta):
    from nbla_test_utils import function_tester
    rng = np.random.RandomState(seed)
    inputs = [rng.randn(2, 3, 4).astype(np.float32) * 2 for _ in range(2)]
    function_tester(rng, F.huber_loss, ref_huber_loss, inputs,
                    func_args=[delta],
                    atol_b=1e-2, ctx=ctx, func_name=func_name)


@pytest.mark.parametrize("ctx, func_name", ctxs)
@pytest.mark.parametrize("seed", [313])
@pytest.mark.parametrize("delta", [0.5, 1.0, 1.5])
def test_huber_loss_double_backward(seed, ctx, func_name, delta):
    from nbla_test_utils import cap_ignore_region, backward_function_tester
    rng = np.random.RandomState(seed)
    inputs = [rng.randn(2, 3, 4).astype(np.float32) * 2 for _ in range(2)]
    backward_function_tester(rng, F.huber_loss, inputs,
                             func_args=[delta],
                             atol_accum=1e-2, ctx=ctx)
