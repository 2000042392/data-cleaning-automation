"""generate_data.py — Creates a realistic messy sales dataset."""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)
np.random.seed(42)

BASE = Path(__file__).parent.parent

n = 300
regions = ["North","South","East","West","north","SOUTH","East "," West"]
products = ["Laptop","Tablet","Phone","Monitor","Headphones","laptop","TABLET","Phone "]
statuses = ["Completed","Pending","Cancelled","completed","PENDING",None]
sales_reps = ["Alice","Bob","Charlie","Diana","Eve",None,"alice","BOB"]

start_date = datetime(2024,1,1)
dates = [start_date + timedelta(days=random.randint(0,364)) for _ in range(n)]
for i in random.sample(range(n), 10):
    dates[i] = None

order_ids = [f"ORD-{1000+i}" for i in range(n)]
# duplicates
dup_indices = random.sample(range(n), 15)
order_ids += [order_ids[i] for i in dup_indices]
dates      += [dates[i] for i in dup_indices]

revenue  = np.round(np.random.uniform(100,5000,n),2).tolist()
for i in random.sample(range(n),8):
    revenue[i] = np.random.choice([None,-999,99999])
revenue += [revenue[i] for i in dup_indices]

quantity  = np.random.randint(1,20,n).tolist()
for i in random.sample(range(n),6):
    quantity[i] = None
quantity += [quantity[i] for i in dup_indices]

total = len(order_ids)
df = pd.DataFrame({
    "order_id":        order_ids,
    "date":            dates,
    "region":          [random.choice(regions) for _ in range(total)],
    "product":         [random.choice(products) for _ in range(total)],
    "sales_rep":       [random.choice(sales_reps) for _ in range(total)],
    "quantity":        quantity,
    "revenue":         revenue,
    "status":          [random.choice(statuses) for _ in range(total)],
    "discount_%":      np.round(np.random.uniform(0,30,total),1),
    "customer_rating": [round(random.uniform(1,5),1) if random.random()>0.1 else None for _ in range(total)],
})

out = BASE / "data" / "raw_sales_data.csv"
df.to_csv(out, index=False)
print(f"✓ Generated {len(df)} rows → {out}")
print(f"  Nulls: {df.isnull().sum().sum()}  |  Dup order_ids: {df['order_id'].duplicated().sum()}")
