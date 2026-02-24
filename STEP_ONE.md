### STEP 1: DATA DESIGN (Foundational Layer of the Project)

This project does **not require external market datasets**. It is a parametric numerical simulation model. Therefore, “data” here means **model inputs and computational structures**, not CSV files.

You must define structured, reproducible input parameters.

---

## 1. Required Input Parameters (Core Model Inputs)

These are scalar numerical inputs supplied through Streamlit UI:

| Parameter                 | Symbol | Type   | Description                         |
| ------------------------- | ------ | ------ | ----------------------------------- |
| Initial Stock Price       | S₀     | float  | Current underlying asset price      |
| Strike Price              | K      | float  | Option strike                       |
| Risk-Free Rate            | r      | float  | Annual continuously compounded rate |
| Volatility                | σ      | float  | Annualized standard deviation       |
| Time to Maturity          | T      | float  | In years                            |
| Number of Steps           | N      | int    | Binomial tree depth                 |
| Option Type               | -      | string | “Call” or “Put”                     |
| Dividend Yield (optional) | q      | float  | Continuous dividend rate            |

These are the only required inputs for CRR implementation.

---

## 2. Internal Data Structures (Generated Data)

The model will internally generate:

### A. Time Step Size

[
\Delta t = \frac{T}{N}
]

### B. Up/Down Factors

[
u = e^{\sigma \sqrt{\Delta t}}
]
[
d = 1/u
]

### C. Risk-Neutral Probability

[
p = \frac{e^{(r-q)\Delta t} - d}{u - d}
]

---

## 3. Tree Data Structures

You will create two matrices:

1. **Stock Price Tree**
2. **Option Value Tree**

Dimensions:

```
(N+1) x (N+1)
```

Only lower triangle is used.

Example structure for N=3:

Stock Tree:

```
t=0:    S
t=1:    Su     Sd
t=2:    Suu    Sud    Sdd
t=3:    Suuu   Suud   Sudd   Sddd
```

Option Tree (backward induction):

```
Start at maturity → move backward
```

---

## 4. Convergence Data (Very Important)

To show convergence, you must generate:

```
steps_list = [10, 20, 30, ..., 1000]
price_list = []
```

For each N:

* Compute American option price
* Store result

This becomes your convergence dataset.

Final structure:

```python
convergence_data = {
    "steps": [...],
    "american_prices": [...],
    "european_prices": [...]
}
```

---

## 5. Suggested Default Values (For Demo)

Use stable baseline parameters:

* S₀ = 100
* K = 100
* r = 0.05
* σ = 0.2
* T = 1
* q = 0
* N = 100 (initial)

These avoid arbitrage instability.

---

## 6. What Files Need Data?

You will NOT use CSV.

Data is generated dynamically inside:

* pricing.py → core numerical generation
* app.py → convergence loop
* visualization.py → plotting data

No external datasets required.

---

## 7. Validation Checks (Important)

Before running pricing:

* Ensure `0 < p < 1`
* Ensure `N > 0`
* Ensure `T > 0`
* Ensure `σ > 0`

Otherwise, the model breaks numerically.

---

## 8. Final Data Flow Diagram

User Input → Parameter Validation →
Tree Construction → Backward Induction →
Store Convergence Results → Plot → Display

---

