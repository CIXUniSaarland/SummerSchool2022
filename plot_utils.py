import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def sample(pmf, n=1):
    return list(np.random.choice(list(pmf.keys()), p=list(pmf.values()), size=n))

def expectation(pmf, g=lambda x: x):
    return sum(g(outcome) * p for outcome, p in pmf.items())

def show_grid(pmf, ax = None):
    xs = np.array(list(pmf.keys()))
    cs = np.sqrt(np.array(list(pmf.values())))
    ys = np.ones_like(xs)
    if not ax:
        fig, ax = plt.subplots()
    ax.imshow(np.tile(cs[None, :], (8, 1)), cmap='magma', vmin=0, vmax=1,  interpolation='nearest')
    try:
        xrange = np.min(xs), np.max(xs)
        ax.imshow(np.tile(cs[None, :], (8, 1)), cmap='magma', vmin=0, vmax=1,  interpolation='nearest', 
                 extent=[xrange[0], xrange[1], 0, 1])
    except TypeError:
        ax.imshow(np.tile(cs[None, :], (8, 1)), cmap='magma', vmin=0, vmax=1,  interpolation='nearest')
        ax.set_xticks(np.arange(len(xs)))
        ax.set_xticklabels(xs)        
    ax.set_aspect(1/20.0)
    ax.set_yticks([])


def to_samples(products, n=150):
    return {product:sample(pmf, n) for product, pmf in products.items()}

def rotate_labels():
    ax = plt.gca()
    ax.set_xticklabels(ax.get_xticklabels(),rotation = 45)
    plt.tight_layout()
 

def show_products_mean(products):
    fig, ax = plt.subplots()    
    ax.scatter(np.arange(len(products)), [expectation(v) for v in products.values()])
    ax.set_xticks(np.arange(len(products)))
    ax.set_xticklabels(products.keys())
    ax.set_ylabel("q")
    ax.set_title("Plain means")
    rotate_labels()
    
def show_products_box(products):
    fig, ax = plt.subplots()
    samps = to_samples(products)
    ax.boxplot(samps.values(), labels=samps.keys())
    ax.set_title("Box plot")
    ax.set_ylabel("q")
    rotate_labels()

def show_products_violin(products):
    fig, ax = plt.subplots()
    samps = to_samples(products)
    sns.violinplot(data=list(samps.values()), scale="width")
    ax.set_xticklabels(samps.keys())    
    ax.set_ylabel("q")
    ax.set_title("Violin plot")
    rotate_labels()

def show_products_swarm(products):
    fig, ax = plt.subplots()
    samps = to_samples(products)
    data = np.array(list(samps.values())) 
    data += np.random.normal(0,0.05,data.shape)
    
    sns.swarmplot(data=list(data), size=2)
    ax.set_xticklabels(samps.keys())    
    ax.set_ylabel("q")    
    ax.set_title("Swarm plot")
    rotate_labels()
    

def show_products_strip(products):
    fig, ax = plt.subplots()
    x = 0
    ax.set_xlim(-0.1,len(products)/5)
    ax.set_ylim(0,1)
    for product, pmf in products.items():
        xs = np.array(list(pmf.keys()))
        cs = np.sqrt(np.array(list(pmf.values())))
        ax.imshow(np.tile(cs[None, :], (8, 1)).T, cmap='magma', vmin=0, vmax=1, 
                   extent=[x, x+0.1, 0, 1], origin='lower')  
        ax.text(x, -0.3, product, rotation=45, ha='center')        
        x += 0.2
        
        rotate_labels()
    ax.set_title("Gradient plot")
    ax.set_ylabel("q") 
    
def show_products_table(products):
    rows = []
    sampled = to_samples(products)
    for food, samples in sampled.items():        
        row = [food, np.percentile(samples, 0.25), np.percentile(samples, 0.5), np.percentile(samples, 0.75)]
        rows.append(row)
    return pd.DataFrame(rows, columns=["name", "Q1", "Median", "Q3"])