from pandas import read_csv

DATASET = 'lowPT' #'highPT' 

molar_mass = {'C': 12.011,
              'O': 15.999,
              'Si': 60.08,
              'H': 1.0078}

molar_mass['CO2'] = molar_mass['C'] + 2*molar_mass['O']
molar_mass['SiO2'] = molar_mass['Si'] + 2*molar_mass['O']
molar_mass['H2O'] = 2*molar_mass['H'] + molar_mass['O']


general_lookup = read_csv(f'data/general_output_{DATASET}.csv')

#caluclate oxide abundances
general_lookup['wCO2_fl'] = general_lookup['wC_fl']*(molar_mass['C']/molar_mass['CO2'])
general_lookup['wCO2_s'] = general_lookup['wC_s']*(molar_mass['C']/molar_mass['CO2'])
general_lookup['wSiO2_s'] = general_lookup['wSi_s']*(molar_mass['Si']/molar_mass['SiO2'])
general_lookup['wH2O_s'] = general_lookup['wH_s']*(molar_mass['H']/molar_mass['H2O'])