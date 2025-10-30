from app.models.livestock_measurement import LivestockMorphometrics

model = LivestockMorphometrics()

def analyze_livestock_image(image_path: str, reference_object_area: float = None):
    """Analyze a single livestock image"""
    detections = model.detect_livestock(image_path)
    if not detections:
        return {"error": "No livestock detected"}

    detection = detections[0]
    features = model.extract_morphometric_features(detection, reference_object_area)
    if "error" in features:
        return features

    # Optional: estimate weight (you can refine later)
    if reference_object_area:
        weight_est = estimate_weight(features)
        features["estimated_weight_kg"] = weight_est

    return features


def estimate_weight(features):
    """Basic weight estimation formula"""
    if "body_length_cm" in features and "heart_girth_cm" in features:
        L = features["body_length_cm"]
        G = features["heart_girth_cm"]
        weight = (G ** 2 * L) / 300  # Example empirical formula
        return round(weight, 2)
    return None
