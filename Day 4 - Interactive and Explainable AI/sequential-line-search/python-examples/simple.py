import pySequentialLineSearch
import numpy as np
import sys
from typing import Optional, Tuple


# A dummy function for testing
def calc_simulated_objective_func(x):
    return -np.linalg.norm(x - 0.2)


# A dummy implementation of slider manipulation
def ask_human_for_slider_manipulation(slider_ends):
    t_max = 0.0
    f_max = -sys.float_info.max

    for i in range(1000):
        t = float(i) / 999.0
        x = (1.0 - t) * slider_ends[0] + t * slider_ends[1]
        f = calc_simulated_objective_func(x)

        if f_max is None or f_max < f:
            f_max = f
            t_max = t

    return t_max


# A typical implementation of sequential line search procedure
def main():
    optimizer = pySequentialLineSearch.SequentialLineSearchOptimizer(
        num_dims=120)

    optimizer.set_hyperparams(kernel_signal_var=0.50,
                              kernel_length_scale=0.10,
                              kernel_hyperparams_prior_var=0.10)
    # Gaussian process with Mat??rn kernel as surrogate model
    # m52 = ConstantKernel(1.0) * Matern(length_scale=0.5, nu=2.5)
    # gpr = GaussianProcessRegressor(kernel=m52, alpha=noise**2)

    # Initialize plane P_1
    v = np.random.randn(120)
    v /= np.linalg.norm(v)
    u = np.random.randn(120)
    u -= u.dot(v) * v
    u /= np.linalg.norm(u)

    c = np.zeros(120)

    def sampling_from_plane(c, u, v, itr=0):
        '''
        Return the 25 sampling points from the given plane, paremeterized by (c,u,v).
        
        Args:
            c: center point of the plane. Shape: 120
            u: vector u. Shape: 120
            v: vector v, which is orthogonal to u. Shape: 120

        Returns:
            sampling_points: shape: (25, 120). Each row is a sampling point
        '''
        base = 20
        vec_len = base / (1.5 ** itr)
        u = vec_len * u / np.linalg.norm(u)
        v = vec_len * v / np.linalg.norm(v)
        c = c.reshape(-1)
        u = u.reshape(-1)
        v = v.reshape(-1)
        row_step = (v - u) / 4
        col_step = (-1 * v - u) / 4
        start_point = c - 2 * row_step - 2 * col_step
        sampling_points = np.zeros((25, 120))
        for i in range(5):
            for j in range(5):
                sampling_points[i * 5 + j] = start_point + row_step * i + col_step * j
        return sampling_points
        
    sampling_points = sampling_from_plane(c, u, v, 0)  
    print("gallery: 0")
    # create_gallery(sampling_points)

    # User picks one 
    print("pick one image (type a number between 0 to 24):")
    pick_idx = 5
    print("picked idx: ", pick_idx)
    c = sampling_points[pick_idx].reshape(-1, 1)
    remove_x_preferable = np.delete(sampling_points, pick_idx, 0)
    xs_other = [remove_x_preferable[i].reshape(-1, 1) for i in range(remove_x_preferable.shape[0])]
    print("c", c)
    print("xs_other", xs_other[0])
    n_iter = 3

    for i in range(n_iter):
        print("gallery: ", i+1)
        # Update Gaussian process with existing samples
    #     gpr.fit(X_observed, Y_observed)
        optimizer.submit_line_search_result(c, xs_other)
    #     gpr = compute_MAP_estimate(X_sample, gpr, m52)
        
        # Obtain next sampling point from the acquisition function (expected_improvement)
if __name__ == '__main__':
    main()
