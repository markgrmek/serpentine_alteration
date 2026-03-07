import matplotlib.pyplot as plt
import matplotlib.animation as ani
from scipy.interpolate import interp1d
import numpy as np
from typing import Literal
from const import P, COLUMN_MAP, DCO2_B, SEC_PER_YEAR, POR_B, WCO2_B, WCO2_SOAP, MINERAL_MAP
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
    

    if savefig: fig.savefig(f'figs\{key}_sys_{dataset}_{PTtype}')

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
    

    if savefig: fig.savefig(f'figs\{key}_sys_{dataset}_{PTtype}')

    plt.show() 

#==============================================================
# ANIMATION PLOTTING
#==============================================================

#PLOT DENSITY------------------------------------------------
def animate_rho_s(
        PTtype: Literal['highPT', 'lowPT'],
        plot_step: int = 1,
        save_animation: bool = True,
        plt_show_pause: float = 0.01):

    #Data fetch-----------------------------------------
    data = np.load(rf"outputs\simulation_{PTtype}.npz")
    df = fetch_lookup_df("general", PTtype)
    fac = df["rho_s"].max()

    x_array = data["grid"][:-1]
    t_array = data["time"][::plot_step]
    y_array = data["rho_s"][:,::plot_step]*fac

    #Plotting-----------------------------------------
    fig, ax = plt.subplots(figsize=(8, 4))

    ax.set_xlabel(r'x $[m]$')
    ax.set_ylabel(r'$\rho_{solids}$ $\left[\frac{kg}{m^3}\right]$')

    line = ax.plot(x_array, y_array[0], color='blue')[0]

    def update(frame):
        ax.set_title(rf'time: {t_array[frame]/(DCO2_B*SEC_PER_YEAR):.1g} $[y]$', fontsize=10)
        line.set_ydata(y_array[frame])
        return line

    # Create the animation
    animation = ani.FuncAnimation(
        fig, 
        update, 
        frames=y_array.shape[0], 
        interval=1)

    if save_animation:
        writer = ani.PillowWriter(fps=20, bitrate=10)
        animation.save(
            f'figs\density_animation_{PTtype}.gif', 
            writer=writer, 
            progress_callback = lambda i, n: print(f'Saving frame {i}/{n}')
            )

    # Display the animation
    plt.pause(plt_show_pause)
    plt.show()

#PLOT POROSITY------------------------------------------------
def animate_por(
        PTtype: Literal['highPT', 'lowPT'],
        plot_step: int = 1,
        save_animation: bool = True,
        plt_show_pause: float = 0.01):
    
    #Data fetch-----------------------------------------
    data = np.load(rf"outputs\simulation_{PTtype}.npz")

    x_array = data["grid"][:-1]
    t_array = data["time"][::plot_step]
    y_array = data["por"][:,::plot_step]

    #Plotting-----------------------------------------
    fig, ax = plt.subplots(figsize=(8, 4))

    ax.set_xlabel(r'x $[m]$')
    ax.set_ylabel(r'$\phi$ $\left[\frac{m^3}{m^3}\right]$')

    line = ax.plot(x_array, np.ones_like(x_array, dtype=float)*POR_B, color='blue')[0]

    def update(frame):
        ax.set_title(rf'time: {t_array[frame]/(DCO2_B*SEC_PER_YEAR):.1g} $[y]$', fontsize=10)
        line.set_ydata(y_array[frame])
        return line

    # Create the animation
    animation = ani.FuncAnimation(
        fig, 
        update, 
        frames=t_array.shape[0], 
        interval=1)

    if save_animation:
        writer = ani.PillowWriter(fps=20, bitrate=10)
        animation.save(
            f'figs\porosity_animation_{PTtype}.gif', 
            writer=writer, 
            progress_callback = lambda i, n: print(f'Saving frame {i}/{n}')
            )

    # Display the animation
    plt.pause(plt_show_pause)
    plt.show()

#WEIGHT FRACTIONS---------------------------------------------------------------------
def animate_weight_fracs(
        PTtype: Literal['highPT', 'lowPT'],
        plot_step: int = 1,
        save_animation: bool = True,
        plt_show_pause: float = 0.01):
    
    #Data fetch-----------------------------------------
    data = np.load(rf"outputs\simulation_{PTtype}.npz")

    x_array = data["grid"][:-1]
    t_array = data["time"][::plot_step]
    wCO2s = data['wCO2_s'][:,::plot_step]
    wCO2fl = data['wCO2_fl'][:,::plot_step]
    wSiO2s = data['wSiO2_s'][:,::plot_step]
    wH2Os = data['wH2O_s'][:,::plot_step]

    #Plotting-----------------------------------------
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.subplots_adjust(right=0.75)

    ax.set_xlabel(r'x $[m]$')
    ax.set_ylabel(r'Weight frac. $\left[\frac{kg}{kg}\right]$')

    ax.plot(x_array, np.ones_like(x_array)*WCO2_SOAP, label=f'{r'$CO_2$'} (LBC: {WCO2_SOAP:.1g})', color='orange', linestyle=':')
    ax.plot(x_array, np.ones_like(x_array)*WCO2_B, label=f'{r'$CO_2$'} (IC: {WCO2_B:.1g})', color='green', linestyle=':')

    line1 = ax.plot(x_array, wCO2s[0], label=r'$CO_2$ (s)', color='orange')[0]
    line2 = ax.plot(x_array, wCO2fl[0], label=r'$CO_2$ (fl)', color='cyan')[0]
    line3 = ax.plot(x_array, wSiO2s[0], label=r'$SiO_2$ (s)', color='chocolate')[0]
    line4 = ax.plot(x_array, wH2Os[0], label=r'$H_2O$  (s)', color='steelblue')[0]

    def update(frame):
        ax.set_title(rf'time: {t_array[frame]/(DCO2_B*SEC_PER_YEAR):.1g} $[y]$', fontsize=10)
        line1.set_ydata(wCO2s[frame])
        line2.set_ydata(wCO2fl[frame])
        line3.set_ydata(wSiO2s[frame])
        line4.set_ydata(wH2Os[frame])
        return line1, line2, line3, line4

    # Create the animation
    animation = ani.FuncAnimation(
        fig, 
        update, 
        frames=t_array.shape[0], 
        interval=1)
    
    ax.legend(bbox_to_anchor=(1.4, 0.5), loc='center right', frameon=False)

    if save_animation:
        writer = ani.PillowWriter(fps=20, bitrate=10)
        animation.save(
            f'figs\weight_frac_animation_{PTtype}.gif', 
            writer=writer, 
            savefig_kwargs={"bbox_inches": "tight"},
            progress_callback = lambda i, n: print(f'Saving frame {i}/{n}')
            )

    # Display the animation
    plt.pause(plt_show_pause)
    plt.show()

#VOL FRACS---------------------------------------------------------------------------
def animate_mineral_vol_fracs(
        PTtype: Literal['highPT', 'lowPT'],
        plot_step: int = 1,
        save_animation: bool = True,
        plt_show_pause: float = 0.01):
    
    #Data fetch-----------------------------------------
    data = np.load(rf"outputs\simulation_{PTtype}.npz")

    x_array = data["grid"][:-1]
    t_array = data["time"][::plot_step]
    zero_line = np.zeros_like(x_array)

    plot_data = {}
    for key in MINERAL_MAP.keys():
        if key in data.keys():
            plot_data[MINERAL_MAP[key]] = data[key][:,::plot_step]

    #Plotting-----------------------------------------
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.subplots_adjust(right=0.75)

    ax.set_xlabel(r'x $[m]$')
    ax.set_ylabel(r'Vol frac. $\left[\frac{m^3}{m^3}\right]$')

    lines = []
    prev_y_array = zero_line
    for mineral in plot_data.keys():
        y_array = plot_data[mineral][0]
        lines.append(ax.fill_between(x_array, prev_y_array, y_array, label=mineral))
        prev_y_array = y_array

    def update(frame):
        ax.set_title(rf'time: {t_array[frame]/(DCO2_B*SEC_PER_YEAR):.1g} $[y]$', fontsize=10)
        lines = []
        prev_y_array = zero_line
        for mineral in plot_data.keys():
            y_array = plot_data[mineral][frame]
            lines.append(ax.fill_between(x_array, prev_y_array, y_array, label=mineral))
            prev_y_array = y_array
        
        return lines

    # Create the animation
    animation = ani.FuncAnimation(
        fig, 
        update, 
        frames=t_array.shape[0], 
        interval=1)
    
    ax.legend(bbox_to_anchor=(1.4, 0.5), loc='center right', frameon=False)

    if save_animation:
        writer = ani.PillowWriter(fps=20, bitrate=10)
        animation.save(
            f'figs\mineral_animation_{PTtype}.gif', 
            writer=writer, 
            savefig_kwargs={"bbox_inches": "tight"},
            progress_callback = lambda i, n: print(f'Saving frame {i}/{n}')
            )

    # Display the animation
    plt.pause(plt_show_pause)
    plt.show()