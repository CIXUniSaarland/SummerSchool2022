import scipy.stats
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

cmap = plt.get_cmap("viridis")

def plot_gp_samples(ax, xs, ys, **kwargs):        
    ax.plot(xs, ys.squeeze(), **kwargs)
    ax.set_xlabel("Font size")
    ax.set_ylabel("Reading speed (seconds per word)")

def render_gp(ax, xs, gp):

    norm = scipy.stats.norm(0, 1)
    if len(xs.shape)==1:
        xs = xs[:, None]
    y_pred, y_std = gp.predict(xs, return_std=True)
    
    y_pred = y_pred.squeeze()

    ax.plot(xs, y_pred, c="k")
    for contour in np.linspace(0, 0.5, 50):
        k1 = norm.ppf(contour)
        k2 = norm.ppf(1 - contour)

        upper = y_pred + y_std * k1 * 2
        lower = y_pred + y_std * k2 * 2
        ax.fill_between(xs[:,0], upper, lower, color=cmap(norm.pdf(k1)))
    
    ys  = gp.sample_y(xs, 20)
    plot_gp_samples(ax, xs[:,0], ys, c='w', alpha=0.1)


def pi(y_pred, y_std):
    
    y_pred = y_pred.squeeze()
    best = max(y_pred)
    # calculate the probability of improvement
    return scipy.stats.norm(0, 1).cdf((y_pred - best) / (y_std + 1e-7))


def ei(y_pred, y_std, xi=0):
    y_pred = y_pred.squeeze()
    norm = scipy.stats.norm(0, 1)    
    best = max(y_pred)
    Z = (y_pred - best - xi) / (y_std + 1e-9)
    # calculate the expected improvement
    return norm.cdf(Z) * (y_pred - best - xi) + y_std * norm.pdf(Z)


def ei(mu, std, xi=0):
    mu = mu.squeeze()
    std = std.squeeze()
    values = np.zeros_like(mu)
    mask = std > 0
    y_opt = max(mu)
    improve = y_opt - xi - mu[mask]
    scaled = improve / std[mask]
    cdf = scipy.stats.norm.cdf(scaled)
    pdf = scipy.stats.norm.pdf(scaled)
    exploit = improve * cdf
    explore = std[mask] * pdf
    values[mask] = exploit + explore
    return -values

def lcb(y_pred, y_std, kappa=1):
    return y_pred.squeeze() - kappa * y_std.squeeze() + np.random.normal(0, 1e-6, y_pred.shape[0])

def ucb(y_pred, y_std, kappa=1):
    return y_pred.squeeze() + kappa * y_std.squeeze() + np.random.normal(0, 1e-6, y_pred.shape[0])

from skopt.learning.gaussian_process import GaussianProcessRegressor
from skopt.learning.gaussian_process.kernels import (
    RBF,
    ConstantKernel,
    WhiteKernel,
    Matern,
)


