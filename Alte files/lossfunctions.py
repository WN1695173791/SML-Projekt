import tensorflow as tf
import math as m
from keras import backend as K


def Trivial_Loss(encoder, decoder, frames):
    x = encoder.inp
    _, x_rec = decoder(encoder(x)[-1])
    return K.mean(tf.keras.losses.binary_crossentropy(x, x_rec))


def Bernoulli_ODE_Loss(encoder, decoder, frames):
    x = encoder.inp
    Ls_mu, Ls_logsig, Lv_mu, Lv_logsig, sLsg = encoder(x)
    _, x_rec = decoder(sLsg)
    return 1


def Bernoulli_Loss(encoder, decoder, frames):
    x = encoder.inp
    μ, log_σ, z = encoder(x)
    _, x_rec = decoder(z)
    log_p_xz = 784. * frames * \
        K.mean(tf.keras.losses.binary_crossentropy(x, x_rec))
    kl_div = .5 * K.sum(1. + 2. * log_σ - K.square(μ) - 2. * K.exp(log_σ), axis=-1)
    return (log_p_xz - kl_div)


def Gauss_Loss(encoder, decoder, frames):
    x = tf.keras.layers.Flatten()(encoder.inp)
    μ, log_σ, z = encoder(encoder.inp)
    _, mu, log_sig = decoder(z)
    log_p_xz = -.5 * K.sum(K.log(2. * tf.constant(m.pi)) + 2. * log_sig +
                           (K.square(mu - x))/(K.exp(2. * log_sig)), axis=-1)
    kl_div = .5 * K.sum(1. + 2. * log_σ - K.square(μ) - 2. * K.exp(log_σ), axis=-1)
    return (-log_p_xz - kl_div)


#tf.keras.backend.reshape(x, (784,))
# To Do:
# https://keras.io/guides/training_with_built_in_methods/ Erklärung wie man die
# Lossfunktion in eine Klasse umschreiben kann, falls wir das mal brauchen sollten.
# Das Problem ist nämlich, dass  Lossfunktionen eigentlich nur zwei Argumente haben
# sollen (Input, Output). Wir brauchen aber vier Argumente (Input, Output, μ, log_σ).

# Unterkapitel: Handling losses and metrics that don't fit the standard signature.
