import math

def calculate_attenuation(f, mu, epsilon_real, epsilon_imag):
    """
    Calculate the attenuation coefficient (α).

    Parameters:
    f (float): Frequency (Hz)
    mu (float): Magnetic permeability (H/m)
    epsilon_real (float): Real part of permittivity (Re(ε_m))
    epsilon_imag (float): Imaginary part of permittivity (Im(ε_m))

    Returns:
    float: Attenuation coefficient (α) in Np/m
    """
    omega = 2 * math.pi * f
    term = math.sqrt(1 + (epsilon_imag / epsilon_real)**2) - 1
    inside = (mu * epsilon_real / 2) * term
    return omega * math.sqrt(inside)

# Example usage
f = 500e6              # Frequency in Hz
mu = 4 * math.pi * 1e-7  # Magnetic permeability of free space (H/m)
epsilon_real = 15.0    # Example real permittivity
epsilon_imag = 3.0     # Example imaginary permittivity

alpha = calculate_attenuation(f, mu, epsilon_real, epsilon_imag)
print(f"α: {alpha} Np/m")
