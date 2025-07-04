# 📊 Option Pricing using Binomial Trees

This project implements a modular, object-oriented framework for pricing financial options using the **binomial tree method**. It supports European, American, and Barrier options using flexible and reusable components.

---

## 🗂️ Project Structure

├── models.py # Include Binomial model environment class with tree parameters
├── options.py # Classes to implement pricing for European, American, and Barrier options
├── README.md # Project documentation
└── .gitignore # Ignore compiled Python files, cache, and checkpoints

---

## ✨ Features

- ✅ Modular design using Python classes
- 📈 Supports:
  - European options
  - American options
  - Barrier options (up-and-in, up-and-out, down-and-in, down-and-out)
- ⚙️ Configurable parameters:
  - Number of steps
  - Up/down multipliers
  - Risk-free rate
  - Initial asset price

---

## ⚙️ Components

### `models.py` – Binomial Model

Defines a `binomial_tree_model` class with:

- Up and down factors `u`, `d`
- Risk-free rate `r`
- Time frame `T`
- Number of steps `N`

This model is passed to the option pricing classes.

---

### `options.py` – Option Pricers

Contains three classes, each with a `.price()` method:

- `EuropeanOption`: Vanilla European call/put pricing
- `AmericanOption`: Allows early exercise
- `BarrierOption`: Supports knock-in and knock-out features

Each class accepts:
- A `binomial_tree_model` instance
- Initial stock price `S0`
- Strike price `K`
- Maturity `T`
- Option type: `'call'` or `'put'`
- Barrier level `H` and type (for barrier options): `up/down-and-out/in`

---

## 🚀 Example Usage

```python
from models import binomial_tree_model
from options import european_option, american_option, barrier_option

S_in = 100 # initial stock price
K = 100 # strike price
T = 1 # maturity in years
r = 0.06 # risk-free rate

# up jump move factor and Number of time steps
u = 1.1
N = 3

# extra contract conditions for barriers 
H = 125
option_type = 'call'
barrier_type = 'up-and-out'

# Create recombining binomial model: d = 1/u
model = binom_model = binomial_tree_model(u, r, T, N)

# Price a European call
eu_option = european_option(binom_model, S_in, K, T, is_call=True)
eu_price = eu_option.price()

# Price an American put
us_option = american_option(binom_model, S_in, K, T, is_call=False)
us_price = us_option.price()

# Price a down-and-out barrier call
b_option = barrier_option(binom_model, S_in, K, H, T, option_type=option_type, barrier_type = barrier_type)
b_price = b_option.price()

print(f"European call price: {eu_price:.5f} $")
print(f"American put price: {us_price:.5f} $")
print(f"Barrier {barrier_type} {option_type} price: {b_price:.5f} $")
```

