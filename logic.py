from formulas import formulas

CHOICE_TYPES = {"multiple", "yesno"}

def normalize_weights(weights):
    total = sum(weights.values())
    if total == 0:
        return weights
    return {k: v / total for k, v in weights.items()}


def parse_value(value, qtype):
    if qtype in CHOICE_TYPES:
        return value
    try:
        return float(value)
    except:
        return 0.0


def score_from_scale(value, scale):
    for min_val, max_val, score in scale:
        if min_val < value <= max_val:
            return float(score)
    return 1


def score_from_options(value, scoring_rules):
    for rule in scoring_rules or []:
        if str(rule.get("option")).upper() == str(value).upper():
            return float(rule.get("score", 0))
    return 0


def score_from_rules(value, scoring_rules):
    for rule in scoring_rules:
        cond = rule.get("condition")
        limit = rule.get("value")

        if cond == "direct":
            return int(value)
        if cond == ">" and value > limit:
            return rule.get("score", 0)
        if cond == ">=" and value >= limit:
            return rule.get("score", 0)
        if cond == "<" and value < limit:
            return rule.get("score", 0)
        if cond == "<=" and value <= limit:
            return rule.get("score", 0)
        if cond == "==" and value == limit:
            return rule.get("score", 0)
        if cond == "else":
            return rule.get("score", 0)

    return 0


def calculate_score(value, scoring_rules=None, qtype=None, scale=None):

    if scale:
        return score_from_scale(value, scale)

    if qtype in CHOICE_TYPES:
        return score_from_options(value, scoring_rules)

    if not scoring_rules:
        try:
            return int(value)
        except:
            return 0

    return score_from_rules(value, scoring_rules)


def apply_derived(score_lookup, formulas):
    results = []

    for dq in formulas:
        func = dq.get("func")
        if not func:
            continue

        try:
            val = func(score_lookup)
            score = calculate_score(val, scale=dq.get("scale"))
        except Exception:
            score = 1

        result = {
            "id": dq["id"],
            "score": float(score),
            "category": dq.get("category", "unknown"),
            "ignore_from_total": dq.get("ignore_from_total", False)
        }

        results.append(result)
        score_lookup[dq["id"]] = score

    return results


def calculate_results(questions, scores, weights=None):
    weights = normalize_weights(weights or {})

    totals = {}
    counts = {}

    score_lookup = {entry.get("id"): entry.get("score", 0) for entry in scores}

    for answer in scores:
        if answer.get("ignore_from_total"):
            continue

        cat = answer.get("category", "unknown")
        try:
            score_val = float(answer.get("score", 0))
        except:
            score_val = 0

        totals[cat] = totals.get(cat, 0) + score_val
        counts[cat] = counts.get(cat, 0) + 1

    derived_scores = apply_derived(score_lookup, formulas)

    for entry in derived_scores:
        cat = entry["category"]
        score = entry["score"]

        totals[cat] = totals.get(cat, 0) + score
        counts[cat] = counts.get(cat, 0) + 1

    averages = {
        cat: round(totals[cat] / counts[cat], 2)
        for cat in totals if counts[cat] > 0
    }

    weighted_total = round(
        sum(averages.get(cat, 0) * weights.get(cat, 0) for cat in averages),
        2
    )

    return averages, weighted_total


def process_answer(session, request, questions):
    q = questions[session["index"]]

    value = request.form.get("score", "0")
    qtype = q.get("type", "number")
    category = q.get("category", "unknown")

    parsed_value = parse_value(value, qtype)

    score = calculate_score(
        parsed_value,
        scoring_rules=q.get("scoring"),
        qtype=qtype,
        scale=q.get("scale")
    )

    print(f"Spørsmål: {q.get('text')} | Input: {parsed_value} | Score: {score}")

    session["scores"].append({
        "id": q.get("id"),
        "score": score,
        "category": category,
        "type": qtype,
        "ignore_from_total": q.get("ignore_from_total", False)
    })

    follow_ups = q.get("follow_up", [])
    if follow_ups and str(value).lower() in ["1", "ja"]:
        questions[session["index"] + 1:session["index"] + 1] = follow_ups

    session["index"] += 1


def calculate_derived(session, formulas):
    score_lookup = {e["id"]: e["score"] for e in session.get("scores", [])}

    derived_scores = apply_derived(score_lookup, formulas)

    session["scores"].extend(derived_scores)
