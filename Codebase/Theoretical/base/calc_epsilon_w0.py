def calculate_epsilon_w0(T):
    """
    Calculate the static permittivity of water (ε_w0) as a function of temperature.

    Parameters:
    T (float): Temperature (°C)

    Returns:
    float: Static permittivity of water (ε_w0)
    """
    return 87.134 - 0.1949 * T - 0.01276 * (T**2) + 2.491e-4 * (T**3)

# Example usage
T = 25  # Temperature in Celsius
epsilon_w0 = calculate_epsilon_w0(T)
print(f"ε_w0(T): {epsilon_w0}")
