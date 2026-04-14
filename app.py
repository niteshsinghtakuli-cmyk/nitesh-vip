from flask import Flask, render_template, request, redirect
from fetch import get_data
from models import generate_models
from tracker import *

import time
import random

app = Flask(__name__)

last_prediction = None
last_result = None
last_period = None
last_confidence = 0
last_update_time = 0


def invert(p):
    return "BIG" if p == "SMALL" else "SMALL"


# 🔥 PATTERN MEMORY
def pattern_memory(results):
    last20 = results[:20]
    big = last20.count("BIG")
    small = last20.count("SMALL")

    return "BIG" if big > small else "SMALL"


# 🔥 ADAPTIVE BIAS
def adaptive_bias(results):
    last100 = results[:100]
    big = last100.count("BIG")
    small = last100.count("SMALL")

    if big > small:
        return "BIG"
    elif small > big:
        return "SMALL"
    return None


# 🔥 ENTRY FILTER
def entry_filter(results, confidence):
    if results[:4].count(results[0]) == 4:
        return False
    if confidence < 55:
        return False
    return True


# 🧠 MAIN AI
def head_ai(predictions, ai_results, results):
    votes = {"BIG": 0, "SMALL": 0}

    for p, ai in zip(predictions, ai_results):
        weight = get_ai_weight(ai["name"])
        votes[p["prediction"]] += p["confidence"] * weight

    total = sum(votes.values())
    if total == 0:
        return "SKIP", 0

    final = "BIG" if votes["BIG"] > votes["SMALL"] else "SMALL"
    confidence = max(votes.values()) / total * 100

    # 🔥 APPLY MEMORY
    mem = pattern_memory(results)
    bias = adaptive_bias(results)

    if random.random() < 0.6:
        final = mem

    if bias and random.random() < 0.5:
        final = bias

    if not entry_filter(results, confidence):
        return "SKIP", confidence

    return final, round(confidence, 2)


@app.route("/")
def home():
    global last_prediction, last_result, last_period, last_confidence, last_update_time

    results, periods, _ = get_data()
    models = generate_models()

    predictions = []
    ai_results = []

    for m in models:
        p = m.predict(results)
        predictions.append(p)
        ai_results.append({"name": m.name, **p})

    current_period = periods[0]
    actual = results[0]
    now = time.time()

    if last_period != current_period or now - last_update_time > 35:

        if last_prediction and last_prediction != "SKIP":
            last_result = "WIN" if last_prediction == actual else "LOSS"
            update_history(current_period, last_prediction, actual, ai_results)
        else:
            last_result = "SKIP"

        final, conf = head_ai(predictions, ai_results, results)

        if last_result == "LOSS" and final != "SKIP":
            if random.random() < 0.5:
                final = invert(final)

        last_prediction = final
        last_confidence = conf
        last_period = current_period
        last_update_time = now

    else:
        final = last_prediction
        conf = last_confidence

    next_period = str(int(current_period) + 1)

    wins, losses, accuracy = get_stats()
    action = "BET" if should_bet(final) else "SKIP"

    # 🔥 STREAK
    streak = 0
    last_type = None

    for h in history_store:
        if h["result"] in ["WIN", "LOSS"]:
            if last_type is None:
                last_type = h["result"]
                streak = 1
            elif h["result"] == last_type:
                streak += 1
            else:
                break

    # 🔥 SIGNAL
    if action == "BET" and conf >= 65:
        signal = "STRONG"
    elif action == "BET":
        signal = "NORMAL"
    else:
        signal = "SKIP"

    level, bet_amount, balance = get_status()

    return render_template(
        "index.html",
        ai_results=ai_results,
        final=final,
        confidence=conf,
        next_period=next_period,
        history=history_store,
        wins=wins,
        losses=losses,
        accuracy=accuracy,
        action=action,
        last_result=last_result,
        level=level,
        bet_amount=bet_amount,
        balance=balance,
        streak=streak,
        streak_type=last_type,
        signal=signal
    )


@app.route("/set_balance", methods=["POST"])
def set_balance_route():
    amount = int(request.form.get("balance"))
    set_balance(amount)
    return redirect("/")


@app.route("/bet", methods=["POST"])
def bet_route():
    place_bet()
    return redirect("/")


if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)