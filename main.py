from fetch import get_results
from models import generate_models


def head_ai(predictions):
    votes = {"BIG": 0, "SMALL": 0}

    for p in predictions:
        votes[p["prediction"]] += p["confidence"]

    final = "BIG" if votes["BIG"] > votes["SMALL"] else "SMALL"

    total = votes["BIG"] + votes["SMALL"]
    confidence = (max(votes.values()) / total) * 100

    return final, round(confidence, 2)


def main():
    data = get_results()

    models = generate_models()
    predictions = []

    print("\n=========== WINGO AI (BIG/SMALL) ===========\n")

    for model in models:
        result = model.predict(data)
        predictions.append(result)

        print(f"{model.name:<10} → {result['prediction']} ({result['confidence']}%)")

    final, conf = head_ai(predictions)

    print("\n-------------------------------------------")
    print(f"HEAD AI   → {final} ({conf}%)")

    if conf < 55:
        print("ACTION    → SKIP")
    else:
        print("ACTION    → BET")


if __name__ == "__main__":
    main()