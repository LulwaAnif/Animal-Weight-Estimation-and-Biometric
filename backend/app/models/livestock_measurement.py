import cv2
import numpy as np
import torch
from ultralytics import YOLO
from scipy import ndimage
from skimage import morphology
import warnings

warnings.filterwarnings("ignore")


class LivestockMorphometrics:
    def __init__(self):
        """Initialize YOLOv8 segmentation model for livestock detection"""
        print("🐄 Loading YOLOv8 model...")
        self.model = YOLO("yolov8n-seg.pt")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.livestock_classes = {
            15: "cat", 16: "dog", 17: "horse", 18: "sheep",
            19: "cow", 20: "elephant", 21: "bear", 22: "zebra", 23: "giraffe"
        }
        print("✅ Model loaded successfully")

    def enhance_image(self, image):
        """Enhance contrast and edges for better segmentation"""
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        enhanced = cv2.filter2D(enhanced, -1, kernel)
        return cv2.GaussianBlur(enhanced, (3, 3), 0)

    def detect_livestock(self, image_path, conf_threshold=0.25):
        """Detect livestock and return segmentation mask"""
        original = cv2.imread(image_path)
        original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        enhanced = self.enhance_image(original)
        results = self.model.predict(source=enhanced, conf=conf_threshold, verbose=False)

        detections = []
        for result in results:
            if result.masks is None:
                continue
            for box, mask, conf, cls in zip(
                result.boxes.xyxy, result.masks.data, result.boxes.conf, result.boxes.cls
            ):
                class_id = int(cls.item())
                if class_id in self.livestock_classes:
                    mask_np = mask.cpu().numpy()
                    binary_mask = (mask_np > 0.5).astype(np.uint8)
                    detections.append({
                        "class_name": self.livestock_classes[class_id],
                        "confidence": conf.item(),
                        "mask": binary_mask,
                        "original_image": original,
                    })
        return detections

    def extract_morphometric_features(self, detection, reference_object_area=None):
        """Extract key body measurements in pixels and cm"""
        mask = detection["mask"]
        img = detection["original_image"]

        cleaned = morphology.remove_small_objects(mask.astype(bool), min_size=100)
        cleaned = ndimage.binary_fill_holes(cleaned).astype(np.uint8)
        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return {"error": "No contour found"}

        contour = max(contours, key=cv2.contourArea)
        features = self._calculate_measurements(contour)

        if reference_object_area:
            ratio = reference_object_area / features["body_length_px"]
            for key in ["body_length", "withers_height", "heart_girth", "hip_length"]:
                features[f"{key}_cm"] = features[f"{key}_px"] * ratio
            features["pixel_to_cm_ratio"] = ratio

        return features

    def _calculate_measurements(self, contour):
        """Compute morphometric parameters in pixels"""
        left = tuple(contour[contour[:, :, 0].argmin()][0])
        right = tuple(contour[contour[:, :, 0].argmax()][0])
        top = tuple(contour[contour[:, :, 1].argmin()][0])
        bottom = tuple(contour[contour[:, :, 1].argmax()][0])

        def distance(p1, p2): return np.linalg.norm(np.array(p1) - np.array(p2))

        return {
            "body_length_px": distance(left, right),
            "withers_height_px": distance(top, bottom),
            "heart_girth_px": distance((left[0], top[1]), (left[0], bottom[1])) * 0.8,
            "hip_length_px": distance((right[0], top[1]), (right[0], bottom[1])) * 0.7,
            "contour_area_px2": cv2.contourArea(contour),
            "contour_perimeter_px": cv2.arcLength(contour, True),
        }
