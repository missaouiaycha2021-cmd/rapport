"""
Script Final - Version 38 Métriques (État avant simplification)
"""

import numpy as np
import joblib
import json
import sys

MODEL_PATH = 'models/isolation_forest_model.pkl'
SCALER_PATH = 'models/scaler.pkl'

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

THRESHOLD = 0.08   # Seuil ajusté

def predict_anomaly(metrics):
    if len(metrics) != 38:
        return {"status": "ERROR", "message": "38 métriques requises"}

    cpu_avg = np.mean(metrics[0:4])
    ram = metrics[5]
    disk = metrics[22] if len(metrics) > 22 else 0.0

    reasons = []
    if ram > 0.93:
        reasons.append("Saturation RAM critique")
    elif ram > 0.90:
        reasons.append("RAM proche de la saturation")

    if cpu_avg > 0.75:
        reasons.append("Charge CPU élevée")

    if disk > 0.85:
        reasons.append("Utilisation disque élevée")

    # Fenêtre temporelle
    window = np.tile(metrics, (60, 1))
    window_flat = window.reshape(1, -1)
    window_scaled = scaler.transform(window_flat)

    score = model.decision_function(window_scaled)[0]

    if score < THRESHOLD or len(reasons) > 0:
        status = "ANOMALIE"
        message = " | ".join(reasons) if reasons else "Risque détecté"
    else:
        status = "NORMAL"
        message = "Comportement normal"

    return {
        "status": status,
        "message": message,
        "score": round(float(score), 4),
        "ram_usage": round(float(ram), 4),
        "cpu_usage": round(float(cpu_avg), 4)
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            metrics = [float(x) for x in sys.argv[1:39]]
            result = predict_anomaly(metrics)
            print(json.dumps(result))
        except:
            print(json.dumps({"status": "ERROR", "message": "Invalid input"}))
    else:
        print("=== MODE TEST - 38 MÉTRIQUES ===\n")
        
        normal = [0.06] * 38
        print("Normal :", predict_anomaly(normal))

        ram_high = [0.06] * 5 + [0.97] + [0.06] * 32
        print("Saturation RAM :", predict_anomaly(ram_high))

        cpu_high = [0.80] * 4 + [0.06] * 1 + [0.85] + [0.06] * 32
        print("Charge CPU élevée :", predict_anomaly(cpu_high))

        print("\nUtilisation : python src/predict_anomaly.py <val1> <val2> ... <val38>")
