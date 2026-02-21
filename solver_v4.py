from numpy import array, ndarray, linspace, diff, savetxt
from numpy import max as npmax
from numpy import abs as npabs
from scipy.interpolate import interp1d
from lookup_table import DATASET

def pair_avg(array: ndarray[int|float]
             ) -> ndarray[int|float]:
    return (array[1:]+array[:-1])*0.5

def normalize(array: ndarray
              ) -> ndarray:
    return array/max(abs(array))

#CONSTANTS========================================================================================
P: int = 1 #pressure at surface (Pa) - calulated at 0.3 GPa and 2.5 GPa
T: float =  300 + 273.15 if DATASET == 'lowPT' else 800 + 273.15
WCO2_B: float = 0.0235 #0.004   #CO2_s in serpentine
WCO2_SOAP: float = 0.1488 #0.04715  #CO2_s in soapstone
POR_B: float = 0.2 #init porosity
MU_F_B: float = 1# 0.8891e-3 #dynamic viscosity of water at 25C (Pa/s)
DCO2_B: float = 1 #1.88e-6 #diffusivity of CO2 in water at 25C (m2/s)
KMUF_B: float = 1*DCO2_B/P #init permeability/fluid viscosity == k/mu_f

#SOLVER AND DOMAIN PARAMETERS=====================================================================
L = 1 #domain length (m)
N_cells: int = 200 #number of cells
dx = L/N_cells  #step in x (m)
x: ndarray[float] = linspace(0,L,N_cells+1) #discrete domain

time_tot: float = 100*L**2/DCO2_B #total integration time (s)
N_steps: int = int(1e9) #number of time steps

npow: int = 3 #non linearity in permeability
N_sweeps: int = int(1e5) #number of sweeps
N_Pf_max: int = int(1e4) #maximum number of fluid pressure sweeps
tolerance: float = 1e-6 #tolerance of our approximation
dec_print: int = 10 #decimal precision when printing result


print(':::CREATING INTERPOLATING FUNCTIONS:::')

single_lookup = single_lookup[single_lookup['T'] == T]
single_lookup = single_lookup.groupby(by='wCO2_s').mean()
wCO2_s_tabvals = single_lookup.index.to_numpy()


rho_s_norm = normalize(single_lookup['rho_s'].to_numpy().reshape(-1))
rho_fl_norm = normalize(single_lookup['rho_fl'].to_numpy().reshape(-1))
mu_fl_norm = normalize(single_lookup['mu_fl'].to_numpy().reshape(-1))
wCO2_fl_tabvals = single_lookup['wCO2_fl'].to_numpy().reshape(-1)
wMg_s_tabvals = single_lookup['wMg_s'].to_numpy().reshape(-1)
wSiO2_s_tabvals = single_lookup['wSiO2_s'].to_numpy().reshape(-1)
wH2O_s_tabvals = single_lookup['wH2O_s'].to_numpy().reshape(-1)
dolomite_tabvals = single_lookup['Dolomite'].to_numpy().reshape(-1)
antigorite_tabvals = single_lookup['Antigorite'].to_numpy().reshape(-1)
talc_tabvals = single_lookup['Talc'].to_numpy().reshape(-1)
magnesite_tabvals = single_lookup['Magnesite'].to_numpy().reshape(-1)
chlorite_tabvals = single_lookup['Chlorite'].to_numpy().reshape(-1)
orthopyroxene_tabvals = single_lookup['Orthopyroxene'].to_numpy().reshape(-1)
olivine_tabvals = single_lookup['Olivine'].to_numpy().reshape(-1)
quartz_tabvals = single_lookup['q,tc-ds633'].to_numpy().reshape(-1)
magnetite_tabvals = single_lookup['mt,tc-ds633'].to_numpy().reshape(-1)
hematite_tabvals = single_lookup['hem,tc-ds633'].to_numpy().reshape(-1)
lime_tabvals = single_lookup['lime,tc-ds633'].to_numpy().reshape(-1)
calcite_tabvals = single_lookup['cc,tc-ds633'].to_numpy().reshape(-1)
corundum_tabvals = single_lookup['cor,tc-ds633'].to_numpy().reshape(-1)

interp_type = 'linear'
fill_val = 'extrapolate'
rho_s_interp = interp1d(wCO2_s_tabvals, rho_s_norm, kind=interp_type, fill_value=fill_val)
rho_fl_interp = interp1d(wCO2_s_tabvals, rho_fl_norm, kind=interp_type, fill_value=fill_val)
wCO2_fl_interp = interp1d(wCO2_s_tabvals, wCO2_fl_tabvals, kind=interp_type, fill_value=fill_val)
wMg_s_interp = interp1d(wCO2_s_tabvals, wMg_s_tabvals, kind=interp_type, fill_value=fill_val)
mu_fl_interp = interp1d(wCO2_s_tabvals, mu_fl_norm, kind=interp_type, fill_value=fill_val)
wSiO2_s_interp = interp1d(wCO2_s_tabvals, wSiO2_s_tabvals, kind=interp_type, fill_value=fill_val)
wH2O_s_interp = interp1d(wCO2_s_tabvals, wH2O_s_tabvals, kind=interp_type, fill_value=fill_val)
dolomite_interp = interp1d(wCO2_s_tabvals, dolomite_tabvals, kind=interp_type, fill_value=fill_val)
antigorite_interp = interp1d(wCO2_s_tabvals, antigorite_tabvals, kind=interp_type, fill_value=fill_val)
talc_interp = interp1d(wCO2_s_tabvals, talc_tabvals, kind=interp_type, fill_value=fill_val)
magnesite_interp = interp1d(wCO2_s_tabvals, magnesite_tabvals, kind=interp_type, fill_value=fill_val)
chlorite_interp = interp1d(wCO2_s_tabvals, chlorite_tabvals, kind=interp_type, fill_value=fill_val)
orthopyroxene_interp = interp1d(wCO2_s_tabvals, orthopyroxene_tabvals, kind=interp_type, fill_value=fill_val)
olivine_interp = interp1d(wCO2_s_tabvals, olivine_tabvals, kind=interp_type, fill_value=fill_val)
quartz_interp = interp1d(wCO2_s_tabvals, quartz_tabvals, kind=interp_type, fill_value=fill_val)
magnetite_interp = interp1d(wCO2_s_tabvals, magnetite_tabvals, kind=interp_type, fill_value=fill_val)
hematite_interp = interp1d(wCO2_s_tabvals, hematite_tabvals, kind=interp_type, fill_value=fill_val)
lime_interp = interp1d(wCO2_s_tabvals, lime_tabvals, kind=interp_type, fill_value=fill_val)
calcite_interp = interp1d(wCO2_s_tabvals, calcite_tabvals, kind=interp_type, fill_value=fill_val)
corundum_interp = interp1d(wCO2_s_tabvals, corundum_tabvals, kind=interp_type, fill_value=fill_val)

por0: ndarray[float] = array([POR_B]*N_cells) #initial porosity
wCO2_s0: ndarray[float] = array([WCO2_SOAP]+[WCO2_B]*(N_cells-1)) #initial CO2 fluid (lefftmost cell soapstone, the rest serpentine)
P_fl0: ndarray[float] = array([P*i/N_cells for i in range(N_cells, 0, -1)]) #initial fluid pressure gradient (from P_0 to 0 as x from 0 to L)

print(':::CALCULATION STARTED:::')
wCO2_s = wCO2_s0
P_fl = P_fl0
time = 0
por_rho_s_wMg0 = None #mass of immobile species at t=0
rho_tot_prev = None #total density at previous time step

#OUTPUT ARRAYS
time_output: list = []
wCO2_s_output: list = []
wCO2_fl_output: list = []
por_output: list = []
density_output: list = []
wSiO2_s_output: list = []
wH2O_s_output: list = []
dolomite_output: list = []
antigorite_output: list = []
talc_output: list = []
magnesite_output: list = []
chlorite_output: list = []
orthopyroxene_output: list = []
olivine_output: list = []
quartz_output: list = []
magnetite_output: list = []
hematite_output: list = []
lime_output: list = []
calcite_output: list = []
corundum_output: list = []

for time_step in range(N_steps):
    #fetch data from lookup table
    rho_s: ndarray[float] = rho_s_interp(wCO2_s)
    rho_fl: ndarray[float] = rho_fl_interp(wCO2_s)
    wCO2_fl: ndarray[float] = wCO2_fl_interp(wCO2_s)
    wMg_s: ndarray[float] = wMg_s_interp(wCO2_s)
    mu_fl: ndarray[float] = mu_fl_interp(wCO2_s)

    #calculate imobile species density
    if time_step == 0:
        por_rho_s_wMg0 = rho_s*wMg_s*(1-por0) #store initial value

    rho_im = rho_s*wMg_s
    por = 1 - por_rho_s_wMg0/rho_im #calulcate porosity
    rho_tot = rho_fl*por + rho_s*(1-por) #calulcate total density
    if time_step == 0:
        rho_tot_prev = rho_tot #store initial value
    rho_CO2_tot = rho_fl*por*wCO2_fl + rho_s*(1-por)*wCO2_s #calculate total rho CO2

        #ARRAY SIZE -1
    #average values between the nodes
    rho_fl_avg = pair_avg(rho_fl) #density of fluid
    rho_CO2_fl_avg = rho_fl*wCO2_fl
    rho_CO2_fl_avg = pair_avg(rho_CO2_fl_avg) #density of CO2_fl in the system
    por_avg = pair_avg(por) #porosity
    perm_avg = KMUF_B*por_avg**npow  #permeability (muf = muf0*muf_r, thus k_muf0/muf_r = m_muf)
    dCO2_avg = rho_CO2_fl_avg*por_avg*DCO2_B #diffusivity

    #PRESSURE SWEEPS
    rho_tot_delta = rho_tot[1:-1]-rho_tot_prev[1:-1]
    for sweep in range(N_sweeps):
        P_grad = diff(P_fl)/dx #calculate pressure gradient in x


        #define proper time step
        dt_diff = 0.45*dx**2/DCO2_B #calulate max time step for diffusion
        dt_adv = rho_fl_avg*perm_avg*P_grad
        dt_adv = 0.45*dx/npmax(npabs(dt_adv)) #calulate max time step for advection
        time_remain = time_tot-time #calculate remaining time
        dt = min((dt_diff, dt_adv, time_remain)) #we use whicever timestep is smaller to achieve stability

        #dt is the bottle neck 
        if (dt == 0.0 and 
            time_remain == 0.0): #end of simulation
            break
        
        elif (dt == 0.0 and 
              time_remain > 0.0): #dt is 0 but we are not at the end
            raise ValueError('dt is 0')

        #calulate Darcy flux
        flux = -perm_avg*P_grad

        #calculate the residual pressure of total mass balance and update pressures (leave out outermost cells == BC)
        P_res = - rho_tot_delta/dt - diff(rho_fl_avg*flux)/dx #this term should ideally be 0
        sweep_calc = dx**2/npmax(perm_avg*rho_fl_avg)/4*P_res
        P_fl[1:-1] = P_fl[1:-1] + sweep_calc

        if npmax(npabs(P_res)) <= tolerance: #break when the pressure is sufficiently swept
            break

        if sweep == N_sweeps:
            print('Pressure sweeping failed. Adjust parameters')
    
    #diffusivity flux
    diff_flux = -dCO2_avg*diff(mu_fl)/dx

    #adjust the weight fraction of CO2 in the system - leave out the boundary conditions (leftmost is already soapstone, rightmost stays serpentine)
    rho_CO2_tot_itm = diff_flux + rho_CO2_fl_avg*flux
    rho_CO2_tot_itm = diff(rho_CO2_tot_itm)
    rho_CO2_tot[1:-1] = rho_CO2_tot[1:-1] - dt*(rho_CO2_tot_itm/dx)

    #calculate new value of CO2 in fluid from the balance equation
    wCO2_s = (rho_CO2_tot - wCO2_fl*rho_fl*por)/rho_s/(1-por)

    #UPDATE VALUES ---------------------------------
    #P_fl gets update inside the loop
    #wCO2_s gets updated at the end
    #rho_im0 gets updated just in the first iteration (rho_im at t=0)
    rho_tot_prev = rho_tot
    time += dt
   
    #PRINT RESULTS-----------------------------------
    if time_step % 100 == 0: #print out result of each time step
        print(f"""
                :::TIMESTEP: {time_step} => TIME: {time}s of {time_tot}s:::
                Domain: {x[:2].round(dec_print)} ... {x[-2:].round(dec_print)};
                Fluid pressure: {P_fl[:2].round(dec_print)} ... {P_fl[-2:].round(dec_print)};
                CO2 in solids: {wCO2_s[:2].round(dec_print)} ... {wCO2_s[-2:].round(dec_print)};
                Porosity: {por[:2].round(dec_print)} ... {por[-2:].round(dec_print)};
                Permeability: {perm_avg[:2].round(dec_print)} ... {perm_avg[-2:].round(dec_print)};
                CO2 diffusivity: {dCO2_avg[:2].round(dec_print)} ... {dCO2_avg[-2:].round(dec_print)};
                """)
        
        print('storing results...')
        #Add results
        time_output.append(time)
        wCO2_s_output.append(wCO2_s)
        wCO2_fl_output.append(wCO2_fl)
        por_output.append(por)
        density_output.append(rho_tot)
        wSiO2_s_output.append(wSiO2_s_interp(wCO2_s))
        wH2O_s_output.append(wH2O_s_interp(wCO2_s))
        dolomite_output.append(dolomite_interp(wCO2_s))
        antigorite_output.append(antigorite_interp(wCO2_s))
        talc_output.append(talc_interp(wCO2_s))
        magnesite_output.append(magnesite_interp(wCO2_s))
        chlorite_output.append(chlorite_interp(wCO2_s))
        orthopyroxene_output.append(orthopyroxene_interp(wCO2_s))
        olivine_output.append(olivine_interp(wCO2_s))
        quartz_output.append(quartz_interp(wCO2_s))
        magnetite_output.append(magnetite_interp(wCO2_s))
        hematite_output.append(hematite_interp(wCO2_s))
        lime_output.append(lime_interp(wCO2_s))
        calcite_output.append(calcite_interp(wCO2_s))
        corundum_output.append(corundum_interp(wCO2_s))
    
    #SAVE RESULTS
    if time == time_tot or time_step==(N_steps-1):
        print(':::CALULCATION FINISHED:::')
        print('saving results...')

        wCO2_s_output = array(wCO2_s_output)
        savetxt(fname=f'grid_{DATASET}.csv', X=x, delimiter=',', fmt='%f')
        savetxt(fname=f'time_{DATASET}.csv', X=time_output, delimiter=',', fmt='%.18e')
        savetxt(fname=f'wCO2_s_{DATASET}.csv',X=wCO2_s_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'wCO2_fl_{DATASET}.csv',X=wCO2_fl_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'por_{DATASET}.csv',X=por_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'density_{DATASET}.csv',X=density_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'wSiO2_s_{DATASET}.csv',X=wSiO2_s_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'wH2O_s_{DATASET}.csv',X=wH2O_s_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'dolomite_{DATASET}.csv',X=dolomite_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'antigorite_{DATASET}.csv',X=antigorite_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'talc_{DATASET}.csv',X=talc_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'magnesite_{DATASET}.csv',X=magnesite_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'chlorite_{DATASET}.csv',X=chlorite_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'orthopyroxene_{DATASET}.csv',X=orthopyroxene_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'olivine_{DATASET}.csv',X=olivine_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'quartz_{DATASET}.csv',X=quartz_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'magnetite_{DATASET}.csv',X=magnetite_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'hematite_{DATASET}.csv',X=hematite_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'lime_{DATASET}.csv',X=lime_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'calcite_{DATASET}.csv',X=calcite_output,delimiter=',',fmt='%.18e')
        savetxt(fname=f'corundum_{DATASET}.csv',X=corundum_output,delimiter=',',fmt='%.18e')
        break


        

