import pandas as pd
import numpy as np
from typing import Literal
from scipy.interpolate import interp1d
from const import T, COLUMN_MAP, MOLAR_MASS

def pair_avg(
        array: np.ndarray[float]
        ) -> np.ndarray[float]:
    
    return (array[1:]+array[:-1])*0.5

def normalize(
        array: np.ndarray[float]
        ) -> np.ndarray[float]:

    return array/max(abs(array))

def fetch_lookup_df(
        dataset: Literal['general', 'solver'],
        PTtype: Literal['highPT', 'lowPT']
        ) -> pd.DataFrame:

    #load thermolab data
    df = pd.read_csv(f'data/thermolab_{dataset}_{PTtype}.csv')

    #caluclate oxide abundances
    df['wCO2_fl'] = df['wC_fl']*(MOLAR_MASS['C']/MOLAR_MASS['CO2'])
    df['wCO2_s'] = df['wC_s']*(MOLAR_MASS['C']/MOLAR_MASS['CO2'])
    df['wSiO2_s'] = df['wSi_s']*(MOLAR_MASS['Si']/MOLAR_MASS['SiO2'])
    df['wH2O_s'] = df['wH_s']*(MOLAR_MASS['H']/MOLAR_MASS['H2O'])

    return df

def create_solver_interpolators(
        PTtype: Literal['highPT', 'lowPT'],
        ) -> dict:

    #FECTH DATA-----------------------------------------
    df = fetch_lookup_df('solver', PTtype)
    df = df[df['T'] == T[PTtype]]
    df = df.groupby(by='wCO2_s', as_index=False).mean() #group such that each wCO2_s point is unique

    #PREPARE INTERPOLATION DATA
    to_normalize = ('rho_s', 'rho_fl', 'mu_fl') #these must be normalized

    output: dict = {}
    for key in df.columns:
        output[key] = interp1d(
            df['wCO2_s'], 
            normalize(df[key]) if key in to_normalize else df[key], 
            kind='linear', 
            fill_value='extrapolate')
        
    return output

if __name__ == '__main__':
    inte = create_solver_interpolators('lowPT')