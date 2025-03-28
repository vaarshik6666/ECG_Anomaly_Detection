import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignalProcessor:
    def __init__(self, sampling_rate):
        self.sampling_rate = sampling_rate
    
    def bandpass_filter(self, signal, lowcut=5.0, highcut=15.0):
        """Bandpass filter to isolate QRS frequencies."""
        from scipy.signal import butter, filtfilt
        nyquist = 0.5 * self.sampling_rate
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(2, [low, high], btype='band')
        return filtfilt(b, a, signal)
    
    def detect_qrs(self, signal):
        """Detect QRS peaks using Pan-Tompkins algorithm."""
        # Validate input is 1D
        if signal.ndim != 1:
            raise ValueError(f"Expected 1D signal. Got shape: {signal.shape}")
        
        # Preprocess
        filtered = self.bandpass_filter(signal)
        differentiated = np.diff(filtered, prepend=0)
        squared = np.square(differentiated)
        
        # Moving average
        window_size = int(0.15 * self.sampling_rate)  # 150ms window
        moving_avg = np.convolve(squared, np.ones(window_size)/window_size, mode='same')
        
        # Thresholding
        threshold = 0.5 * np.max(moving_avg)
        peaks = np.where(moving_avg > threshold)[0]
        logger.info(f"Detected {len(peaks)} QRS peaks")
        return peaks