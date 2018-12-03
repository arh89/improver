# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# (C) British Crown Copyright 2017-2018 Met Office.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""
Module to contain a saturated vapour pressure (SVP) lookup table.

The data held in this table were created using the utilties.ancillary_creation
plugin SaturatedVapourPressureTable, rounded to 6 decimal places. That plugin
employs the Goff-Gratch method to produce values for given temperatures.

The values contained here are for SVP in a pure water vapour system. A
correction is applied to convert these to SVP in air; see the
WetBulbTemperature._pressure_correct_svp function. The correction is applied
subsequently to keep the method aligned with that employed in the Met
Office UM.

Values are given in units of Pa.

A value of SVP for any temperature between T_min and T_max (inclusive) can be
obtained by interpolating through the table, as is done in the
WetBulbTemperature_lookup_svp function.
"""

import numpy as np

# These values describe the range in temperatures covered by the table and
# the increments at which data points are given.
T_MIN = 183.15
T_MAX = 338.15
T_INCREMENT = 0.1

DATA = np.array([
    9.664590e-03, 9.842644e-03, 1.002378e-02, 1.020805e-02, 1.039551e-02,
    1.058619e-02, 1.078017e-02, 1.097749e-02, 1.117820e-02, 1.138236e-02,
    1.159002e-02, 1.180124e-02, 1.201609e-02, 1.223460e-02, 1.245685e-02,
    1.268289e-02, 1.291279e-02, 1.314660e-02, 1.338438e-02, 1.362621e-02,
    1.387214e-02, 1.412224e-02, 1.437658e-02, 1.463522e-02, 1.489823e-02,
    1.516568e-02, 1.543763e-02, 1.571417e-02, 1.599536e-02, 1.628127e-02,
    1.657199e-02, 1.686758e-02, 1.716811e-02, 1.747368e-02, 1.778435e-02,
    1.810021e-02, 1.842134e-02, 1.874781e-02, 1.907972e-02, 1.941714e-02,
    1.976016e-02, 2.010887e-02, 2.046336e-02, 2.082372e-02, 2.119003e-02,
    2.156238e-02, 2.194088e-02, 2.232562e-02, 2.271668e-02, 2.311417e-02,
    2.351819e-02, 2.392884e-02, 2.434622e-02, 2.477042e-02, 2.520156e-02,
    2.563975e-02, 2.608508e-02, 2.653766e-02, 2.699762e-02, 2.746505e-02,
    2.794007e-02, 2.842280e-02, 2.891336e-02, 2.941185e-02, 2.991841e-02,
    3.043315e-02, 3.095620e-02, 3.148767e-02, 3.202771e-02, 3.257643e-02,
    3.313396e-02, 3.370045e-02, 3.427601e-02, 3.486080e-02, 3.545493e-02,
    3.605856e-02, 3.667183e-02, 3.729488e-02, 3.792785e-02, 3.857089e-02,
    3.922415e-02, 3.988778e-02, 4.056194e-02, 4.124678e-02, 4.194245e-02,
    4.264913e-02, 4.336696e-02, 4.409612e-02, 4.483676e-02, 4.558907e-02,
    4.635320e-02, 4.712933e-02, 4.791765e-02, 4.871831e-02, 4.953152e-02,
    5.035744e-02, 5.119627e-02, 5.204818e-02, 5.291338e-02, 5.379205e-02,
    5.468439e-02, 5.559060e-02, 5.651087e-02, 5.744542e-02, 5.839444e-02,
    5.935815e-02, 6.033675e-02, 6.133046e-02, 6.233950e-02, 6.336409e-02,
    6.440445e-02, 6.546080e-02, 6.653338e-02, 6.762241e-02, 6.872814e-02,
    6.985079e-02, 7.099061e-02, 7.214785e-02, 7.332275e-02, 7.451556e-02,
    7.572654e-02, 7.695594e-02, 7.820402e-02, 7.947105e-02, 8.075730e-02,
    8.206303e-02, 8.338852e-02, 8.473405e-02, 8.609990e-02, 8.748635e-02,
    8.889370e-02, 9.032223e-02, 9.177224e-02, 9.324404e-02, 9.473792e-02,
    9.625420e-02, 9.779319e-02, 9.935519e-02, 1.009405e-01, 1.025496e-01,
    1.041826e-01, 1.058399e-01, 1.075219e-01, 1.092289e-01, 1.109612e-01,
    1.127193e-01, 1.145034e-01, 1.163139e-01, 1.181512e-01, 1.200156e-01,
    1.219076e-01, 1.238274e-01, 1.257755e-01, 1.277523e-01, 1.297581e-01,
    1.317934e-01, 1.338585e-01, 1.359538e-01, 1.380799e-01, 1.402370e-01,
    1.424256e-01, 1.446461e-01, 1.468991e-01, 1.491848e-01, 1.515037e-01,
    1.538564e-01, 1.562432e-01, 1.586646e-01, 1.611211e-01, 1.636131e-01,
    1.661411e-01, 1.687057e-01, 1.713072e-01, 1.739462e-01, 1.766233e-01,
    1.793388e-01, 1.820933e-01, 1.848873e-01, 1.877214e-01, 1.905961e-01,
    1.935119e-01, 1.964694e-01, 1.994691e-01, 2.025116e-01, 2.055975e-01,
    2.087272e-01, 2.119015e-01, 2.151208e-01, 2.183859e-01, 2.216972e-01,
    2.250554e-01, 2.284611e-01, 2.319149e-01, 2.354175e-01, 2.389695e-01,
    2.425715e-01, 2.462243e-01, 2.499283e-01, 2.536844e-01, 2.574933e-01,
    2.613554e-01, 2.652717e-01, 2.692428e-01, 2.732693e-01, 2.773521e-01,
    2.814918e-01, 2.856891e-01, 2.899449e-01, 2.942598e-01, 2.986347e-01,
    3.030703e-01, 3.075674e-01, 3.121267e-01, 3.167491e-01, 3.214354e-01,
    3.261863e-01, 3.310028e-01, 3.358856e-01, 3.408357e-01, 3.458538e-01,
    3.509408e-01, 3.560977e-01, 3.613252e-01, 3.666243e-01, 3.719959e-01,
    3.774409e-01, 3.829603e-01, 3.885549e-01, 3.942257e-01, 3.999738e-01,
    4.058000e-01, 4.117053e-01, 4.176908e-01, 4.237574e-01, 4.299062e-01,
    4.361382e-01, 4.424544e-01, 4.488559e-01, 4.553438e-01, 4.619191e-01,
    4.685829e-01, 4.753363e-01, 4.821804e-01, 4.891164e-01, 4.961455e-01,
    5.032686e-01, 5.104871e-01, 5.178021e-01, 5.252148e-01, 5.327264e-01,
    5.403381e-01, 5.480511e-01, 5.558668e-01, 5.637863e-01, 5.718110e-01,
    5.799420e-01, 5.881808e-01, 5.965287e-01, 6.049870e-01, 6.135569e-01,
    6.222400e-01, 6.310375e-01, 6.399510e-01, 6.489817e-01, 6.581311e-01,
    6.674006e-01, 6.767918e-01, 6.863060e-01, 6.959448e-01, 7.057097e-01,
    7.156022e-01, 7.256238e-01, 7.357761e-01, 7.460607e-01, 7.564791e-01,
    7.670330e-01, 7.777240e-01, 7.885537e-01, 7.995238e-01, 8.106361e-01,
    8.218921e-01, 8.332936e-01, 8.448423e-01, 8.565400e-01, 8.683885e-01,
    8.803895e-01, 8.925449e-01, 9.048566e-01, 9.173262e-01, 9.299558e-01,
    9.427472e-01, 9.557024e-01, 9.688232e-01, 9.821116e-01, 9.955696e-01,
    1.009199e+00, 1.023003e+00, 1.036981e+00, 1.051138e+00, 1.065474e+00,
    1.079993e+00, 1.094695e+00, 1.109584e+00, 1.124660e+00, 1.139928e+00,
    1.155388e+00, 1.171043e+00, 1.186896e+00, 1.202948e+00, 1.219202e+00,
    1.235660e+00, 1.252325e+00, 1.269199e+00, 1.286284e+00, 1.303583e+00,
    1.321099e+00, 1.338833e+00, 1.356789e+00, 1.374968e+00, 1.393374e+00,
    1.412009e+00, 1.430876e+00, 1.449977e+00, 1.469315e+00, 1.488893e+00,
    1.508713e+00, 1.528778e+00, 1.549092e+00, 1.569656e+00, 1.590474e+00,
    1.611549e+00, 1.632883e+00, 1.654480e+00, 1.676342e+00, 1.698472e+00,
    1.720874e+00, 1.743550e+00, 1.766504e+00, 1.789739e+00, 1.813258e+00,
    1.837063e+00, 1.861159e+00, 1.885549e+00, 1.910236e+00, 1.935223e+00,
    1.960513e+00, 1.986110e+00, 2.012018e+00, 2.038240e+00, 2.064778e+00,
    2.091638e+00, 2.118823e+00, 2.146335e+00, 2.174179e+00, 2.202359e+00,
    2.230877e+00, 2.259739e+00, 2.288947e+00, 2.318505e+00, 2.348418e+00,
    2.378690e+00, 2.409323e+00, 2.440323e+00, 2.471693e+00, 2.503437e+00,
    2.535559e+00, 2.568064e+00, 2.600956e+00, 2.634239e+00, 2.667917e+00,
    2.701995e+00, 2.736476e+00, 2.771366e+00, 2.806669e+00, 2.842389e+00,
    2.878530e+00, 2.915098e+00, 2.952097e+00, 2.989532e+00, 3.027407e+00,
    3.065727e+00, 3.104497e+00, 3.143722e+00, 3.183407e+00, 3.223556e+00,
    3.264175e+00, 3.305268e+00, 3.346841e+00, 3.388900e+00, 3.431448e+00,
    3.474492e+00, 3.518036e+00, 3.562087e+00, 3.606649e+00, 3.651727e+00,
    3.697328e+00, 3.743458e+00, 3.790120e+00, 3.837322e+00, 3.885069e+00,
    3.933366e+00, 3.982220e+00, 4.031637e+00, 4.081622e+00, 4.132181e+00,
    4.183321e+00, 4.235047e+00, 4.287366e+00, 4.340284e+00, 4.393807e+00,
    4.447942e+00, 4.502695e+00, 4.558073e+00, 4.614081e+00, 4.670727e+00,
    4.728017e+00, 4.785959e+00, 4.844558e+00, 4.903822e+00, 4.963758e+00,
    5.024372e+00, 5.085671e+00, 5.147664e+00, 5.210356e+00, 5.273755e+00,
    5.337869e+00, 5.402705e+00, 5.468270e+00, 5.534572e+00, 5.601618e+00,
    5.669417e+00, 5.737975e+00, 5.807301e+00, 5.877402e+00, 5.948287e+00,
    6.019963e+00, 6.092439e+00, 6.165722e+00, 6.239822e+00, 6.314746e+00,
    6.390502e+00, 6.467100e+00, 6.544548e+00, 6.622854e+00, 6.702027e+00,
    6.782077e+00, 6.863011e+00, 6.944838e+00, 7.027569e+00, 7.111211e+00,
    7.195775e+00, 7.281269e+00, 7.367703e+00, 7.455087e+00, 7.543429e+00,
    7.632739e+00, 7.723028e+00, 7.814305e+00, 7.906579e+00, 7.999862e+00,
    8.094162e+00, 8.189491e+00, 8.285858e+00, 8.383274e+00, 8.481749e+00,
    8.581294e+00, 8.681919e+00, 8.783635e+00, 8.886454e+00, 8.990385e+00,
    9.095440e+00, 9.201630e+00, 9.308966e+00, 9.417460e+00, 9.527123e+00,
    9.637967e+00, 9.750002e+00, 9.863242e+00, 9.977697e+00, 1.009338e+01,
    1.021030e+01, 1.032848e+01, 1.044791e+01, 1.056863e+01, 1.069063e+01,
    1.081394e+01, 1.093856e+01, 1.106451e+01, 1.119179e+01, 1.132043e+01,
    1.145044e+01, 1.158182e+01, 1.171460e+01, 1.184878e+01, 1.198439e+01,
    1.212143e+01, 1.225991e+01, 1.239986e+01, 1.254128e+01, 1.268419e+01,
    1.282861e+01, 1.297454e+01, 1.312201e+01, 1.327103e+01, 1.342161e+01,
    1.357376e+01, 1.372751e+01, 1.388287e+01, 1.403985e+01, 1.419847e+01,
    1.435874e+01, 1.452069e+01, 1.468432e+01, 1.484965e+01, 1.501670e+01,
    1.518549e+01, 1.535603e+01, 1.552833e+01, 1.570242e+01, 1.587831e+01,
    1.605602e+01, 1.623557e+01, 1.641697e+01, 1.660023e+01, 1.678539e+01,
    1.697245e+01, 1.716144e+01, 1.735236e+01, 1.754525e+01, 1.774011e+01,
    1.793698e+01, 1.813585e+01, 1.833676e+01, 1.853973e+01, 1.874477e+01,
    1.895189e+01, 1.916113e+01, 1.937250e+01, 1.958602e+01, 1.980172e+01,
    2.001960e+01, 2.023969e+01, 2.046201e+01, 2.068659e+01, 2.091344e+01,
    2.114258e+01, 2.137404e+01, 2.160783e+01, 2.184398e+01, 2.208252e+01,
    2.232345e+01, 2.256680e+01, 2.281260e+01, 2.306087e+01, 2.331163e+01,
    2.356491e+01, 2.382071e+01, 2.407908e+01, 2.434003e+01, 2.460359e+01,
    2.486978e+01, 2.513862e+01, 2.541014e+01, 2.568436e+01, 2.596131e+01,
    2.624101e+01, 2.652349e+01, 2.680877e+01, 2.709687e+01, 2.738783e+01,
    2.768166e+01, 2.797840e+01, 2.827807e+01, 2.858070e+01, 2.888631e+01,
    2.919492e+01, 2.950658e+01, 2.982130e+01, 3.013911e+01, 3.046004e+01,
    3.078412e+01, 3.111137e+01, 3.144182e+01, 3.177551e+01, 3.211246e+01,
    3.245270e+01, 3.279625e+01, 3.314316e+01, 3.349344e+01, 3.384713e+01,
    3.420426e+01, 3.456486e+01, 3.492895e+01, 3.529658e+01, 3.566777e+01,
    3.604255e+01, 3.642096e+01, 3.680302e+01, 3.718877e+01, 3.757824e+01,
    3.797146e+01, 3.836847e+01, 3.876930e+01, 3.917398e+01, 3.958255e+01,
    3.999503e+01, 4.041148e+01, 4.083191e+01, 4.125636e+01, 4.168488e+01,
    4.211749e+01, 4.255422e+01, 4.299513e+01, 4.344023e+01, 4.388957e+01,
    4.434319e+01, 4.480112e+01, 4.526340e+01, 4.573006e+01, 4.620115e+01,
    4.667670e+01, 4.715675e+01, 4.764134e+01, 4.813050e+01, 4.862429e+01,
    4.912273e+01, 4.962587e+01, 5.013375e+01, 5.064640e+01, 5.116388e+01,
    5.168621e+01, 5.221345e+01, 5.274562e+01, 5.328278e+01, 5.382497e+01,
    5.437223e+01, 5.492461e+01, 5.548214e+01, 5.604486e+01, 5.661284e+01,
    5.718610e+01, 5.776470e+01, 5.834867e+01, 5.893807e+01, 5.953293e+01,
    6.013332e+01, 6.073926e+01, 6.135081e+01, 6.196802e+01, 6.259093e+01,
    6.321959e+01, 6.385406e+01, 6.449437e+01, 6.514057e+01, 6.579272e+01,
    6.645087e+01, 6.711506e+01, 6.778535e+01, 6.846178e+01, 6.914441e+01,
    6.983330e+01, 7.052848e+01, 7.123001e+01, 7.193795e+01, 7.265235e+01,
    7.337326e+01, 7.410074e+01, 7.483484e+01, 7.557561e+01, 7.632312e+01,
    7.707740e+01, 7.783853e+01, 7.860656e+01, 7.938154e+01, 8.016353e+01,
    8.095259e+01, 8.174878e+01, 8.255215e+01, 8.336276e+01, 8.418068e+01,
    8.500596e+01, 8.583866e+01, 8.667884e+01, 8.752657e+01, 8.838190e+01,
    8.924490e+01, 9.011563e+01, 9.099415e+01, 9.188052e+01, 9.277481e+01,
    9.367709e+01, 9.458741e+01, 9.550584e+01, 9.643245e+01, 9.736730e+01,
    9.831047e+01, 9.926200e+01, 1.002220e+02, 1.011905e+02, 1.021676e+02,
    1.031533e+02, 1.041477e+02, 1.051509e+02, 1.061630e+02, 1.071840e+02,
    1.082141e+02, 1.092531e+02, 1.103014e+02, 1.113588e+02, 1.124255e+02,
    1.135016e+02, 1.145872e+02, 1.156822e+02, 1.167869e+02, 1.179012e+02,
    1.190252e+02, 1.201591e+02, 1.213028e+02, 1.224566e+02, 1.236203e+02,
    1.247942e+02, 1.259784e+02, 1.271728e+02, 1.283776e+02, 1.295928e+02,
    1.308186e+02, 1.320550e+02, 1.333021e+02, 1.345599e+02, 1.358287e+02,
    1.371084e+02, 1.383991e+02, 1.397010e+02, 1.410140e+02, 1.423384e+02,
    1.436742e+02, 1.450214e+02, 1.463802e+02, 1.477507e+02, 1.491329e+02,
    1.505269e+02, 1.519328e+02, 1.533508e+02, 1.547809e+02, 1.562232e+02,
    1.576778e+02, 1.591448e+02, 1.606242e+02, 1.621163e+02, 1.636210e+02,
    1.651386e+02, 1.666689e+02, 1.682123e+02, 1.697688e+02, 1.713384e+02,
    1.729213e+02, 1.745175e+02, 1.761273e+02, 1.777506e+02, 1.793876e+02,
    1.810384e+02, 1.827031e+02, 1.843818e+02, 1.860746e+02, 1.877816e+02,
    1.895029e+02, 1.912387e+02, 1.929890e+02, 1.947539e+02, 1.965336e+02,
    1.983282e+02, 2.001377e+02, 2.019623e+02, 2.038022e+02, 2.056573e+02,
    2.075279e+02, 2.094141e+02, 2.113159e+02, 2.132335e+02, 2.151670e+02,
    2.171165e+02, 2.190822e+02, 2.210641e+02, 2.230624e+02, 2.250773e+02,
    2.271087e+02, 2.291569e+02, 2.312220e+02, 2.333040e+02, 2.354032e+02,
    2.375197e+02, 2.396535e+02, 2.418049e+02, 2.439739e+02, 2.461606e+02,
    2.483653e+02, 2.505880e+02, 2.528288e+02, 2.550880e+02, 2.573656e+02,
    2.596617e+02, 2.619766e+02, 2.643103e+02, 2.666630e+02, 2.690348e+02,
    2.714259e+02, 2.738364e+02, 2.762664e+02, 2.787161e+02, 2.811856e+02,
    2.836751e+02, 2.861847e+02, 2.887146e+02, 2.912649e+02, 2.938357e+02,
    2.964273e+02, 2.990397e+02, 3.016731e+02, 3.043277e+02, 3.070036e+02,
    3.097010e+02, 3.124200e+02, 3.151607e+02, 3.179235e+02, 3.207083e+02,
    3.235153e+02, 3.263448e+02, 3.291968e+02, 3.320716e+02, 3.349693e+02,
    3.378900e+02, 3.408340e+02, 3.438013e+02, 3.467922e+02, 3.498069e+02,
    3.528454e+02, 3.559080e+02, 3.589948e+02, 3.621061e+02, 3.652419e+02,
    3.684025e+02, 3.715881e+02, 3.747987e+02, 3.780346e+02, 3.812960e+02,
    3.845831e+02, 3.878959e+02, 3.912348e+02, 3.945999e+02, 3.979914e+02,
    4.014094e+02, 4.048541e+02, 4.083259e+02, 4.118247e+02, 4.153509e+02,
    4.189045e+02, 4.224859e+02, 4.260951e+02, 4.297325e+02, 4.333981e+02,
    4.370923e+02, 4.408151e+02, 4.445668e+02, 4.483475e+02, 4.521576e+02,
    4.559972e+02, 4.598664e+02, 4.637656e+02, 4.676948e+02, 4.716544e+02,
    4.756445e+02, 4.796653e+02, 4.837171e+02, 4.878000e+02, 4.919144e+02,
    4.960603e+02, 5.002380e+02, 5.044478e+02, 5.086898e+02, 5.129643e+02,
    5.172714e+02, 5.216115e+02, 5.259848e+02, 5.303914e+02, 5.348316e+02,
    5.393056e+02, 5.438137e+02, 5.483561e+02, 5.529330e+02, 5.575447e+02,
    5.621914e+02, 5.668733e+02, 5.715906e+02, 5.763437e+02, 5.811328e+02,
    5.859580e+02, 5.908197e+02, 5.957181e+02, 6.006535e+02, 6.056260e+02,
    6.106359e+02, 6.151470e+02, 6.196277e+02, 6.241373e+02, 6.286760e+02,
    6.332439e+02, 6.378411e+02, 6.424680e+02, 6.471245e+02, 6.518109e+02,
    6.565274e+02, 6.612741e+02, 6.660511e+02, 6.708587e+02, 6.756970e+02,
    6.805662e+02, 6.854665e+02, 6.903979e+02, 6.953608e+02, 7.003552e+02,
    7.053813e+02, 7.104394e+02, 7.155296e+02, 7.206520e+02, 7.258068e+02,
    7.309943e+02, 7.362145e+02, 7.414677e+02, 7.467541e+02, 7.520738e+02,
    7.574269e+02, 7.628138e+02, 7.682346e+02, 7.736894e+02, 7.791784e+02,
    7.847019e+02, 7.902599e+02, 7.958528e+02, 8.014806e+02, 8.071436e+02,
    8.128419e+02, 8.185758e+02, 8.243455e+02, 8.301510e+02, 8.359927e+02,
    8.418707e+02, 8.477852e+02, 8.537364e+02, 8.597245e+02, 8.657497e+02,
    8.718121e+02, 8.779121e+02, 8.840497e+02, 8.902252e+02, 8.964388e+02,
    9.026907e+02, 9.089811e+02, 9.153102e+02, 9.216781e+02, 9.280852e+02,
    9.345316e+02, 9.410175e+02, 9.475430e+02, 9.541086e+02, 9.607142e+02,
    9.673602e+02, 9.740468e+02, 9.807741e+02, 9.875425e+02, 9.943520e+02,
    1.001203e+03, 1.008095e+03, 1.015030e+03, 1.022006e+03, 1.029025e+03,
    1.036086e+03, 1.043190e+03, 1.050337e+03, 1.057527e+03, 1.064761e+03,
    1.072038e+03, 1.079358e+03, 1.086723e+03, 1.094133e+03, 1.101586e+03,
    1.109085e+03, 1.116628e+03, 1.124217e+03, 1.131851e+03, 1.139531e+03,
    1.147256e+03, 1.155028e+03, 1.162846e+03, 1.170711e+03, 1.178622e+03,
    1.186581e+03, 1.194587e+03, 1.202641e+03, 1.210742e+03, 1.218891e+03,
    1.227089e+03, 1.235335e+03, 1.243630e+03, 1.251974e+03, 1.260367e+03,
    1.268810e+03, 1.277302e+03, 1.285845e+03, 1.294438e+03, 1.303081e+03,
    1.311775e+03, 1.320520e+03, 1.329316e+03, 1.338164e+03, 1.347064e+03,
    1.356016e+03, 1.365020e+03, 1.374077e+03, 1.383186e+03, 1.392349e+03,
    1.401564e+03, 1.410834e+03, 1.420157e+03, 1.429535e+03, 1.438967e+03,
    1.448454e+03, 1.457995e+03, 1.467592e+03, 1.477245e+03, 1.486953e+03,
    1.496717e+03, 1.506538e+03, 1.516415e+03, 1.526349e+03, 1.536340e+03,
    1.546389e+03, 1.556495e+03, 1.566659e+03, 1.576882e+03, 1.587163e+03,
    1.597503e+03, 1.607902e+03, 1.618361e+03, 1.628879e+03, 1.639458e+03,
    1.650096e+03, 1.660796e+03, 1.671556e+03, 1.682377e+03, 1.693260e+03,
    1.704204e+03, 1.715211e+03, 1.726280e+03, 1.737411e+03, 1.748606e+03,
    1.759864e+03, 1.771185e+03, 1.782571e+03, 1.794020e+03, 1.805534e+03,
    1.817113e+03, 1.828757e+03, 1.840466e+03, 1.852241e+03, 1.864082e+03,
    1.875989e+03, 1.887963e+03, 1.900004e+03, 1.912113e+03, 1.924289e+03,
    1.936533e+03, 1.948845e+03, 1.961226e+03, 1.973675e+03, 1.986194e+03,
    1.998783e+03, 2.011441e+03, 2.024170e+03, 2.036969e+03, 2.049839e+03,
    2.062780e+03, 2.075793e+03, 2.088877e+03, 2.102034e+03, 2.115264e+03,
    2.128566e+03, 2.141941e+03, 2.155390e+03, 2.168913e+03, 2.182511e+03,
    2.196182e+03, 2.209929e+03, 2.223751e+03, 2.237649e+03, 2.251623e+03,
    2.265673e+03, 2.279799e+03, 2.294003e+03, 2.308284e+03, 2.322643e+03,
    2.337080e+03, 2.351596e+03, 2.366190e+03, 2.380864e+03, 2.395617e+03,
    2.410450e+03, 2.425363e+03, 2.440357e+03, 2.455432e+03, 2.470588e+03,
    2.485827e+03, 2.501147e+03, 2.516550e+03, 2.532035e+03, 2.547604e+03,
    2.563257e+03, 2.578994e+03, 2.594815e+03, 2.610720e+03, 2.626711e+03,
    2.642788e+03, 2.658950e+03, 2.675199e+03, 2.691534e+03, 2.707957e+03,
    2.724467e+03, 2.741065e+03, 2.757751e+03, 2.774526e+03, 2.791390e+03,
    2.808343e+03, 2.825386e+03, 2.842520e+03, 2.859744e+03, 2.877059e+03,
    2.894466e+03, 2.911965e+03, 2.929556e+03, 2.947239e+03, 2.965016e+03,
    2.982886e+03, 3.000851e+03, 3.018909e+03, 3.037062e+03, 3.055311e+03,
    3.073655e+03, 3.092095e+03, 3.110632e+03, 3.129265e+03, 3.147996e+03,
    3.166824e+03, 3.185751e+03, 3.204776e+03, 3.223901e+03, 3.243124e+03,
    3.262448e+03, 3.281872e+03, 3.301396e+03, 3.321022e+03, 3.340750e+03,
    3.360579e+03, 3.380511e+03, 3.400546e+03, 3.420685e+03, 3.440927e+03,
    3.461274e+03, 3.481725e+03, 3.502282e+03, 3.522944e+03, 3.543713e+03,
    3.564588e+03, 3.585570e+03, 3.606659e+03, 3.627857e+03, 3.649162e+03,
    3.670577e+03, 3.692101e+03, 3.713735e+03, 3.735480e+03, 3.757335e+03,
    3.779301e+03, 3.801379e+03, 3.823569e+03, 3.845872e+03, 3.868288e+03,
    3.890817e+03, 3.913461e+03, 3.936219e+03, 3.959092e+03, 3.982081e+03,
    4.005186e+03, 4.028407e+03, 4.051746e+03, 4.075202e+03, 4.098776e+03,
    4.122468e+03, 4.146280e+03, 4.170211e+03, 4.194262e+03, 4.218433e+03,
    4.242726e+03, 4.267140e+03, 4.291676e+03, 4.316335e+03, 4.341117e+03,
    4.366022e+03, 4.391051e+03, 4.416205e+03, 4.441484e+03, 4.466889e+03,
    4.492420e+03, 4.518077e+03, 4.543862e+03, 4.569774e+03, 4.595815e+03,
    4.621985e+03, 4.648284e+03, 4.674712e+03, 4.701271e+03, 4.727961e+03,
    4.754783e+03, 4.781736e+03, 4.808822e+03, 4.836041e+03, 4.863394e+03,
    4.890881e+03, 4.918502e+03, 4.946259e+03, 4.974152e+03, 5.002181e+03,
    5.030347e+03, 5.058650e+03, 5.087092e+03, 5.115672e+03, 5.144391e+03,
    5.173251e+03, 5.202250e+03, 5.231390e+03, 5.260672e+03, 5.290096e+03,
    5.319662e+03, 5.349371e+03, 5.379224e+03, 5.409222e+03, 5.439364e+03,
    5.469652e+03, 5.500086e+03, 5.530667e+03, 5.561395e+03, 5.592270e+03,
    5.623294e+03, 5.654467e+03, 5.685790e+03, 5.717263e+03, 5.748887e+03,
    5.780662e+03, 5.812589e+03, 5.844668e+03, 5.876901e+03, 5.909288e+03,
    5.941829e+03, 5.974525e+03, 6.007377e+03, 6.040385e+03, 6.073550e+03,
    6.106872e+03, 6.140353e+03, 6.173992e+03, 6.207791e+03, 6.241750e+03,
    6.275869e+03, 6.310149e+03, 6.344592e+03, 6.379197e+03, 6.413965e+03,
    6.448897e+03, 6.483993e+03, 6.519254e+03, 6.554682e+03, 6.590275e+03,
    6.626035e+03, 6.661964e+03, 6.698060e+03, 6.734325e+03, 6.770760e+03,
    6.807366e+03, 6.844142e+03, 6.881090e+03, 6.918210e+03, 6.955503e+03,
    6.992969e+03, 7.030610e+03, 7.068426e+03, 7.106417e+03, 7.144584e+03,
    7.182929e+03, 7.221451e+03, 7.260151e+03, 7.299031e+03, 7.338090e+03,
    7.377329e+03, 7.416750e+03, 7.456352e+03, 7.496137e+03, 7.536104e+03,
    7.576256e+03, 7.616592e+03, 7.657113e+03, 7.697821e+03, 7.738715e+03,
    7.779796e+03, 7.821065e+03, 7.862523e+03, 7.904170e+03, 7.946008e+03,
    7.988036e+03, 8.030256e+03, 8.072669e+03, 8.115274e+03, 8.158073e+03,
    8.201067e+03, 8.244256e+03, 8.287641e+03, 8.331223e+03, 8.375002e+03,
    8.418979e+03, 8.463155e+03, 8.507531e+03, 8.552107e+03, 8.596884e+03,
    8.641863e+03, 8.687045e+03, 8.732430e+03, 8.778020e+03, 8.823814e+03,
    8.869814e+03, 8.916020e+03, 8.962433e+03, 9.009055e+03, 9.055885e+03,
    9.102925e+03, 9.150174e+03, 9.197635e+03, 9.245308e+03, 9.293193e+03,
    9.341292e+03, 9.389604e+03, 9.438132e+03, 9.486875e+03, 9.535835e+03,
    9.585012e+03, 9.634407e+03, 9.684021e+03, 9.733855e+03, 9.783909e+03,
    9.834184e+03, 9.884682e+03, 9.935402e+03, 9.986346e+03, 1.003751e+04,
    1.008891e+04, 1.014053e+04, 1.019237e+04, 1.024445e+04, 1.029675e+04,
    1.034928e+04, 1.040205e+04, 1.045504e+04, 1.050827e+04, 1.056173e+04,
    1.061542e+04, 1.066934e+04, 1.072351e+04, 1.077790e+04, 1.083254e+04,
    1.088741e+04, 1.094252e+04, 1.099787e+04, 1.105346e+04, 1.110929e+04,
    1.116537e+04, 1.122168e+04, 1.127824e+04, 1.133505e+04, 1.139210e+04,
    1.144939e+04, 1.150694e+04, 1.156473e+04, 1.162277e+04, 1.168106e+04,
    1.173960e+04, 1.179840e+04, 1.185744e+04, 1.191674e+04, 1.197629e+04,
    1.203610e+04, 1.209617e+04, 1.215649e+04, 1.221706e+04, 1.227790e+04,
    1.233900e+04, 1.240036e+04, 1.246198e+04, 1.252386e+04, 1.258600e+04,
    1.264841e+04, 1.271109e+04, 1.277403e+04, 1.283723e+04, 1.290071e+04,
    1.296445e+04, 1.302846e+04, 1.309275e+04, 1.315730e+04, 1.322213e+04,
    1.328723e+04, 1.335261e+04, 1.341826e+04, 1.348419e+04, 1.355039e+04,
    1.361687e+04, 1.368364e+04, 1.375068e+04, 1.381800e+04, 1.388561e+04,
    1.395349e+04, 1.402167e+04, 1.409012e+04, 1.415887e+04, 1.422789e+04,
    1.429721e+04, 1.436682e+04, 1.443671e+04, 1.450690e+04, 1.457738e+04,
    1.464815e+04, 1.471921e+04, 1.479057e+04, 1.486223e+04, 1.493418e+04,
    1.500643e+04, 1.507898e+04, 1.515183e+04, 1.522497e+04, 1.529842e+04,
    1.537218e+04, 1.544623e+04, 1.552060e+04, 1.559526e+04, 1.567024e+04,
    1.574552e+04, 1.582111e+04, 1.589701e+04, 1.597322e+04, 1.604974e+04,
    1.612658e+04, 1.620373e+04, 1.628120e+04, 1.635898e+04, 1.643708e+04,
    1.651549e+04, 1.659423e+04, 1.667329e+04, 1.675266e+04, 1.683236e+04,
    1.691239e+04, 1.699273e+04, 1.707341e+04, 1.715441e+04, 1.723574e+04,
    1.731739e+04, 1.739938e+04, 1.748170e+04, 1.756435e+04, 1.764733e+04,
    1.773065e+04, 1.781430e+04, 1.789829e+04, 1.798262e+04, 1.806728e+04,
    1.815229e+04, 1.823763e+04, 1.832332e+04, 1.840935e+04, 1.849572e+04,
    1.858244e+04, 1.866951e+04, 1.875692e+04, 1.884469e+04, 1.893280e+04,
    1.902126e+04, 1.911008e+04, 1.919924e+04, 1.928877e+04, 1.937864e+04,
    1.946888e+04, 1.955947e+04, 1.965042e+04, 1.974173e+04, 1.983340e+04,
    1.992544e+04, 2.001783e+04, 2.011060e+04, 2.020372e+04, 2.029722e+04,
    2.039108e+04, 2.048531e+04, 2.057992e+04, 2.067489e+04, 2.077024e+04,
    2.086596e+04, 2.096205e+04, 2.105852e+04, 2.115537e+04, 2.125260e+04,
    2.135021e+04, 2.144820e+04, 2.154657e+04, 2.164533e+04, 2.174447e+04,
    2.184399e+04, 2.194391e+04, 2.204421e+04, 2.214490e+04, 2.224598e+04,
    2.234745e+04, 2.244932e+04, 2.255158e+04, 2.265424e+04, 2.275729e+04,
    2.286074e+04, 2.296459e+04, 2.306884e+04, 2.317350e+04, 2.327855e+04,
    2.338401e+04, 2.348988e+04, 2.359615e+04, 2.370283e+04, 2.380993e+04,
    2.391743e+04, 2.402534e+04, 2.413367e+04, 2.424241e+04, 2.435156e+04,
    2.446114e+04, 2.457113e+04, 2.468154e+04, 2.479237e+04, 2.490363e+04,
    2.501530e+04
], dtype=np.float32)
