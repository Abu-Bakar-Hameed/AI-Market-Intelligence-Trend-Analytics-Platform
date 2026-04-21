# growth_trend.py
from process.daily_counts import daily_counts

async def growth_trend():
    data = await daily_counts()  

    sorted_days = sorted(data.items())

    trend = []

    for i in range(1, len(sorted_days)):
        prev = sorted_days[i - 1][1]
        curr = sorted_days[i][1]

        growth = ((curr - prev) / prev * 100) if prev else 0

        trend.append({
            "day": sorted_days[i][0],
            "growth_percent": round(growth, 2)
        })

    return trend
