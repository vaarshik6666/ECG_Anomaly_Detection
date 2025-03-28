import os
import wfdb
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_ecg_data(sample_length=1000):
    record_name = 'mitdb/100'
    data_dir = 'mitdb'

    required_files = [f'{data_dir}/100.hea', f'{data_dir}/100.dat']
    if not all(os.path.isfile(f) for f in required_files):
        logger.warning("Downloading missing dataset files...")
        try:
            wfdb.dl_database('mitdb', dl_dir=data_dir, records=['100'])
        except Exception as e:
            logger.error(f"Download failed: {str(e)}")
            raise
    try:
        record = wfdb.rdrecord(record_name, sampto=sample_length)
        signal = record.p_signal[:, 0].flatten()
        logger.info(f"Loaded ECG signal (shape: {signal.shape})")
        return signal, record.fs
    except Exception as e:
        logger.error(f"Data loading error: {str(e)}")
        raise