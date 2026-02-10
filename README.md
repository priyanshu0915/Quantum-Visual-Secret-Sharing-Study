# Quantum-Visual-Secret-Sharing-Study
# Quantum Visual Secret Sharing (QVSS) Study

This repository contains an experimental study and implementation of fundamental concepts in Quantum Visual Secret Sharing (QVSS) and Quantum Image Processing (QIP). The project focuses on the implementation of quantum image representation standards and basic secret sharing simulation using IBM's Qiskit framework.

## 📂 Project Overview

The goal of this project is to explore how digital images can be encoded into quantum states and how classical secret sharing principles interact with quantum circuit simulations.

### Key Features Implemented:
* **NEQR (Novel Enhanced Quantum Representation):** Implementation of the standard NEQR protocol to encode 128x128 grayscale images into quantum superposition states.
* **Image Pre-processing:** Automated conversion of classical datasets (Medical, Natural, and Synthetic images) into binary sequences suitable for quantum encoding.
* **Quantum Circuit Simulation:** Utilization of `Qiskit Aer` to simulate quantum state preparation and measurement.
* **Quality Metrics:** Scripts to calculate Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM) to evaluate reconstruction fidelity in simulation environments.

## 🛠️ Technologies & Tools

* **Language:** Python 3.11.9
* **Quantum Framework:** Qiskit 0.45.0 (Aer Simulator)
* **Image Processing:** OpenCV 4.8.0, Pillow 10.0.0
* **Scientific Computing:** NumPy, SciPy

## 📊 Dataset

The study utilizes a standard diverse dataset for testing image encoding capabilities:
* Standard Test Images (Lena, Baboon, etc.)
* Medical Imaging Samples (X-Ray, MRI)
* Synthetic Patterns (Checkerboards)

## 🚀 Getting Started

### Prerequisites
```bash
pip install qiskit qiskit-aer opencv-python pillow numpy matplotlib
