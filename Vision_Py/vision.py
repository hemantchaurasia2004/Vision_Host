import bluetooth
from filterpy.kalman import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt

def initialize_kalman_filter(initial_state, process_noise, measurement_noise):
    kf = KalmanFilter(dim_x=1, dim_z=1)
    kf.x = initial_state
    kf.F = np.array([[1]])
    kf.H = np.array([[1]])
    kf.P *= process_noise
    kf.R *= measurement_noise
    return kf

def bluetooth_scan(device_address, num_measurements):
    rssi_values = []
    
    # Scan for Bluetooth devices
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, lookup_class=True, device_id=-1, device_name='hci0')
    
    for device, _, _ in nearby_devices:
        if device == device_address:
            print(f"Found device: {device}")
            
            # Connect to the Bluetooth device
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((device, 1))
            
            for _ in range(num_measurements):
                # Read RSSI value
                rssi = bluetooth.read_rssi(sock)
                rssi_values.append(rssi)
                
            # Close the Bluetooth connection
            sock.close()
            
            break

    return np.array(rssi_values)

def main():
    device_address = "5C:ED:F4:43:03:BE"  # Replace with the address of your Bluetooth device
    num_measurements = 50
    
    # Kalman filter parameters
    initial_state = np.array([0])
    process_noise = 0.01
    measurement_noise = 5
    
    # Initialize Kalman filter
    kf = initialize_kalman_filter(initial_state, process_noise, measurement_noise)
    
    # Real-time processing loop
    filtered_rssi_values = []
    for _ in range(num_measurements):
        # Read RSSI values from Bluetooth device
        rssi_values = bluetooth_scan(device_address, num_measurements)
        
        # Apply Kalman filter
        for measurement in rssi_values:
            kf.predict()
            kf.update(measurement)
            filtered_rssi_values.append(kf.x[0])
    
    # Plot the results
    plt.plot(filtered_rssi_values, label='Filtered RSSI')
    plt.xlabel('Measurement')
    plt.ylabel('RSSI')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
