from Codebase.Theoretical.base.calc_attenuation import calculate_attenuation
from Codebase.Theoretical.base.calc_beta import calculate_beta
from Codebase.Theoretical.base.calc_epsilon_s import calculate_epsilon_s
from Codebase.Theoretical.base.calc_epsilon_w0 import calculate_epsilon_w0
from Codebase.Theoretical.base.calc_imag_epsilon_fw import calculate_imag_epsilon_fw
from Codebase.Theoretical.base.calc_imag_epsilon_m import calculate_imag_epsilon_m
from Codebase.Theoretical.base.calc_pl_soil import calculate_pl_soil
from Codebase.Theoretical.base.calc_pl_total import calculate_pl_total
from Codebase.Theoretical.base.calc_pl_total_1 import calculate_pl_total1
from Codebase.Theoretical.base.calc_real_epsilon_m import calculate_real_epsilon_m
from Codebase.Theoretical.base.calc_rssi import calculate_rssi
from Codebase.Theoretical.base.calculate_real_epsilon_fw import calculate_real_epsilon_fw
from Codebase.Theoretical.base.sigma_eff import calculate_sigma_eff


def solve_rssi_from_m_t(temp, moisture_pcnt, mounted_rssi):

    S = 12.8        # Sand (%)
    I = 72.0        # Silt (%)
    C = 15.2        # Clay (%)
    f = 491e6       # Frequency (Hz)

    G_r_mounted = 9     # Rx Gain (dBi)
    P_t_mounted = 10    # Tx Power (dBm)
    P_r_mounted = 7     # Rx Power (dBm)

    G_r_buried = 9      # Rx Gain (dBi)
    P_t_buried = 7      # Tx Power (dBm)
    P_r_buried = 7      # Rx Power (dBm)
    d_buried = 3 * 0.0254

    k = 0.65            # Shape Factor
    rho_b = 1.08        # Bulk Density (g/cm³)
    rho_s = 2.66        # Particle Density (g/cm³)
    epsilon_0 = 8.854e-12   # Permittivity of free space (F/m)
    epsilon_w_inf = 4.9     # High-frequency permittivity of water
    mu_r = 1                # Relative permeability
    mu_0 = 4 * 3.141592653589793 * 1e-7  # Permeability of free space (H/m)
    tau_w = 1e-9            # Relaxation time (s)
    j = complex(0, 1)       # Imaginary unit

    # get all the items

    temperature = temp
    moisture_pcnt = moisture_pcnt
    mounted_rssi = mounted_rssi

    #Epsilon_w0
    epsilon_w0 = calculate_epsilon_w0(temperature)

    #Sigma_eff
    sigma_eff = calculate_sigma_eff(rho_b,S,C)


    ## epsilon fw
    imag_epsilon_fw = calculate_imag_epsilon_fw(epsilon_w0,epsilon_w_inf,f,tau_w,sigma_eff,epsilon_0,rho_s,rho_b,moisture_pcnt)
    real_epsilon_fw = calculate_real_epsilon_fw(epsilon_w0,epsilon_w_inf,f,tau_w)


    #Beta
    beta = calculate_beta(S,C,imag_epsilon_fw)

    ## epsilon m
    imag_epsilon_m = calculate_imag_epsilon_m(moisture_pcnt,beta,imag_epsilon_fw,k)

    #epsilon_s
    epsilon_s = calculate_epsilon_s(rho_s)

    ##epsilon m
    real_epsilon_m = calculate_real_epsilon_m(rho_b,rho_s,epsilon_s,moisture_pcnt,beta,real_epsilon_fw,k)

    mu = mu_r * mu_0

    ##attenuation
    attenuation = calculate_attenuation(f,mu,real_epsilon_m,imag_epsilon_m)

    ## calc soil path loss
    pl_soil = calculate_pl_soil(attenuation,d_buried)

    pl_mounted = calculate_pl_total1(P_t_mounted,P_r_buried,G_r_mounted,mounted_rssi)

    pl_total = calculate_pl_total(pl_mounted,pl_soil)

    return calculate_rssi(P_t_buried,P_r_mounted, G_r_buried, pl_total)

