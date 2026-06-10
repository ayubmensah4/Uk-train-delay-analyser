import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

OPERATORS = [
    "Avanti West Coast", "LNER", "Great Western Railway",
    "South Western Railway", "Thameslink", "Southern",
    "CrossCountry", "TransPennine Express", "Chiltern Railways"
]

ROUTES = [
    ("London Paddington",   "Bristol Temple Meads"),
    ("London Euston",       "Manchester Piccadilly"),
    ("London Kings Cross",  "Leeds"),
    ("London Waterloo",     "Southampton Central"),
    ("London Victoria",     "Gatwick Airport"),
    ("Birmingham New St",   "London Euston"),
    ("Manchester Piccadilly","Leeds"),
    ("London Paddington",   "Cardiff Central"),
    ("Edinburgh Waverley",  "Glasgow Central"),
]

OPERATOR_MAP = {
    "London Paddington":    "Great Western Railway",
    "London Euston":        "Avanti West Coast",
    "London Kings Cross":   "LNER",
    "London Waterloo":      "South Western Railway",
    "London Victoria":      "Southern",
    "Birmingham New St":    "Avanti West Coast",
    "Manchester Piccadilly":"TransPennine Express",
    "Edinburgh Waverley":   "LNER",
}

def generate_delays(n_records: int = 5000) -> pd.DataFrame:
    rows = []
    start_date = datetime(2024, 1, 1)

    for _ in range(n_records):
        origin, destination = random.choice(ROUTES)
        operator = OPERATOR_MAP.get(origin, random.choice(OPERATORS))
        date = start_date + timedelta(days=random.randint(0, 365))
        hour = random.choices(
            range(24),
            # Peak hours (7-9, 17-19) more likely
            weights=[1,1,1,1,1,1,2,5,5,3,2,2,2,2,2,2,3,5,5,3,2,2,1,1],
            k=1
        )[0]
        scheduled = f"{hour:02d}{random.choice(['00','15','30','45'])}"

        # Delays follow a realistic distribution
        # Most trains on time, long tail of delays
        delay = max(0, int(np.random.exponential(scale=4)))
        if random.random() < 0.03:   # 3% chance of big delay
            delay += random.randint(20, 90)

        cancelled = random.random() < 0.02  # 2% cancellation rate
        if cancelled:
            delay = 0

        rows.append({
            "origin":             origin,
            "destination":        destination,
            "operator":           operator,
            "date":               date.strftime("%Y-%m-%d"),
            "hour":               hour,
            "month":              date.month,
            "day_of_week":        date.strftime("%A"),
            "scheduled_departure": scheduled,
            "mins_late":          delay,
            "cancelled":          cancelled,
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_delays(5000)
    df.to_csv("data/cleaned_delays.csv", index=False)

    print(f"Generated {len(df):,} records")
    print(f"Average delay:      {df['mins_late'].mean():.1f} mins")
    print(f"Cancellation rate:  {df['cancelled'].mean()*100:.1f}%")
    print(f"Date range:         {df['date'].min()} to {df['date'].max()}")
    print(f"\nDelay by operator:")
    print(df.groupby("operator")["mins_late"].mean().sort_values(ascending=False).round(1))