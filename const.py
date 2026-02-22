#general (solver) constants
P_SURF: int = 1 #pressure at surface (Pa) - calulated at 0.3 GPa and 2.5 GPa
WCO2_B: float = 0.0022 #CO2_s in serpentine
WCO2_SOAP: float = 0.022 #CO2_s in soapstone
POR_B: float = 0.2 #inital porosity
MU_F_B: float = 1 #dynamic viscosity of water at 25C (Pa/s)
DCO2_B: float = 1 #diffusivity of CO2 in water at 25C (m2/s)
KMUF_B: float = 1*DCO2_B/P_SURF #init permeability/fluid viscosity == k/mu_f

#thermolab pressure setup [GPa]
P: dict[str, float] = {
    'lowPT': 0.3,
    'highPT': 2.5
}

#thermolab temperature setup [K]
T: dict[str, float] = {
    'lowPT': 300 + 273.15,
    'highPT': 800 + 273.15
}

#molar masses for carbon, oxygen, silica and hydrogen and their oxides
MOLAR_MASS: dict[str, float] = {
    'C': 12.011,
    'O': 15.999,
    'Si': 60.08,
    'H': 1.0078
}

MOLAR_MASS['CO2'] = MOLAR_MASS['C'] + 2*MOLAR_MASS['O']
MOLAR_MASS['SiO2'] = MOLAR_MASS['Si'] + 2*MOLAR_MASS['O']
MOLAR_MASS['H2O'] = 2*MOLAR_MASS['H'] + MOLAR_MASS['O']

#thermoalb naming covention
COLUMN_MAP = {
    'rho_s': 'Solid density',
    'rho_fl': 'Fluid density',
    'mu_fl': 'Fluid viscosity',
    'wCO2_fl': 'CO₂ mass frac. (fluid)',
    'wMg_s': 'Mg mass frac. (solid)',
    'wSiO2_s': 'SiO₂ mass frac. (solid)',
    'wH2O_s': 'H₂O mass frac. (solid)',
    'Dolomite': 'Dolomite',
    'Antigorite': 'Antigorite',
    'Talc': 'Talc',
    'Magnesite': 'Magnesite',
    'Chlorite': 'Chlorite',
    'Orthopyroxene': 'Orthopyroxene',
    'Olivine': 'Olivine',
    'q,tc-ds633': 'Quartz',
    'mt,tc-ds633': 'Magnetite',
    'hem,tc-ds633': 'Hematite',
    'lime,tc-ds633': 'Lime',
    'cc,tc-ds633': 'Calcite',
    'cor,tc-ds633': 'Corundum'
}

#solver output map for interpolated results
INTERP_MAP = {
    'wSiO2_s': 'SiO₂ mass frac. (solid)',
    'wH2O_s': 'H₂O mass frac. (solid)',
    'Dolomite': 'Dolomite',
    'Antigorite': 'Antigorite',
    'Talc': 'Talc',
    'Magnesite': 'Magnesite',
    'Chlorite': 'Chlorite',
    'Orthopyroxene': 'Orthopyroxene',
    'Olivine': 'Olivine',
    'q,tc-ds633': 'Quartz',
    'mt,tc-ds633': 'Magnetite',
    'hem,tc-ds633': 'Hematite',
    'lime,tc-ds633': 'Lime',
    'cc,tc-ds633': 'Calcite',
    'cor,tc-ds633': 'Corundum'
}

#solver output map for calculated (non-interpolated) results
NONINTERP_MAP = {
    'time': 'simulation time',
    'wCO2_s': 'CO₂ mass frac. (solid)',
    'wCO2_fl': 'CO₂ mass frac. (fluid)',
    'por': 'Porosity',
    'rho_tot': 'Total density'
}

