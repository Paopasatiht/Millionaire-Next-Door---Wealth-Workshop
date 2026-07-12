def calc_expected_nw(age: int, annual_income: float) -> float:
    return (age * annual_income) / 10


def calc_multiplier(actual: float, expected: float) -> float:
    if not expected:
        return 0.0
    return round(actual / expected, 2)


def get_paw_status(actual: float, expected: float) -> dict:
    m = calc_multiplier(actual, expected)
    if m >= 2:
        label, css = "PAW", "paw"
    elif m >= 0.5:
        label, css = "AAW", "aaw"
    else:
        label, css = "UAW", "uaw"
    return {"label": label, "css": css, "multiplier": m}


def calc_savings_rate(income: float, expenses: float) -> float:
    if not income:
        return 0.0
    return round((income - expenses) / income * 100, 1)
