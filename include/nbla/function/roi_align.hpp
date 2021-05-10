// Copyright (c) 2017 Sony Corporation. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef NBLA_FUNCTION_ROI_ALIGN_HPP
#define NBLA_FUNCTION_ROI_ALIGN_HPP

#include <nbla/cpu.hpp>
#include <nbla/function.hpp>
#include <nbla/function_registry.hpp>

namespace nbla {

NBLA_REGISTER_FUNCTION_HEADER(RoiAlign, const vector<int> &,
                              const vector<float> &, int, bool, bool);

/**
    @todo Write doc.

Inputs:

Outputs:

\ingroup FunctionImplGrp
 */
template <typename T>
class RoiAlign : public BaseFunction<const vector<int> &, const vector<float> &,
                                     int, bool, bool> {
protected:
  const vector<int> output_size_;
  const vector<float> spatial_scale_;
  int sampling_ratio_;
  bool aligned_;
  bool channel_last_;

public:
  RoiAlign(const Context &ctx, const vector<int> &output_size,
           const vector<float> &spatial_scale, int sampling_ratio, bool aligned,
           bool channel_last)
      : BaseFunction(ctx, output_size, spatial_scale, sampling_ratio, aligned,
                     channel_last),
        output_size_(output_size), spatial_scale_(spatial_scale),
        sampling_ratio_(sampling_ratio), aligned_(aligned),
        channel_last_(channel_last) {}
  virtual ~RoiAlign() {}
  virtual shared_ptr<Function> copy() const {
    return create_RoiAlign(ctx_, output_size_, spatial_scale_, sampling_ratio_,
                           aligned_, channel_last_);
  }
  virtual int min_inputs() { return 2; }
  virtual int min_outputs() { return 1; }
  virtual vector<dtypes> in_types() {
    return vector<dtypes>{get_dtype<T>(), get_dtype<T>()};
  }
  virtual vector<dtypes> out_types() { return vector<dtypes>{get_dtype<T>()}; }
  virtual vector<string> allowed_array_classes() {
    return SingletonManager::get<Cpu>()->array_classes();
  }
  virtual string name() { return "RoiAlign"; }

protected:
  NBLA_API virtual void setup_impl(const Variables &inputs,
                                   const Variables &outputs);
  NBLA_API virtual void forward_impl(const Variables &inputs,
                                     const Variables &outputs);
  NBLA_API virtual void backward_impl(const Variables &inputs,
                                      const Variables &outputs,
                                      const vector<bool> &propagate_down,
                                      const vector<bool> &accum);
};
}
#endif
