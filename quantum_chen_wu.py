from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np
from neqr_basics import neqr_encode_pixel

class QuantumChenWu:
    def __init__(self):
        self.simulator = AerSimulator()

    def build_sharing_circuit(self, g0_val, g1_val):
        """
        Implements the Chen-Wu (2,3) scheme in the Quantum Domain.
        
        Logic (Standard Quantum XOR):
        1. Encodes Secrets G0, G1 using NEQR.
        2. Prepares random share S0.
        3. Computes B0 = G1 XOR S0 (using CNOTs).
        4. Computes Sn = G0 XOR B0 (using CNOTs).
        """
        # Define Quantum Registers (8 qubits each for 8-bit pixels)
        q_g0 = QuantumRegister(8, 'g0') # Secret 1
        q_g1 = QuantumRegister(8, 'g1') # Secret 2
        q_s0 = QuantumRegister(8, 's0') # Random Share
        q_b0 = QuantumRegister(8, 'b0') # Intermediate Share
        q_sn = QuantumRegister(8, 'sn') # Final Share
        
        # Classical Registers for measurement
        c_out = ClassicalRegister(24, 'measure') # To store outputs
        
        qc = QuantumCircuit(q_g0, q_g1, q_s0, q_b0, q_sn, c_out)
        
        # --- STEP 1: NEQR ENCODING (State Preparation) ---
        # Encode Secret G0
        g0_circ = neqr_encode_pixel(g0_val)
        qc.compose(g0_circ, qubits=q_g0, inplace=True)
        
        # Encode Secret G1
        g1_circ = neqr_encode_pixel(g1_val)
        qc.compose(g1_circ, qubits=q_g1, inplace=True)
        
        # --- STEP 2: RANDOM SHARE GENERATION (S0) ---
        # In a real quantum VSS, S0 is a superposition or random state.
        # Here we use Hadamard gates to create superposition (Randomness source)
        qc.h(q_s0)
        
        # --- STEP 3: QUANTUM CHEN-WU OPERATIONS (CNOT Chain) ---
        # Logic: B0 = G1 XOR S0
        # In Quantum: CNOT(Control, Target) performs XOR on the Target.
        # We copy G1 to B0, then XOR S0 into B0.
        for i in range(8):
            qc.cx(q_g1[i], q_b0[i]) # B0 now holds G1
            qc.cx(q_s0[i], q_b0[i]) # B0 now holds G1 ^ S0
            
        # Logic: Sn = G0 XOR B0
        # We copy G0 to Sn, then XOR B0 into Sn.
        for i in range(8):
            qc.cx(q_g0[i], q_sn[i]) # Sn now holds G0
            qc.cx(q_b0[i], q_sn[i]) # Sn now holds G0 ^ B0
            
        # --- STEP 4: MEASUREMENT ---
        # We measure the shares S0, B0, Sn to "distribute" them
        qc.measure(q_s0, c_out[0:8])
        qc.measure(q_b0, c_out[8:16])
        qc.measure(q_sn, c_out[16:24])
        
        return qc

    def run_simulation(self, circuit):
        """Simulate the circuit and return counts."""
        transpiled_qc = transpile(circuit, self.simulator)
        result = self.simulator.run(transpiled_qc, shots=1).result()
        return result.get_counts()

if __name__ == "__main__":
    # Test Values (Pixel Intensities)
    secret_g0 = 200 # Example intensity
    secret_g1 = 55  # Example intensity
    
    print(f"--- Quantum Chen-Wu Simulation ---")
    print(f"Secret G0: {secret_g0}")
    print(f"Secret G1: {secret_g1}")
    
    qcw = QuantumChenWu()
    qc = qcw.build_sharing_circuit(secret_g0, secret_g1)
    
    # Run Simulation
    counts = qcw.run_simulation(qc)
    
    # Parse Result (Just taking the first shot for demonstration)
    raw_bits = list(counts.keys())[0]
    
    # Qiskit output is reversed string. We need to split it.
    # Bit order in string: [Sn][B0][S0] (reading left to right)
    sn_bits = raw_bits[0:8]
    b0_bits = raw_bits[8:16]
    s0_bits = raw_bits[16:24]
    
    s0_val = int(s0_bits, 2)
    b0_val = int(b0_bits, 2)
    sn_val = int(sn_bits, 2)
    
    print(f"\nGenerated Quantum Shares:")
    print(f"Share S0 (Random): {s0_val}")
    print(f"Share B0: {b0_val}")
    print(f"Share Sn: {sn_val}")
    
    # Verification (Classical XOR to check logic)
    # Reconstruct G1 = B0 ^ S0
    rec_g1 = b0_val ^ s0_val
    # Reconstruct G0 = Sn ^ B0
    rec_g0 = sn_val ^ b0_val
    
    print(f"\nReconstruction Check:")
    print(f"Recovered G0: {rec_g0} (Match: {rec_g0 == secret_g0})")
    print(f"Recovered G1: {rec_g1} (Match: {rec_g1 == secret_g1})")
