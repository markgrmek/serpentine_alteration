import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pandas import read_csv
import ffmpeg

DCO2_B: float = 1.88e-6

def plot_density(save_animation: bool = False, plot_every = 20):
    #time
    time = read_csv('time.csv')
    time = time.to_numpy().reshape(-1)

    #Y values
    ws1 = read_csv('density.csv')
    ws1 = ws1.to_numpy().T


    if plot_every: 
        ws1 = ws1[:,::plot_every]
        time = time[::plot_every]

    N_frames = ws1.shape[1]

    #X values
    grid = read_csv('grid.csv',header=None)
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
        ani.save('density_animation.gif', writer=writer, progress_callback = lambda i, n: print(f'Saving frame {i}/{n}'))

    # Display the animation
    plt.pause(0.01)
    plt.show()
    plt.legend()

def plot_porosity(save_animation: bool = False, plot_every = 20):
    #time
    time = read_csv('time.csv')
    time = time.to_numpy().reshape(-1)

    #Y values
    ws1 = read_csv('por.csv')
    ws1 = ws1.to_numpy().T

    init_por = [0.2]*20
    if plot_every: 
        ws1 = ws1[:,::plot_every]
        time = time[::plot_every]

    N_frames = ws1.shape[1]

    #X values
    grid = read_csv('grid.csv',header=None)
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
    init_por, = ax.plot(grid, init_por, label=f'initial porosity', color='orange', linestyle=':')
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
        ani.save('por_animation.gif', writer=writer, progress_callback = lambda i, n: print(f'Saving frame {i}/{n}'))

    # Display the animation
    plt.pause(0.01)
    plt.show()
    plt.legend()

def plot_weight_fracs(save_animation: bool = False, plot_every = 20):
    #time
    time = read_csv('time.csv')
    time = time.to_numpy().reshape(-1)

    #Y values
    ws1 = read_csv('wCO2_s.csv')
    ws1 = ws1.to_numpy().T
    
    ws2 = read_csv('wCO2_fl.csv')
    ws2 = ws2.to_numpy().T

    ws3 = read_csv('wSiO2_s.csv')
    ws3 = ws3.to_numpy().T

    ws4 = read_csv('wH2O_s.csv')
    ws4 = ws4.to_numpy().T

    if plot_every: 
        ws1 = ws1[:,::plot_every]
        ws2 = ws2[:,::plot_every]
        ws3 = ws3[:,::plot_every]
        ws4 = ws4[:,::plot_every]
        time = time[::plot_every]

    N_frames = ws1.shape[1]

    soap_lvl = 0.04715
    serp_lvl = 0.004

    #X values
    grid = read_csv('grid.csv',header=None)
    grid = grid.to_numpy().reshape(-1)[:-1]

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.subplots_adjust(left=0.1, right=0.7, top=0.85, bottom=0.1)
    fig.suptitle('Evolution of weight frac. of species in time')

    ax.set_xlabel('x')
    ax.set_ylabel(r'weight frac. of $CO_2$')

    ax.set_xlim(min(grid), max(grid))
    ax.set_ylim(0, 0.05)  # Adjust y-axis limits based on your data

    #Plot lines
    text = ax.text(0.8, 0.8, 'Time', transform=ax.transAxes, fontsize=12, color='black', ha='center')

    soap, = ax.plot(grid, np.ones(len(grid))*soap_lvl, label=f'{r'$CO_2$'} soapstone ({soap_lvl})', color='orange', linestyle=':')
    serp, = ax.plot(grid, np.ones(len(grid))*serp_lvl, label=f'{r'$CO_2$'} serpentine ({serp_lvl})', color='green', linestyle=':')  

    line1, = ax.plot(grid, ws1[:, 0], label=f'{r'$CO_2$'} solids', color='gray')
    line2, = ax.plot(grid, ws2[:, 0], label=f'{r'$CO_2$'} fluids', color='cyan', linestyle='--')
    line3, = ax.plot(grid, ws1[:, 0], label=f'{r'$SiO_2$'} solids', color='brown', linestyle='--')
    line4, = ax.plot(grid, ws2[:, 0], label=f'{r'$H_2O$'}  solids', color='blue', linestyle='--')

    def update(frame):
        line1.set_ydata(ws1[:, frame])
        line2.set_ydata(ws2[:, frame])
        line3.set_ydata(ws3[:, frame])
        line4.set_ydata(ws4[:, frame])
        text.set_text(f'time {(time[frame]/DCO2_B/(365*24*60*60)):.1f} y')
        return text, line1, line2

    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, frames=N_frames, interval=10, blit= not save_animation
    )

    ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

    if save_animation: 
        writer = animation.PillowWriter(fps=20, bitrate=10)
        ani.save('weight_frac_animation.gif', writer=writer, progress_callback = lambda i, n: print(f'Saving frame {i}/{n}'))

    # Display the animation
    plt.pause(0.001)
    plt.show()
    plt.legend()

# def plot_CO2(save_animation: bool = False, plot_every = 20):
#     #time
#     time = read_csv('time.csv')
#     time = time.to_numpy().reshape(-1)

#     #Y values
#     ws1 = read_csv('wCO2_s.csv')
#     ws1 = ws1.to_numpy().T
    
#     ws2 = read_csv('wCO2_fl.csv')
#     ws2 = ws2.to_numpy().T

#     if plot_every: 
#         ws1 = ws1[:,::plot_every]
#         ws2 = ws2[:,::plot_every]
#         time = time[::plot_every]

#     N_frames = ws1.shape[1]

#     soap_lvl = 0.04715
#     serp_lvl = 0.004

#     #X values
#     grid = read_csv('grid.csv',header=None)
#     grid = grid.to_numpy().reshape(-1)[:-1]

#     # Set up the figure and axis
#     fig, ax = plt.subplots(figsize=(8, 4))
#     fig.subplots_adjust(left=0.1, right=0.7, top=0.85, bottom=0.1)
#     fig.suptitle(r'Evolution of $CO_2$ in time')

#     ax.set_xlabel('x')
#     ax.set_ylabel(r'weight frac. of $CO_2$')

#     ax.set_xlim(min(grid), max(grid))
#     ax.set_ylim(0, 0.05)  # Adjust y-axis limits based on your data

#     #Plot lines
#     text = ax.text(0.8, 0.8, 'Time', transform=ax.transAxes, fontsize=12, color='black', ha='center')

#     soap, = ax.plot(grid, np.ones(len(grid))*soap_lvl, label=f'soapstone ({soap_lvl})', color='orange', linestyle=':')
#     serp, = ax.plot(grid, np.ones(len(grid))*serp_lvl, label=f'serpentine ({serp_lvl})', color='green', linestyle=':')  

#     line0, = ax.plot(grid, ws1[:, 0], label='solids', color='gray')
#     line1, = ax.plot(grid, ws2[:, 0], label='fluids', color='cyan', linestyle='--')

#     def update(frame):
#         line0.set_ydata(ws1[:, frame])
#         line1.set_ydata(ws2[:, frame])
#         text.set_text(f'time {(time[frame]/DCO2_B/(365*24*60*60)):.1f} y')
#         # line0, = ax.plot(grid, ws1[:, frame], label='solids', color='gray')
#         # line1, = ax.plot(grid, ws2[:, frame], label='fluids', color='cyan', linestyle='--')  
#         return text, line0, line1

#     # Create the animation
#     ani = animation.FuncAnimation(
#         fig, update, frames=N_frames, interval=10, blit= not save_animation
#     )

#     ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

#     if save_animation: 
#         writer = animation.PillowWriter(fps=20, bitrate=10)
#         ani.save('CO2_animation.gif', writer=writer, progress_callback = lambda i, n: print(f'Saving frame {i}/{n}'))

#     # Display the animation
#     plt.pause(0.001)
#     plt.show()
#     plt.legend()

def plot_mineral_vols(save_animation: bool = False, plot_every = 20):
    #Y values
    ws1 = read_csv('vol_solids0.csv')
    ws1 = ws1.to_numpy().T
    ws2 = read_csv('vol_solids1.csv')
    ws2 = ws2.to_numpy().T + ws1
    ws3 = read_csv('vol_solids2.csv')
    ws3 = ws3.to_numpy().T + ws2
    ws4 = read_csv('vol_solids3.csv')
    ws4 = ws4.to_numpy().T + ws3
    ws5 = read_csv('vol_solids4.csv')
    ws5 = ws5.to_numpy().T + ws4
    ws6 = read_csv('vol_solids5.csv')
    ws6 = ws6.to_numpy().T + ws5

    if plot_every:
        ws1 = ws1[:,::plot_every]
        ws2 = ws2[:,::plot_every]
        ws3 = ws3[:,::plot_every]
        ws4 = ws4[:,::plot_every]
        ws5 = ws5[:,::plot_every]
        ws6 = ws6[:,::plot_every]

    N_frames = ws1.shape[1]

    #X values
    grid = read_csv('grid.csv',header=None)
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
    lables = 'Chlorite', 'Antigorite', 'Talc', 'Magnesite', 'Dolomite', 'q,tc-ds55'

    line0 = ax.fill_between(grid, zero_line, ws1[:, 0], label=lables[0], color='red')
    line1 = ax.fill_between(grid, ws1[:, 0], ws2[:, 0], label=lables[1], color='cyan')
    line2 = ax.fill_between(grid, ws2[:, 0], ws3[:, 0], label=lables[2], color='blue')
    line3 = ax.fill_between(grid, ws3[:, 0], ws4[:, 0], label=lables[3], color='yellow')
    line4 = ax.fill_between(grid, ws4[:, 0], ws5[:, 0], label=lables[4], color='orange')
    line5 = ax.fill_between(grid, ws5[:, 0], ws6[:, 0], label=lables[5], color='purple')

    # Update function for animation
    def update(frame):
        line0 = ax.fill_between(grid, 0, ws1[:, frame], color='red')
        line1 = ax.fill_between(grid, ws1[:, frame], ws2[:, frame], color='cyan')
        line2 = ax.fill_between(grid, ws2[:, frame], ws3[:, frame], color='blue')
        line3 = ax.fill_between(grid, ws3[:, frame], ws4[:, frame], color='yellow')
        line4 = ax.fill_between(grid, ws4[:, frame], ws5[:, frame], color='orange')
        line5 = ax.fill_between(grid, ws5[:, frame], ws6[:, frame], color='purple')
       
        return line0, line1, line2, line3, line4, line5

    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, frames=N_frames, interval=1, blit=not save_animation
    )

    ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

    if save_animation:
        writer = animation.PillowWriter(fps=20, bitrate=10)
        ani.save('min_vol_animation.gif', writer=writer, progress_callback = lambda i, n: print(f'Saving frame {i}/{n}'))


    # Display the animation
    plt.pause(0.01)
    plt.show()
    plt.legend()

if __name__ == '__main__':
    plot_mineral_vols(save_animation=True, plot_every=300)


