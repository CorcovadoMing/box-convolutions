import torch

import box_convolution_cpp_cuda as cpp_cuda

# TODO: rename `x_` and `y_` to `h_` and `w_`
class BoxConvolutionFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input, x_min, x_max, y_min, y_max):
        input_integrated = cpp_cuda.integral_image(input)
        ctx.save_for_backward(
            input_integrated, x_min, x_max, y_min, y_max)
        return cpp_cuda.box_convolution_forward(
            input_integrated, x_min, x_max, y_min, y_max)

    @staticmethod
    def backward(ctx, grad_output):
        input_integrated, x_min, x_max, y_min, y_max = ctx.saved_variables
        input_integrated_grad, = cpp_cuda.box_convolution_backward(
            input_integrated, x_min, x_max, y_min, y_max, grad_output, *ctx.needs_input_grad)
        return input_integrated_grad, x_min, x_max, y_min, y_max
