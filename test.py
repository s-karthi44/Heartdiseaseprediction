import joblib
import pandas as pd

model = joblib.load("models/heart_model.pkl")
encoders = joblib.load("models/heart_encoders.pkl")

sample = pd.DataFrame({
    "Age":[63],
    "Sex":["M"],
    "ChestPainType":["ASY"],
    "RestingBP":[145],
    "Cholesterol":[233],
    "FastingBS":[1],
    "RestingECG":["Normal"],
    "MaxHR":[150],
    "ExerciseAngina":["N"],
    "Oldpeak":[2.3],
    "ST_Slope":["Flat"]
})

for col in ["Sex","ChestPainType","RestingECG","ExerciseAngina","ST_Slope"]:
    sample[col] = encoders[col].transform(sample[col])

print(sample)
print(model.predict(sample))
print(model.predict_proba(sample))