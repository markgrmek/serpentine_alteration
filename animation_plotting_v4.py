import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pandas import read_csv
from lookup_table import general_lookup

DATASET = 'lowPT'
DCO2_B: float = 1.88e-6

def plot_density(save_animation: bool = False, plot_every = 20):
    #time
    time = read_csv(f'time_{DATASET}.csv')
    time = time.to_numpy().reshape(-1)

    #Y values
    factor = general_lookup['rho_s'].max()
    ws1 = read_csv(f'density_{DATASET}.csv')
    ws1 = ws1.to_numpy().T
    ws1 = ws1*factor


    if plot_every: 
        ws1 = ws1[:,::plot_every]
        time = time[::plot_every]

    N_frames = ws1.shape[1]

    #X values
    grid = read_csv(f'grid_{DATASET}.csv',header=None)
    grid = grid.to_numpy().reshape(-1)[:-1]
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.subplots_adjust(left=0.1, right=0.7, top=0.85, bottom=0.1)
    fig.suptitle('Evolution of density in time')

    ax.set_xlabel('x')
    ax.set_ylabel('Density')

    ax.set_xlim(min(grid), max(grid))
    ax.set_ylim(ws1.min()-0.01, ws1.max()+0.01)

    #Plot lines
    text = ax.text(0.8, 0.8, 'Time', transform=ax.transAxes, fontsize=12, color='black', ha='center')

    line1, = ax.plot(grid, ws1[:, 0], label=r'$\rho_{solids}$', color='orange')

    #Plot lines
    def update(frame):
        text.set_text(f'time {(time[frame]/DCO2_B/(365*24*60*60)):.1f} y')
        line1.set_ydata(ws1[:, frame])
        return line1, text

    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, frames=N_frames, interval=1, blit=not save_animation
    )

    ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

    if save_animation:
        writer = animation.PillowWriter(fps=20, bitrate=10)
        ani.save(f'density_animation_{DATASET}.gif', writer=writer, progress_callback = lambda i, n: print(f'Saving frame {i}/{n}'))

    # Display the animation
    plt.pause(0.01)
    plt.show()
    plt.legend()

def plot_porosity(save_animation: bool = False, plot_every = 20):
    #time
    time = read_csv(f'time_{DATASET}.csv')
    time = time.to_numpy().reshape(-1)

    #Y values
    ws1 = read_csv(f'por_{DATASET}.csv')
    ws1 = ws1.to_numpy().T

    init_por_val = 0.2
    init_por = [init_por_val]*100

    if plot_every: 
        ws1 = ws1[:,::plot_every]
        time = time[::plot_every]

    N_frames = ws1.shape[1]

    #X values
    grid = read_csv(f'grid_{DATASET}.csv',header=None)
    grid = grid.to_numpy().reshape(-1)[:-1]

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.subplots_adjust(left=0.1, right=0.7, top=0.85, bottom=0.1)
    fig.suptitle('Evolution of porosity in time')

    ax.set_xlabel('x')
    ax.set_ylabel('Porosity')

    ax.set_xlim(min(grid), max(grid))
    ax.set_ylim(ws1.min()-0.01, ws1.max()+0.01)

    #Plot lines
    text = ax.text(0.8, 0.8, 'Time', transform=ax.transAxes, fontsize=12, color='black', ha='center')

    init_por, = ax.plot(grid, init_por, label=f'{r'$\phi$'} IC ({init_por_val})', color='orange', linestyle=':')
    line1, = ax.plot(grid, ws1[:, 0], label=r'$\phi$', color='orange') 

    def update(frame):
        line1.set_ydata(ws1[:, frame])
        text.set_text(f'time {(time[frame]/DCO2_B/(365*24*60*60)):.1f} y')
        return text, line1

    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, frames=N_frames, interval=1, blit=not save_animation
    )

    ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

    if save_animation:
        writer = animation.PillowWriter(fps=20, bitrate=10)
        ani.save(f'por_animation_{DATASET}.gif', writer=writer, progress_callback = lambda i, n: print(f'Saving frame {i}/{n}'))

    # Display the animation
    plt.pause(0.01)
    plt.show()
    plt.legend()

def plot_weight_fracs(save_animation: bool = False, plot_every = 20):
    #time
    time = read_csv(f'time_{DATASET}.csv')
    time = time.to_numpy().reshape(-1)

    #Y values
    ws1 = read_csv(f'wCO2_s_{DATASET}.csv')
    ws1 = ws1.to_numpy().T
    
    ws2 = read_csv(f'wCO2_fl_{DATASET}.csv')
    ws2 = ws2.to_numpy().T

    ws3 = read_csv(f'wSiO2_s_{DATASET}.csv')
    ws3 = ws3.to_numpy().T

    ws4 = read_csv(f'wH2O_s_{DATASET}.csv')
    ws4 = ws4.to_numpy().T

    if plot_every: 
        ws1 = ws1[:,::plot_every]
        ws2 = ws2[:,::plot_every]
        ws3 = ws3[:,::plot_every]
        ws4 = ws4[:,::plot_every]
        time = time[::plot_every]

    N_frames = ws1.shape[1]

    soap_lvl = 0.022
    serp_lvl = 0.0022

    #X values
    grid = read_csv(f'grid_{DATASET}.csv',header=None)
    grid = grid.to_numpy().reshape(-1)[:-1]

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.subplots_adjust(left=0.1, right=0.7, top=0.85, bottom=0.1)
    fig.suptitle('Evolution of weight fractions of species in time')

    ax.set_xlabel('x')
    ax.set_ylabel(r'weight fraction')

    ax.set_xlim(min(grid), max(grid))
    ax.set_ylim(0, 0.03)  # Adjust y-axis limits based on your data

    #Plot lines
    text = ax.text(0.8, 0.8, 'Time', transform=ax.transAxes, fontsize=12, color='black', ha='center')

    soap, = ax.plot(grid, np.ones(len(grid))*soap_lvl, label=f'{r'$CO_2$'} LBC ({soap_lvl})', color='orange', linestyle=':')
    serp, = ax.plot(grid, np.ones(len(grid))*serp_lvl, label=f'{r'$CO_2$'} IC ({serp_lvl})', color='green', linestyle=':')  

    line1, = ax.plot(grid, ws1[:, 0], label=r'$CO_2$ solids', color='orange')
    line2, = ax.plot(grid, ws2[:, 0], label=r'$CO_2$ fluids', color='cyan', linestyle='--')
    line3, = ax.plot(grid, ws1[:, 0], label=r'$SiO_2$ solids', color='chocolate', linestyle='--')
    line4, = ax.plot(grid, ws2[:, 0], label=r'$H_2O$  solids', color='steelblue', linestyle='--')

    def update(frame):
        line1.set_ydata(ws1[:, frame])
        line2.set_ydata(ws2[:, frame])
        line3.set_ydata(ws3[:, frame])
        line4.set_ydata(ws4[:, frame])
        text.set_text(f'time {(time[frame]/DCO2_B/(365*24*60*60)):.1f} y')
        return text, line1, line2, line3, line4

    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, frames=N_frames, interval=1, blit= not save_animation
    )

    ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

    if save_animation: 
        writer = animation.PillowWriter(fps=20, bitrate=10)
        ani.save(f'weight_frac_animation_{DATASET}.gif', writer=writer, progress_callback = lambda i, n: print(f'Saving frame {i}/{n}'))

    # Display the animation
    plt.pause(0.01)
    plt.show()
    plt.legend()

def plot_mineral_vols_lowPT(save_animation: bool = False, plot_every = 20):
    #Y values
    ws1 = read_csv(f'dolomite_{DATASET}.csv')
    ws1 = ws1.to_numpy().T
    ws2 = read_csv(f'antigorite_{DATASET}.csv')
    ws2 = ws2.to_numpy().T + ws1
    ws3 = read_csv(f'talc_{DATASET}.csv')
    ws3 = ws3.to_numpy().T + ws2
    ws4 = read_csv(f'magnesite_{DATASET}.csv')
    ws4 = ws4.to_numpy().T + ws3
    ws5 = read_csv(f'chlorite_{DATASET}.csv')
    ws5 = ws5.to_numpy().T + ws4
    ws6 = read_csv(f'quartz_{DATASET}.csv')
    ws6 = ws6.to_numpy().T + ws5
    ws7 = read_csv(f'magnetite_{DATASET}.csv')
    ws7 = ws7.to_numpy().T + ws6
    ws8 = read_csv(f'hematite_{DATASET}.csv')
    ws8 = ws8.to_numpy().T + ws7
    ws9 = read_csv(f'lime_{DATASET}.csv')
    ws9 = ws9.to_numpy().T + ws8
    ws10 = read_csv(f'calcite_{DATASET}.csv')
    ws10 = ws10.to_numpy().T + ws9


    if plot_every:
        ws1 = ws1[:,::plot_every]
        ws2 = ws2[:,::plot_every]
        ws3 = ws3[:,::plot_every]
        ws4 = ws4[:,::plot_every]
        ws5 = ws5[:,::plot_every]
        ws6 = ws6[:,::plot_every]
        ws7 = ws7[:,::plot_every]
        ws8 = ws8[:,::plot_every]
        ws9 = ws9[:,::plot_every]
        ws10 = ws10[:,::plot_every]

    N_frames = ws1.shape[1]

    #X values
    grid = read_csv(f'grid_{DATASET}.csv',header=None)
    grid = grid.to_numpy().reshape(-1)[:-1]

    zero_line = np.zeros(len(grid))

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.subplots_adjust(left=0.1, right=0.7, top=0.85, bottom=0.1)
    ax.set_title('Evolution of the mineral composition in time')

    ax.set_ylabel('volumetric proportion')
    ax.set_xlabel('x')

    ax.set_xlim(min(grid), max(grid))
    ax.set_ylim(0, 1)  # Adjust y-axis limits based on your data

    #Plot lines

    line1 = ax.fill_between(grid, zero_line, ws1[:, 0], label='dolomite', color='orange')
    line2 = ax.fill_between(grid, ws1[:, 0], ws2[:, 0], label='antigorite', color='cyan')
    line3 = ax.fill_between(grid, ws2[:, 0], ws3[:, 0], label='talc', color='olive')
    line4 = ax.fill_between(grid, ws3[:, 0], ws4[:, 0], label='magnesite', color='yellow')
    line5 = ax.fill_between(grid, ws4[:, 0], ws5[:, 0], label='chlorite', color='coral')
    line6 = ax.fill_between(grid, ws5[:, 0], ws6[:, 0], label='quartz', color='purple')
    line7 = ax.fill_between(grid, ws6[:, 0], ws7[:, 0], label='magnetite', color='pink')
    line8 = ax.fill_between(grid, ws7[:, 0], ws8[:, 0], label='hematite', color='green')
    line9 = ax.fill_between(grid, ws8[:, 0], ws9[:, 0], label='lime', color='steelblue')
    line10 = ax.fill_between(grid, ws9[:, 0], ws10[:, 0], label='calcite', color='azure')


    # Update function for animation
    def update(frame):
        line1 = ax.fill_between(grid, zero_line, ws1[:, frame], label='dolomite', color='orange')
        line2 = ax.fill_between(grid, ws1[:, frame], ws2[:, frame], label='antigorite', color='cyan')
        line3 = ax.fill_between(grid, ws2[:, frame], ws3[:, frame], label='talc', color='olive')
        line4 = ax.fill_between(grid, ws3[:, frame], ws4[:, frame], label='magnesite', color='yellow')
        line5 = ax.fill_between(grid, ws4[:, frame], ws5[:, frame], label='chlorite', color='coral')
        line6 = ax.fill_between(grid, ws5[:, frame], ws6[:, frame], label='quartz', color='purple')
        line7 = ax.fill_between(grid, ws6[:, frame], ws7[:, frame], label='magnetite', color='pink')
        line8 = ax.fill_between(grid, ws7[:, frame], ws8[:, frame], label='hematite', color='green')
        line9 = ax.fill_between(grid, ws8[:, frame], ws9[:, frame], label='lime', color='steelblue')
        line10 = ax.fill_between(grid, ws9[:, frame], ws10[:, frame], label='calcite', color='azure')
        return line1, line2, line3, line4, line5, line6, line7, line8, line9, line10

    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, frames=N_frames, interval=1, blit=not save_animation
    )

    ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

    if save_animation:
        writer = animation.PillowWriter(fps=20, bitrate=10)
        ani.save('min_vol_animation_lowPT.gif', writer=writer, progress_callback = lambda i, n: print(f'Saving frame {i}/{n}'))


    # Display the animation
    plt.pause(0.01)
    plt.show()
    plt.legend()

def plot_mineral_vols_highPT(save_animation: bool = False, plot_every = 20):
    #Y values
    ws1 = read_csv(f'dolomite_{DATASET}.csv')
    ws1 = ws1.to_numpy().T
    ws2 = read_csv(f'talc_{DATASET}.csv')
    ws2 = ws2.to_numpy().T + ws1
    ws3 = read_csv(f'magnesite_{DATASET}.csv')
    ws3 = ws3.to_numpy().T + ws2
    ws4 = read_csv(f'chlorite_{DATASET}.csv')
    ws4 = ws4.to_numpy().T + ws3
    ws5 = read_csv(f'orthopyroxene_{DATASET}.csv')
    ws5 = ws5.to_numpy().T + ws4
    ws6 = read_csv(f'olivine_{DATASET}.csv')
    ws6 = ws6.to_numpy().T + ws5
    ws7 = read_csv(f'quartz_{DATASET}.csv')
    ws7 = ws7.to_numpy().T + ws6
    ws8 = read_csv(f'hematite_{DATASET}.csv')
    ws8 = ws8.to_numpy().T + ws7
    ws9 = read_csv(f'lime_{DATASET}.csv')
    ws9 = ws9.to_numpy().T + ws8
    ws10 = read_csv(f'calcite_{DATASET}.csv')
    ws10 = ws10.to_numpy().T + ws9
    ws11 = read_csv(f'corundum_{DATASET}.csv')
    ws11 = ws11.to_numpy().T + ws10


    if plot_every:
        ws1 = ws1[:,::plot_every]
        ws2 = ws2[:,::plot_every]
        ws3 = ws3[:,::plot_every]
        ws4 = ws4[:,::plot_every]
        ws5 = ws5[:,::plot_every]
        ws6 = ws6[:,::plot_every]
        ws7 = ws7[:,::plot_every]
        ws8 = ws8[:,::plot_every]
        ws9 = ws9[:,::plot_every]
        ws10 = ws10[:,::plot_every]
        ws11 = ws11[:,::plot_every]

    N_frames = ws1.shape[1]

    #X values
    grid = read_csv(f'grid_{DATASET}.csv',header=None)
    grid = grid.to_numpy().reshape(-1)[:-1]

    zero_line = np.zeros(len(grid))

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.subplots_adjust(left=0.1, right=0.7, top=0.85, bottom=0.1)
    ax.set_title('Evolution of the mineral composition in time')

    ax.set_ylabel('volumetric proportion')
    ax.set_xlabel('x')

    ax.set_xlim(min(grid), max(grid))
    ax.set_ylim(0, 1)  # Adjust y-axis limits based on your data

    #Plot lines

    line1 = ax.fill_between(grid, zero_line, ws1[:, 0], label='dolomite', color='orange')
    line2 = ax.fill_between(grid, ws1[:, 0], ws2[:, 0], label='talc', color='olive')
    line3 = ax.fill_between(grid, ws2[:, 0], ws3[:, 0], label='magnesite', color='yellow')
    line4 = ax.fill_between(grid, ws3[:, 0], ws4[:, 0], label='chlorite', color='coral')
    line5 = ax.fill_between(grid, ws4[:, 0], ws5[:, 0], label='orthopyroxene', color='purple')
    line6 = ax.fill_between(grid, ws5[:, 0], ws6[:, 0], label='olivine', color='pink')
    line7 = ax.fill_between(grid, ws6[:, 0], ws7[:, 0], label='quartz', color='green')
    line8 = ax.fill_between(grid, ws7[:, 0], ws8[:, 0], label='hematite', color='azure')
    line9 = ax.fill_between(grid, ws8[:, 0], ws9[:, 0], label='lime', color='orchid')
    line10 = ax.fill_between(grid, ws9[:, 0], ws10[:, 0], label='calcite', color='salmon')
    line11 = ax.fill_between(grid, ws10[:, 0], ws11[:, 0], label='corundum', color='peru')


    # Update function for animation
    def update(frame):
        line1 = ax.fill_between(grid, zero_line, ws1[:, frame], label='dolomite', color='orange')
        line2 = ax.fill_between(grid, ws1[:, frame], ws2[:, frame], label='talc', color='olive')
        line3 = ax.fill_between(grid, ws2[:, frame], ws3[:, frame], label='magnesite', color='yellow')
        line4 = ax.fill_between(grid, ws3[:, frame], ws4[:, frame], label='chlorite', color='coral')
        line5 = ax.fill_between(grid, ws4[:, frame], ws5[:, frame], label='orthopyroxene', color='purple')
        line6 = ax.fill_between(grid, ws5[:, frame], ws6[:, frame], label='olivine', color='pink')
        line7 = ax.fill_between(grid, ws6[:, frame], ws7[:, frame], label='quartz', color='green')
        line8 = ax.fill_between(grid, ws7[:, frame], ws8[:, frame], label='hematite', color='azure')
        line9 = ax.fill_between(grid, ws8[:, frame], ws9[:, frame], label='lime', color='orchid')
        line10 = ax.fill_between(grid, ws9[:, frame], ws10[:, frame], label='calcite', color='salmon')
        line11 = ax.fill_between(grid, ws10[:, frame], ws11[:, frame], label='corundum', color='peru')
        return line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11

    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, frames=N_frames, interval=1, blit=not save_animation
    )

    ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

    if save_animation:
        writer = animation.PillowWriter(fps=20, bitrate=10)
        ani.save('min_vol_animation_hightPT.gif', writer=writer, progress_callback = lambda i, n: print(f'Saving frame {i}/{n}'))


    # Display the animation
    plt.pause(0.01)
    plt.show()
    plt.legend()

def plot_mineral_vols(save_animation: bool = False, plot_every = 20):
    if DATASET == 'lowPT':
        plot_mineral_vols_lowPT(save_animation, plot_every)
    else:
        plot_mineral_vols_highPT(save_animation, plot_every)

if __name__ == '__main__':
    plot_weight_fracs(save_animation=True, plot_every=2)

