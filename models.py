import random

class AIModel:
    def __init__(self, name):
        self.name = name


def streak_ai(data):
    last = data[0]
    count = 0
    for d in data:
        if d == last:
            count += 1
        else:
            break

    if count >= 2:
        return "BIG" if last == "SMALL" else "SMALL"
    return last


def probability_ai(data):
    big = data[:20].count("BIG")
    small = data[:20].count("SMALL")
    return "BIG" if big < small else "SMALL"


def momentum_ai(data):
    return max(set(data[:5]), key=data[:5].count)


def anti_streak_ai(data):
    last3 = data[:3]
    if last3.count(last3[0]) == 3:
        return "BIG" if last3[0] == "SMALL" else "SMALL"
    return data[0]


def hybrid_ai(data):
    return random.choice([
        streak_ai(data),
        probability_ai(data),
        momentum_ai(data)
    ])


def generate_models():
    names = ["AlphaCore","NeuroNet","QuantumAI","DeepLogic","PatternX"]
    strategies = [streak_ai, probability_ai, momentum_ai, anti_streak_ai, hybrid_ai]

    models = []

    for name, strat in zip(names, strategies):
        m = AIModel(name)

        def predict(data, strat=strat):
            return {
                "prediction": strat(data),
                "confidence": random.randint(60, 85)
            }

        m.predict = predict
        models.append(m)

    return models