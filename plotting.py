import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
import numpy as np
from typing import Literal
from const import P, COLUMN_MAP
from utils import fetch_lookup_df

#===============================================================
# Plot the equilibrium variable value in both solids and fluids 
# on a T vs C02 mass frac. grid
#===============================================================
def plot_T_vs_wCO2sys(
        dataset: Literal['general', 'solver'],
        PTtype: Literal['highPT', 'lowPT'],
        key: str,
        savefig: bool = False
        ) -> None:

    #DATA FETCH-----------------------------------------
    df = fetch_lookup_df(dataset, PTtype)

    #create a pivot table
    # T == index, wCO2 == columns -> only unique (T, wCO2) points
    df = df.pivot(index='T', columns='wCO2', values=key) 

    #PLOTTING--------------------------------------------
    extent = (
        df.columns.min(),
        df.columns.max(),
        df.index.min(),
        df.index.max()
    )

    fig, ax = plt.subplots()
    im = ax.imshow(df, extent=extent, origin='lower', aspect='auto')
    fig.colorbar(im, ax=ax, label=COLUMN_MAP[key])
    
    ax.set_title(f'P={P[PTtype]} (GPa)')
    ax.set_ylabel('T (°K)')
    ax.set_xlabel(r'CO₂ mass frac.')
    

    if savefig: fig.savefig(f'{key}_sys_{dataset}_{PTtype}')

    plt.show() 

#==============================================================
# Plot the equilibrium value in only solids with interpolaiton
# on a T vs C02 mass frac. grid
#==============================================================
def plot_T_vs_wCO2solids(
        dataset: Literal['general', 'solver'],
        PTtype: Literal['highPT', 'lowPT'],
        key: str,
        N_inter_pts: int = 100,
        savefig: bool = False
        ) -> None:

    #DATA FETCH-----------------------------------------
    df = fetch_lookup_df(dataset, PTtype)

    #DATA INTERPOLATION-----------------------------------
    #unified grid used to interpolate the new values
    interp_grid = np.linspace(0, df['wCO2_s'].max(), N_inter_pts)
    
    #Sort the temps. in descending order
    T_array = np.sort(df['T'].unique()[::-1])

    #allocate array with T on y and var on x
    data = np.ndarray(shape=(len(T_array), N_inter_pts)) 

    #interpolate for each T point
    for idx, T in enumerate(T_array):
        df_slice = df[df['T'] == T]
        interpolator = interp1d(
            df_slice['wCO2_s'], 
            df_slice[key], 
            kind='nearest', 
            fill_value='extrapolate'
            )
        weights = interpolator(interp_grid) 
        data[idx] = weights

    #PLOTTING---------------------------------------------
    extent = (
        interp_grid.min(),
        interp_grid.max(),
        T_array.min(),
        T_array.max()
    )

    fig, ax = plt.subplots()
    im = ax.imshow(data, extent=extent, origin='lower', aspect='auto')
    fig.colorbar(im, ax=ax, label=COLUMN_MAP[key])
    
    ax.set_title(f'P={P[PTtype]} (GPa)')
    ax.set_ylabel('T (°K)')
    ax.set_xlabel(r'CO₂ mass frac. in solids')
    

    if savefig: fig.savefig(f'{key}_sys_{dataset}_{PTtype}')

    plt.show() 