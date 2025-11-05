import tensorflow as tf
from tensorflow.keras.preprocessing import image # pyright: ignore[reportMissingImports]
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input # pyright: ignore[reportMissingImports]

import numpy as np
class SpoilagePredictionModel:
    def __init__(self,model_path):
        self.model = tf.keras.models.load_model(model_path)
        self.class_names = ["overripe","ripe","rotten","unripe"]
        self.rsl = {
            "unripe":  (8.0, 12.0),   # days until unfit (min, max)
            "ripe":    (3.0, 5.0),
            "overripe":(1.0, 2.0),
            "rotten":  (0.0, 1.0)
        }
    
    def __predict_stage(self,img_path):
        """Takes input image path as input and outputs one of [overrope, ripe, rotten, unripe] as pred_class"""
        
        # --- Load and preprocess image ---
        img = image.load_img(img_path, target_size=(224, 224))  # MobileNetV2 input size
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # --- Predict ---
        logits = self.model.predict(img_array)           # raw outputs
        probs = tf.nn.softmax(logits).numpy()          # convert to probabilities
        pred_class = self.class_names[np.argmax(probs)]
        confidence = np.max(probs) * 100

    
        # --- Display image and result ---
        # plt.imshow(image.load_img(img_path))
        # plt.axis('off')
        # plt.title(f"Predicted: {pred_class}")
        # plt.show()

        return pred_class 
    
    def get_shelf_life(self,image_path: str, temp_c: float = 25.0, humidity_pct: float = 60.0, ethylene_ppm: float = 0.0):
        
        stage = self.__predict_stage(image_path)

        if stage not in self.rsl:
            raise ValueError(f"Unknown stage: {stage}")

        low_base, high_base = self.rsl[stage]
        median_base = (low_base + high_base) / 2.0

        # Temperature (Q10 scaling)
        q10 = 2 ** ((temp_c - 25) / 10)
        temp_factor = 1 / q10

        # Continuous humidity adjustment
        humidity_factor = 1 - 0.002 * (humidity_pct - 60)
        humidity_factor = np.clip(humidity_factor, 0.9, 1.1)

        # Continuous ethylene adjustment (exponential)
        k = 0.4  # sensitivity constant
        ethylene_factor = np.exp(-k * ethylene_ppm)

        # Combine
        combined_multiplier = temp_factor * humidity_factor * ethylene_factor

        low_adj = max(0.0, low_base * combined_multiplier)
        high_adj = max(0.0, high_base * combined_multiplier)
        median_adj = (low_adj + high_adj) / 2

        return {
            "stage":stage,
            "min_days": int(round(low_adj, 2)),
            "max_days": int(round(high_adj, 2)),
            "median_days": int(round(median_adj, 2)),
            "combined_multiplier": round(combined_multiplier, 3),
            # "notes": (f"temp_factor={temp_factor:.3f}, "
            #         f"humidity_factor={humidity_factor:.3f}, "
            #         f"ethylene_factor={ethylene_factor:.3f}"),
            "input":{
                "temperature":temp_c,
                "humidity":humidity_pct,
                "ethylene":ethylene_ppm
            }
        }
        # return {
        #     "stage":"unripe",
        #     "image":image_path,
        #     "min_days": int(round(8, 2)),
        #     "max_days": int(round(12, 2)),
        #     "median_days": int(round(10, 2)),
        #     "combined_multiplier": round(1, 3),
        #     "notes": (f"temp_factor={1:.3f}, "
        #             f"humidity_factor={1:.3f}, "
        #             f"ethylene_factor={1:.3f}")
        # }
