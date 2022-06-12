
import pandas as pd 
import numpy as np
import scipy.stats as ss
import matplotlib as mpl
import matplotlib.pyplot as plt
import pymc3
import arviz as az

# utility to collect all samples together
def pymc3_sample(n=1000, observed=None):
    # get the posterior
    trace = pymc3.sample(n, cores=1, return_inferencedata=False)
    # get the prior and prior predictive
    prior_pc = pymc3.sample_prior_predictive(n)
    # get the posterior predictive
    ppc = pymc3.sample_posterior_predictive(trace)
    return {"posterior":trace, "prior":prior_pc, "posterior_predictive":ppc, "observed":observed}




def trace_hist(ax, trace, name, c='C1'):
        """Draw a histogram of 'trace' on the given axis 'ax',
        and label it 'name'."""
        n, bins, patches = ax.hist(np.array(trace).ravel(), density=True, bins=30, color=c)                
        max_n = np.max(n)
        upper, lower = np.percentile(trace, 5.0), np.percentile(trace, 95.0)
        ci_text = f'[{upper:.2f} - {lower:.2f}]'
        ax.set_title("{var_name}\n{ci_text}".format(var_name=name, ci_text=ci_text))
        
        # draw simple statistics
        ctr_max = 0.5 * (bins[np.argmax(n)] + bins[np.argmax(n)+1])
        #ax.axvline(np.mean(trace),  color='C1', label='Expected')
        # 90% credible interval
        
        ax.fill_between(x=[upper, lower], y1=max_n,
                          color='C1', alpha=0.2, label='90% credible')
        ax.text(np.mean(trace), 0.5*max_n, f'[{upper:.2f} - {lower:.2f}]', ha='center', c='k')