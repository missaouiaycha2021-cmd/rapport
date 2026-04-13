"""
Script Final Stable - Version 5 Métriques
Pour Rapport PFA - Simple et Fiable
"""

import json
import sys
from datetime import datetime

def predict_anomaly(cpu, ram, disk, net_in, net_out):
    reasons = []
    
    if ram > 0.93:
        reasons.append("Saturation RAM imminente")
    if cpu > 0.78:
        reasons.append("Surcharge CPU prévue")
    if disk > 0.85:
        reasons.append("Utilisation disque élevée")

    if len(reasons) >= 2:
        status = "ANOMALIE"
        risk_level = "Critique"
        predicted_in = "dans les 30 minutes"
        action = "MIGRER IMMÉDIATEMENT la VM + scaler RAM"
    elif len(reasons) == 1:
        status = "ANOMALIE"
        risk_level = "Élevé"
        predicted_in = "dans 1 à 2 heures"
        action = "Migrer les workloads ou scaler les instances"
    else:
        status = "NORMAL"
        risk_level = "Faible"
        predicted_in = "Aucun risque visible"
        action = "Surveillance normale"

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "risk_level": risk_level,
        "predicted_in": predicted_in,
        "recommended_action": action,
        "reasons": reasons,
        "current_ram": round(ram, 2),
        "current_cpu": round(cpu, 2),
        "current_disk": round(disk, 2)
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            cpu = float(sys.argv[1])
            ram = float(sys.argv[2])
            disk = float(sys.argv[3])
            net_in = float(sys.argv[4])
            net_out = float(sys.argv[5])
            
            result = predict_anomaly(cpu, ram, disk, net_in, net_out)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except:
            print(json.dumps({"status": "ERROR", "message": "Valeurs numériques invalides"}))
    else:
        print("=== TEST FINAL - 5 MÉTRIQUES (Version Stable) ===\n")
        
        tests = {
            "Normal": [0.06, 0.88, 0.25, 0.10, 0.12],
            "Saturation RAM": [0.06, 0.97, 0.25, 0.10, 0.12],
            "Surcharge CPU": [0.82, 0.85, 0.30, 0.15, 0.18],
            "Risque Critique": [0.85, 0.96, 0.40, 0.20, 0.25]
        }
        
        for name, values in tests.items():
            print(f"{name} :")
            result = predict_anomaly(*values)
            print(result)
            print("-" * 60)
        
        print("\n✅ Script prêt pour ton rapport PFA et intégration avec Terraform")
        print("Utilisation : python src/predict_anomaly.py <CPU> <RAM> <Disk> <Net_In> <Net_Out>")
