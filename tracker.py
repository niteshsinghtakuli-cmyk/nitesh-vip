history_store = []

current_balance = 1000
martingale_level = 1
base_bet = 10

bet_active = False
last_bet_amount = 0

# 🔥 AI PERFORMANCE TRACK
ai_stats = {}


def set_balance(amount):
    global current_balance
    current_balance = amount


def get_bet_amount():
    return base_bet * (2 ** (martingale_level - 1))


def place_bet():
    global bet_active, last_bet_amount
    bet_active = True
    last_bet_amount = get_bet_amount()


def update_result(result):
    global current_balance, martingale_level, bet_active

    if not bet_active:
        return

    if result == "WIN":
        current_balance += last_bet_amount
        martingale_level = 1
    else:
        current_balance -= last_bet_amount
        martingale_level += 1
        if martingale_level > 3:
            martingale_level = 1

    bet_active = False


# 🔥 AI LEARNING
def update_ai_stats(ai_results, actual):
    for ai in ai_results:
        name = ai["name"]
        pred = ai["prediction"]

        if name not in ai_stats:
            ai_stats[name] = {"win": 0, "loss": 0}

        if pred == actual:
            ai_stats[name]["win"] += 1
        else:
            ai_stats[name]["loss"] += 1


def get_ai_weight(name):
    if name not in ai_stats:
        return 1

    win = ai_stats[name]["win"]
    loss = ai_stats[name]["loss"]

    total = win + loss
    return (win / total) * 2 if total > 0 else 1


def update_history(period, prediction, actual, ai_results):
    if history_store and history_store[0]["period"] == period:
        return history_store

    if prediction == "SKIP":
        result = "SKIP"
    else:
        result = "WIN" if prediction == actual else "LOSS"

    update_result(result)
    update_ai_stats(ai_results, actual)

    history_store.insert(0, {
        "period": period,
        "prediction": prediction,
        "actual": actual,
        "result": result,
        "balance": round(current_balance, 2),
        "level": martingale_level
    })

    return history_store[:100]


def get_stats():
    wins = sum(1 for h in history_store if h["result"] == "WIN")
    losses = sum(1 for h in history_store if h["result"] == "LOSS")

    total = wins + losses
    accuracy = (wins / total * 100) if total > 0 else 0

    return wins, losses, round(accuracy, 2)


def should_bet(pred):
    return pred != "SKIP"


def get_status():
    return martingale_level, get_bet_amount(), current_balance