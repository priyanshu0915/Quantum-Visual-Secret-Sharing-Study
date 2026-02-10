import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import cv2

class NEQR_Processor:
    def __init__(self):
        """
        Initialize the NEQR Processor.
        Uses Qiskit Aer for simulation as described in the study.
        """
        self.simulator = AerSimulator()
        
    def encode_pixel_intensity(self, intensity_value):
        """
        Encodes a single 8-bit pixel intensity into a quantum state using NEQR principles.
        
        Args:
            intensity_value (int): Pixel intensity (0-255).
            
        Returns:
            QuantumCircuit: A circuit representing the pixel's intensity.
        """
        # We need 8 qubits to represent an 8-bit intensity value (0-255)
        # In NEQR, the intensity is encoded in the basis state |C>
        num_qubits = 8
        qc = QuantumCircuit(num_qubits, num_qubits)
        
        # Convert intensity to binary string (e.g., 255 -> '11111111')
        binary_string = format(intensity_value, '08b')
        
        # Apply X gates to qubits corresponding to '1's in the binary string
        # This sets the quantum register to the state |intensity>
        # Note: Qiskit orders bits 0 to 7 from right to left (Little Endian)
        for i, bit in enumerate(reversed(binary_string)):
            if bit == '1':
                qc.x(i)
                
        # Add measurement to verify encoding (simulating the read-out)
        qc.measure(range(num_qubits), range(num_qubits))
        
        return qc

    def run_simulation(self, circuit, shots=64):
        """
        Executes the circuit on the simulator.
        
        Args:
            circuit (QuantumCircuit): The circuit to run.
            shots (int): Number of measurement shots (default 64 per report).
        """
        # Transpile for the simulator
        transpiled_qc = transpile(circuit, self.simulator)
        
        # Run simulation
        result = self.simulator.run(transpiled_qc, shots=shots).result()
        counts = result.get_counts()
        
        return counts

if __name__ == "__main__":
    # Example Usage: Demonstrate encoding of a sample pixel
    neqr = NEQR_Processor()
    
    # Test with a sample intensity value (e.g., 170)
    sample_pixel = 170
    print(f"Encoding Pixel Intensity: {sample_pixel}")
    
    qc = neqr.encode_pixel_intensity(sample_pixel)
    counts = neqr.run_simulation(qc)
    
    # In a noise-free simulation, we expect 100% probability of the encoded state
    print(f"Simulation Results (Counts): {counts}")
    
    # Verify the result
    measured_state = list(counts.keys())[0]
    measured_int = int(measured_state, 2)
    print(f"Recovered Intensity: {measured_int}")
    
    if measured_int == sample_pixel:
        print("SUCCESS: NEQR Encoding/Decoding verified.")
