def calculate_rssi(P_t, G_t, G_r, PL_total):
    """
    Calculate RSSI based on transmit power, antenna gains, and total path loss.

    Parameters:
    P_t (float): Transmit power (dBm)
    G_t (float): Transmitter antenna gain (dBi)
    G_r (float): Receiver antenna gain (dBi)
    PL_total (float): Total path loss (dB)

    Returns:
    float: Received Signal Strength Indicator (RSSI) in dBm
    """
    return P_t + G_t + G_r - PL_total

# Example usage
P_t = 20       # Transmit power in dBm
G_t = 5        # Transmitter antenna gain in dBi
G_r = 5        # Receiver antenna gain in dBi
PL_total = 80  # Total path loss in dB

rssi = calculate_rssi(P_t, G_t, G_r, PL_total)
print(f"RSSI: {rssi} dBm")
