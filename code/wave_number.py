import numpy as np

def _newtRaph(T, h):

    # Function to determine k from dispersion relation given period (T) and depth (h) using
    # the Newton-Raphson method.

    if not np.isnan(T):
        L_not = (9.81 * (T ** 2)) / (2 * np.pi)
        k1 = (2 * np.pi) / L_not

        def fk(k):
            return (((2 * np.pi) / T) ** 2) - (9.81 * k * np.tanh(k * h))

        def f_prime_k(k):
            return (-9.81 * np.tanh(k * h)) - (
                9.81 * k * (1 - (np.tanh(k * h) ** 2))
            )

        k2 = 100
        i = 0
        while abs((k2 - k1)) / k1 > 0.01:
            i += 1
            if i != 1:
                k1 = k2
            k2 = k1 - (fk(k1) / f_prime_k(k1))
    else:
        k2 = np.nan  # pragma: no cover

    return k2

k=[]
for T in period:
    k.append(_newtRaph(T, h))


#radial frequency at depth h
sigma = (2 * np.pi) / period

#celerity at depth h
c1 = sigma / np.array(k)

#group speed at depth h
n = (0.5 + (np.array(k) * h)/np.sinh(2 *np.array(k)*h))
cg1 = c1 * n
