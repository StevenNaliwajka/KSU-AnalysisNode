import math

def calculate_omega(f):
    """
    Calculate angular frequency (ω).

    Parameters:
    f (float): Frequency (Hz)

    Returns:
    float: Angular frequency (rad/s)
    """
    return 2 * math.pi * f

# Example usage
f = 500e6  # Frequency in Hz
omega = calculate_omega(f)
print(f"ω: {omega} rad/s")
