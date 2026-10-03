# M.I.N.D.A.S. - Metacognitive Integrated Neural Dynamic Agent System
# Data Pipeline Engine (Multimodal Cleaning & Feature Preprocessing)

import re
import numpy as np
import pandas as pd

class MindasDataPipeline:
    def __init__(self, target_tensor_dim: int = 512):
        self.target_tensor_dim = target_tensor_dim
        print("[M.I.N.D.A.S. Data Pipeline] Initialized Data Preprocessing Engine.")

    # 1. Text Data Cleaning & Vectorization
    def clean_and_vectorize_text(self, raw_text: str) -> np.ndarray:
        """
        Cleans raw unstructured text input and converts it into a normalized feature vector.
        """
        # Clean special characters, links, and extra spaces
        text_cleaned = re.sub(r'http\S+|www\S+|[^a-zA-Z0-9\s]', '', raw_text)
        text_cleaned = text_cleaned.lower().strip()
        
        # Simple ASCII token encoding simulation
        tokens = [ord(char) for char in text_cleaned]
        
        # Normalize and pad/crop array to fit target tensor dimensions
        feature_vector = np.zeros(self.target_tensor_dim, dtype=np.float32)
        length = min(len(tokens), self.target_tensor_dim)
        
        if length > 0:
            feature_vector[:length] = np.array(tokens[:length], dtype=np.float32) / 255.0

        print(f"[Data Pipeline - Text] Cleaned Input Length: {len(text_cleaned)} chars.")
        return feature_vector

    # 2. Audio Signal Processing & Feature Extraction
    def process_audio_features(self, raw_audio_waveform: np.ndarray, sample_rate: int = 16000) -> np.ndarray:
        """
        Cleans raw audio waveform, normalizes amplitude, and extracts frequency-like signals using NumPy.
        """
        if raw_audio_waveform.size == 0:
            return np.zeros(self.target_tensor_dim, dtype=np.float32)

        # Remove DC offset and normalize amplitude [-1.0, 1.0]
        audio_cleaned = raw_audio_waveform - np.mean(raw_audio_waveform)
        max_val = np.max(np.abs(audio_cleaned))
        if max_val > 0:
            audio_cleaned = audio_cleaned / max_val

        # Resample / Slice to fit target tensor size
        if len(audio_cleaned) > self.target_tensor_dim:
            processed_vector = audio_cleaned[:self.target_tensor_dim]
        else:
            processed_vector = np.pad(audio_cleaned, (0, self.target_tensor_dim - len(audio_cleaned)), 'constant')

        print(f"[Data Pipeline - Audio] Processed audio signal array with size: {processed_vector.shape}")
        return processed_vector.astype(np.float32)

    # 3. Image Tensor Processing (Camera / Visual Inputs)
    def process_image_tensor(self, raw_image_array: np.ndarray) -> np.ndarray:
        """
        Normalizes multi-channel RGB image matrices into standardized float32 tensors.
        """
        # Ensure array is floating point and scale pixel values to range [0.0, 1.0]
        normalized_img = raw_image_array.astype(np.float32) / 255.0
        
        # Flatten and resize to core tensor dimension
        flattened = normalized_img.flatten()
        if len(flattened) >= self.target_tensor_dim:
            image_features = flattened[:self.target_tensor_dim]
        else:
            image_features = np.pad(flattened, (0, self.target_tensor_dim - len(flattened)), 'constant')

        print(f"[Data Pipeline - Image] Flattened & Normalized Image Features with shape: {image_features.shape}")
        return image_features

    # 4. Multimodal Data Fusion (Pandas Integration)
    def create_multimodal_dataset(self, text_samples: list, audio_features: list) -> pd.DataFrame:
        """
        Combines disparate data sources into a structured Pandas DataFrame pipeline.
        """
        data = {
            "text_raw": text_samples,
            "audio_signal_mean": [np.mean(a) for a in audio_features],
            "text_feature_vector": [self.clean_and_vectorize_text(t) for t in text_samples]
        }
        df = pd.DataFrame(data)
        print("[Data Pipeline - Pandas] Multimodal DataFrame constructed successfully:")
        print(df[["text_raw", "audio_signal_mean"]].head())
        return df


# Test Execution Engine
if __name__ == "__main__":
    print("--------------------------------------------------")
    print(" Initializing M.I.N.D.A.S. Data Pipeline Module   ")
    print("--------------------------------------------------")

    pipeline = MindasDataPipeline(target_tensor_dim=512)

    # 1. Clean Raw Text Input
    sample_text = "Hello! User is feeling sad/stressed today. Need empathetic agent response... @123"
    text_vector = pipeline.clean_and_vectorize_text(sample_text)

    # 2. Process Raw Audio Array Simulation
    simulated_audio = np.random.uniform(-0.8, 0.8, 1000)
    audio_vector = pipeline.process_audio_features(simulated_audio)

    # 3. Process Raw Camera Frame Array Simulation (RGB Image 64x64x3)
    simulated_image = np.random.randint(0, 256, (64, 64, 3))
    image_vector = pipeline.process_image_tensor(simulated_image)

    # 4. Create Pandas Multimodal Pipeline
    df = pipeline.create_multimodal_dataset([sample_text], [simulated_audio])