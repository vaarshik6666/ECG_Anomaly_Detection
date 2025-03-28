import logging
import matplotlib.pyplot as plt
from data_loader import load_ecg_data
from signal_processor import SignalProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting ECG Anomaly Detection System")
    
    # Load data
    signal, sampling_rate = load_ecg_data()
    logger.info(f"Sampling rate: {sampling_rate} Hz")
    
    # Process signal
    processor = SignalProcessor(sampling_rate)
    peaks = processor.detect_qrs(signal)
    
    # Plot
    plt.figure(figsize=(12, 4))
    plt.plot(signal, label='ECG Signal (Lead MLII)', alpha=0.7)
    plt.scatter(peaks, signal[peaks], color='red', label='QRS Peaks', marker='x')
    plt.title("ECG Signal with QRS Detection")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude (mV)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()