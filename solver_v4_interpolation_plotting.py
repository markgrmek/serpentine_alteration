import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from pandas import read_csv
from lookup_table import molar_mass

def normalize(array: np.ndarray
              ) -> np.ndarray:
    return array/max(abs(array))

single_lookup = read_csv(f'single_output_lowPT.csv')

#caluclate oxide abundances

single_lookup['wCO2_fl'] = single_lookup['wC_fl']*(molar_mass['C']/molar_mass['CO2'])
single_lookup['wCO2_s'] = single_lookup['wC_s']*(molar_mass['C']/molar_mass['CO2'])
single_lookup['wSiO2_s'] = single_lookup['wSi_s']*(molar_mass['Si']/molar_mass['SiO2'])
single_lookup['wH2O_s'] = single_lookup['wH_s']*(molar_mass['H']/molar_mass['H2O'])



single_lookup = single_lookup[single_lookup['T'] == 573.15]
single_lookup = single_lookup.groupby(by='wCO2_s').mean()
wCO2_s_tabvals = single_lookup.index.to_numpy()


rho_s_norm = normalize(single_lookup['rho_s'].to_numpy().reshape(-1))
rho_fl_norm = normalize(single_lookup['rho_fl'].to_numpy().reshape(-1))
wCO2_fl_tabvals = single_lookup['wCO2_fl'].to_numpy().reshape(-1)
wMg_s_tabvals = single_lookup['wMg_s'].to_numpy().reshape(-1)
wSiO2_s_tabvals = single_lookup['wSiO2_s'].to_numpy().reshape(-1)
wH2O_s_tabvals = single_lookup['wH2O_s'].to_numpy().reshape(-1)


interp_type = 'linear'
fill_val = 'extrapolate'
rho_s_interp = interp1d(wCO2_s_tabvals, rho_s_norm, kind=interp_type, fill_value=fill_val)
rho_fl_interp = interp1d(wCO2_s_tabvals, rho_fl_norm, kind=interp_type, fill_value=fill_val)
wCO2_fl_interp = interp1d(wCO2_s_tabvals, wCO2_fl_tabvals, kind=interp_type, fill_value=fill_val)
wMg_s_interp = interp1d(wCO2_s_tabvals, wMg_s_tabvals, kind=interp_type, fill_value=fill_val)
wSiO2_s_interp = interp1d(wCO2_s_tabvals, wSiO2_s_tabvals, kind=interp_type, fill_value=fill_val)
wH2O_s_interp = interp1d(wCO2_s_tabvals, wH2O_s_tabvals, kind=interp_type, fill_value=fill_val)


wCO2_s = np.random.random(100)/40
x = np.linspace(0,1, 100)

plt.title('Interpolation functions (schematic example)')
plt.grid()
plt.plot(x, wCO2_s, label=r'weight frac. $CO_2$ solids')
plt.plot(x, rho_s_interp(wCO2_s), label=r'$rho_{solids}$ (normalized)')
plt.plot(x, wMg_s_interp(wCO2_s), label=r'weight frac. Mg solids')
plt.xlabel('X')
plt.legend()
plt.show()
