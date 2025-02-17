# collection of basic functions

import numpy as np

# A collection of activation functions
# INP: x : numpy ndarray of the size (batch_size, arbitrary size)

# activation functions
def step(x):
  if x > 0:
    return 1
  else:
    return 0

def sigmoid(x):
  y = 1 / (1 + np.exp(-x))
  return y

def relu(x):
  return np.maximum(0, x)

# output functions
# for regression
def identity(x):
  return x

# for classification
def softmax(x):
  c = np.max(x, axis=1, keepdims=True)
  x_exp = np.exp(x-c)
  x_exp_sum = np.sum(x_exp, axis=1, keepdims=True)
  y = x_exp / x_exp_sum
  return y

# loss functions
# INP: y, t : numpy ndarray with the size (batch_size, output_size)
#      y is the output, t is the teaching data

def square_error(y, t):
  assert y.shape == t.shape, "y and t should have the same shape"
  e = np.sum(np.square(y - t), axis=1) / 2
  return e


def mean_square_error(y, t):
  assert y.shape == t.shape, "y and t should have the same shape"
  e = np.sum(np.square(y - t), axis=1) / len(y)
  return e

# for classification
# INP: the elemens of y is in (0, 1)
#      t is (one-hot-label=True)
def cross_entropy_error(y, t):
  assert y.shape == t.shape, "y and t should have the same shape"
  delta = 1e-7 # to prevent log0 = -np.inf
  e = -np.sum(t * np.log(y + delta)) / t.shape[0] # the average loss
  return e

# function copied from https://www.oreilly.co.jp/books/9784873117584/
def im2col(input_data, filter_h, filter_w, stride=1, pad=0):
    """

    Parameters
    ----------
    input_data : (データ数, チャンネル, 高さ, 幅)の4次元配列からなる入力データ
    filter_h : フィルターの高さ
    filter_w : フィルターの幅
    stride : ストライド
    pad : パディング

    Returns
    -------
    col : 2次元配列
    """
    N, C, H, W = input_data.shape
    out_h = (H + 2*pad - filter_h)//stride + 1
    out_w = (W + 2*pad - filter_w)//stride + 1

    img = np.pad(input_data, [(0,0), (0,0), (pad, pad), (pad, pad)], 'constant')
    col = np.zeros((N, C, filter_h, filter_w, out_h, out_w))

    for y in range(filter_h):
        y_max = y + stride*out_h
        for x in range(filter_w):
            x_max = x + stride*out_w
            col[:, :, y, x, :, :] = img[:, :, y:y_max:stride, x:x_max:stride]

    col = col.transpose(0, 4, 5, 1, 2, 3).reshape(N*out_h*out_w, -1)
    return col


# funciton copied from https://www.oreilly.co.jp/books/9784873117584/
def col2im(col, input_shape, filter_h, filter_w, stride=1, pad=0):
    """

    Parameters
    ----------
    col :
    input_shape : 入力データの形状（例：(10, 1, 28, 28)）
    filter_h :
    filter_w
    stride
    pad

    Returns
    -------

    """
    N, C, H, W = input_shape
    out_h = (H + 2*pad - filter_h)//stride + 1
    out_w = (W + 2*pad - filter_w)//stride + 1
    col = col.reshape(N, out_h, out_w, C, filter_h, filter_w).transpose(0, 3, 4, 5, 1, 2)

    img = np.zeros((N, C, H + 2*pad + stride - 1, W + 2*pad + stride - 1))
    for y in range(filter_h):
        y_max = y + stride*out_h
        for x in range(filter_w):
            x_max = x + stride*out_w
            img[:, :, y:y_max:stride, x:x_max:stride] += col[:, :, y, x, :, :]

    return img[:, :, pad:H + pad, pad:W + pad]