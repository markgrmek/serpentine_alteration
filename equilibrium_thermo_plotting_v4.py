from lookup_table import general_lookup
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from pandas import DataFrame, read_csv
from numpy import linspace


DATASET = 'highPT'

#LOOKUP TABLE=============================================
molar_mass = {'C': 12.011,
              'O': 15.999,
              'Si': 60.08,
              'H': 1.0078}

molar_mass['CO2'] = molar_mass['C'] + 2*molar_mass['O']
molar_mass['SiO2'] = molar_mass['Si'] + 2*molar_mass['O']
molar_mass['H2O'] = 2*molar_mass['H'] + molar_mass['O']


general_lookup = read_csv(f'general_output_{DATASET}.csv')

#caluclate oxide abundances
general_lookup['wCO2_fl'] = general_lookup['wC_fl']*(molar_mass['C']/molar_mass['CO2'])
general_lookup['wCO2_s'] = general_lookup['wC_s']*(molar_mass['C']/molar_mass['CO2'])
general_lookup['wSiO2_s'] = general_lookup['wSi_s']*(molar_mass['Si']/molar_mass['SiO2'])
general_lookup['wH2O_s'] = general_lookup['wH_s']*(molar_mass['H']/molar_mass['H2O'])


#SETUP=======================================================

P = 0.3 if DATASET == 'lowPT' else 2.5

T_STEPS, WCO2_STEPS = general_lookup['T'].unique(), general_lookup['wCO2'].unique()
EXTENT_SYS = [general_lookup['wCO2'].min(), general_lookup['wCO2'].max(), T_STEPS.min(), T_STEPS.max()]
EXTENT_S = [general_lookup['wCO2_s'].min(), general_lookup['wCO2_s'].max(), T_STEPS.min(), T_STEPS.max()]
WCO2_S_AXES = linspace(0, general_lookup['wCO2_s'].max(), 100)

T_MIN, T_MAX = general_lookup['T'].min(), general_lookup['T'].max()
WCO2_MIN, WCO2_MAX = general_lookup['wCO2'].min(), general_lookup['wCO2'].max()
WCO2_S_MIN, WCO2_S_MAX = general_lookup['wCO2_s'].min(), general_lookup['wCO2_s'].max()

def plot_wCO2_sys(key, title, colorbar_unit = '% [kg/kg]', savefig = True):
    data = []
    for T in T_STEPS:
        data.append([general_lookup[(general_lookup['T'] == T) & (general_lookup['wCO2'] == CO2)][key].values[0] for CO2 in WCO2_STEPS]) 

    fig, ax = plt.subplots()
    im = ax.imshow(data, extent=EXTENT_SYS,origin='lower', aspect='auto')
    fig.colorbar(im, ax=ax, label= f'{key} {colorbar_unit}')
    ax.set_title(f'{title} (P={P}GPa)')

    ax.invert_yaxis()
    ax.set_ylim(bottom=T_MIN, top=T_MAX)
    ax.set_ylabel('Temperature [K]')

    ax.set_xlim(left=general_lookup['wCO2'].min(), right=general_lookup['wCO2'].max())
    ax.set_xlabel(r'X = weight fraction $CO_2$ in the system')

    if savefig: fig.savefig(f'{key}_system_{DATASET}')

    plt.show() 

def plot_wCO2_solid(key: str, title: str, colorbar_unit: str = '% [kg/kg]', savefig = True):
    data = []
    for T in T_STEPS:
        #sort that the wCO2_fl values are ascending
        row: DataFrame = general_lookup[general_lookup['T'] == T]
        x_vals, y_vals = row['wCO2_s'].values, row[key].values

        # interpolate onto new grid
        f_interp = interp1d(x_vals, y_vals, kind='nearest', fill_value='extrapolate')

        interpolated_weights = f_interp(WCO2_S_AXES)  # Interpolate to common x-values
        data.append(interpolated_weights)

    fig, ax = plt.subplots()
    im = ax.imshow(data, extent=EXTENT_S, origin='lower', aspect='auto')

    fig.colorbar(im, ax=ax, label= f'{key} {colorbar_unit}')

    ax.set_title(f'{title} (P={P}GPa)')

    ax.invert_yaxis()
    ax.set_ylim(bottom=T_MIN, top=T_MAX)
    ax.set_ylabel('Temperature [K]')

    ax.set_xlim(left=WCO2_S_MIN, right=WCO2_S_MAX)
    ax.set_xlabel(r'X = weight fraction $CO_2$ in solids')

    if savefig: fig.savefig(f'{key}_interp_{DATASET}')

    plt.show()


if __name__ == '__main__':
    plot_wCO2_solid('rho_s', 'Solids density')
    plot_wCO2_sys('rho_s', 'Solids density')
    plot_wCO2_solid('rho_fl','Fluids density')
    plot_wCO2_sys('rho_fl', 'Fluids density')
    plot_wCO2_sys('wCO2_s', r'Weight fraction of $CO_2$ in solids')
    plot_wCO2_solid('wMg_s', 'Weight fraction of Mg in solids')
    plot_wCO2_sys('wMg_s', 'Weight fraction of Mg in solids')
