import numpy as np

from pyldpc import (make_ldpc, binaryproduct, ldpc_images, get_message)
from pyldpc.utils_img import gray2bin, bin2gray, rgb2bin, bin2rgb
import pytest
from itertools import product


@pytest.mark.parametrize("systematic, log, sparse",
                         product([False, True], [True], [False, True]))
def test_image_gray(systematic, log, sparse):

    n = 10
    d_v = 1
    d_c = 2
    seed = 0
    rnd = np.random.RandomState(seed)
    H, G = make_ldpc(n, d_v, d_c, seed=seed, systematic=systematic)
    assert not binaryproduct(H, G).any()

    n, k = G.shape
    print(n, k)
    snr = 100

    img = rnd.randint(0, 255, size=(3, 3))
    img_bin = gray2bin(img)
    coded, noisy = ldpc_images.encode_img(G, img_bin, snr, seed)

    x = ldpc_images.decode_img(G, H, coded, snr, maxiter=100, log=log)

    assert abs(img - x).sum() == 0


# @pytest.mark.parametrize("systematic, log, sparse",
#                          product([False, True], [True], [False, True]))
# def test_image_rgb(systematic, log, sparse):
#     n = 15
#     d_v = 4
#     d_c = 5
#     seed = 0
#
#     H, G = make_ldpc(n, d_v, d_c, seed=seed, systematic=systematic)
#     assert not binaryproduct(H, G).any()
#
#     n, k = G.shape
#     snr = 100
#
#     v = np.arange(k) % 2
#     y = encode(G, v, snr, seed)
#
#     d = decode(H, y, snr, maxiter=10, log=log)
#     x = get_message(G, d)
#
#     assert abs(v - x).sum() == 0