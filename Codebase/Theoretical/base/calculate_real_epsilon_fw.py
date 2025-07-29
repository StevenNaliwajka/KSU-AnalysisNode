import math

def calculate_real_epsilon_fw(epsilon_w0, epsilon_w_inf, f, tau_w):
    """
    Calculate the real component of free water permittivity (Re(ε_fw)).

    Parameters:
    epsilon_w0 (float): Static permittivity of water (ε_w0)
    epsilon_w_inf (float): High-frequency permittivity of water (ε_w∞)
    f (float): Frequency (Hz)
    tau_w (float): Relaxation time of water (s)

    Returns:
    float: Real component of free water permittivity (Re(ε_fw))
    """
    return (epsilon_w0 - epsilon_w_inf) / (1 + (2 * math.pi * f * tau_w)**2)

# Example usage
epsilon_w0 = 87.134  # Static permittivity of water
epsilon_w_inf = 4.9  # High-frequency permittivity of water
f = 491e6           # Frequency (Hz)
tau_w = 1e-9        # Relaxation time (s)

epsilon_fw_real = calculate_real_epsilon_fw(epsilon_w0, epsilon_w_inf, f, tau_w)
print(f"Re(ε_fw): {epsilon_fw_real}")
