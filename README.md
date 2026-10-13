# sefop-sctc-2026

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![Tests](https://github.com/sefop/sefop-sctc-2026/actions/workflows/ci.yml/badge.svg)](https://github.com/sefop/sefop-sctc-2026/actions/workflows/ci.yml)

**Airlines Optimization Workshop: industry best practices for a decision-support system.**

3rd Annual Southern Colorado Transportation Conference (SCTC 2026), Colorado State University Pueblo.

## Installation instructions

1. Clone the repository and move into its folder:

   ```bash
   git clone https://github.com/sefop/sefop-sctc-2026.git
   cd sefop-sctc-2026
   ```

2. Create a virtual environment with Python 3.12 and activate it.

   On Windows:

   ```bash
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   ```

   On macOS or Linux:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the tests:

   ```bash
   pytest
   ```

5. Run one case:

   ```bash
   python -m cli optimize_cargo SC101
   ```

## Business problem

<p align="center">
  <img src="assets/planner_image.png" width="640"
       alt="A load planner at a desk beside a freighter being loaded, with six customers' shipments in front of
            them, four marked loaded and two left behind, under the goal of maximizing revenue while total
            weight stays within the aircraft's capacity">
</p>

A cargo airline sells space on its flights to customers who need goods moved. On a busy day, more
shipments are waiting at the airport than one aircraft can carry. Someone has to decide which
shipments fly today and which wait for a later flight. That person is the load planner.

**What the planner knows.** For each shipment: the customer it belongs to, how much it weighs, and
how much the airline earns if it flies. For the aircraft: the maximum weight it may carry.

**The rules.**

- The weight limit is a safety limit. It is never exceeded, however valuable the cargo.
- A shipment flies whole or stays behind whole. It cannot be split.

**The goal.** Choose the shipments that earn the most revenue for the flight.

**Why it is hard.** Loading the most valuable shipments first does not always give the best
result: one heavy shipment can take the room of two lighter ones that together earn more. Nine
waiting shipments can be combined in 512 ways; thirty, in more than a billion. No one can compare
them all before departure.

**Who decides.** The planner does. The recommended load is advice; the planner knows things the
numbers do not show and makes the final call.

**What the highest revenue hides.** On the workshop flight, six customers have cargo waiting. The
load that earns the most carries cargo for only two of them; the other four have nothing on this
flight. That observation is where the workshop starts.

The flights, customers and numbers here are invented for the workshop.

## Mathematical model

This problem can be formulated as a classical 0/1 knapsack problem. Given a flight, the program
returns the set of shipments that maximizes revenue without exceeding the aircraft's weight limit.

### Sets

- $I$: the shipments waiting for the flight. The index $i$ runs over it.

### Parameters

Assume all these are deterministic.

For each shipment $i \in I$:

- $r_i > 0$: the revenue earned if the shipment flies, in USD.
- $w_i > 0$: the weight of the shipment, in kg.

For the aircraft:

- $W > 0$: the maximum weight the aircraft may carry, in kg.

### Variables

- $x_i \in \lbrace 0, 1 \rbrace$: 1 if shipment $i$ flies, 0 if it is left behind, for each $i \in I$.

### Objective function

Maximize revenue:

$$
\max_{x} \quad \sum_{i \in I} r_i x_i
$$

### Constraints

**(C1) Weight limit.** The loaded shipments weigh no more than the aircraft may carry.

$$
\sum_{i \in I} w_i x_i \le W
$$

**(C2) Whole shipments.** A shipment flies whole or not at all.

$$
x_i \in \lbrace 0, 1 \rbrace \qquad \forall i \in I
$$

Put together, the complete model reads:

$$
\begin{aligned}
\max_{x} \quad & \sum_{i \in I} r_i x_i \\
\text{s.t.} \quad & \sum_{i \in I} w_i x_i \le W & \text{(C1) weight limit} \\
& x_i \in \lbrace 0, 1 \rbrace \quad \forall i \in I & \text{(C2) whole shipments}
\end{aligned}
$$


### Notation

| Symbol | Type      | Meaning                               | Unit | Domain                           |
| :----: | --------- | ------------------------------------- | ---- | -------------------------------- |
|  $I$   | set       | shipments waiting for the flight      | —    | finite set                       |
|  $i$   | index     | one shipment                          | —    | $i \in I$                        |
| $r_i$  | parameter | revenue earned if shipment $i$ flies  | USD  | $r_i > 0$                        |
| $w_i$  | parameter | weight of shipment $i$                | kg   | $w_i > 0$                        |
|  $W$   | parameter | maximum weight the aircraft may carry | kg   | $W > 0$                          |
| $x_i$  | variable  | whether shipment $i$ flies            | —    | $x_i \in \lbrace 0, 1 \rbrace$   |

### An example instance

Flight `SC001`, in `data/SC001/data.json`:

| Shipment         | Weight $w_i$ | Revenue $r_i$ |
| ---------------- | :----------: | :-----------: |
| S1: Atlas Steel  |     500      |     3000      |
| S2: Bighorn Auto |     250      |     2000      |
| S3: Cedar Pharma |     250      |     1800      |

with $W = 500$ kg:

$$
\begin{aligned}
\max_{x} \quad & 3000 x_1 + 2000 x_2 + 1800 x_3 \\
\text{s.t.} \quad & 500 x_1 + 250 x_2 + 250 x_3 \le 500 \\
& x_1, x_2, x_3 \in \lbrace 0, 1 \rbrace
\end{aligned}
$$

S1 is the most valuable shipment, but it fills the aircraft alone and earns 3,000 USD. S2 and S3
fit together and earn 3,800 USD. The optimal solution is $x_1 = 0$, $x_2 = 1$, $x_3 = 1$:

| Value       | Computed as                                  |     Result      |
| ----------- | -------------------------------------------- | :-------------: |
| Revenue     | $3000 \cdot 0 + 2000 \cdot 1 + 1800 \cdot 1$ |    3,800 USD    |
| Weight used | $500 \cdot 0 + 250 \cdot 1 + 250 \cdot 1$    | 500 of 500 kg   |

Run the following script in your terminal to reproduce this case:

```bash
python -m cli optimize_cargo SC001
```

## Repository structure

```text
src/
├── cli.py            reads the command line and hands over to startup.py
├── startup.py        the only place where concrete parts are assembled
├── domain/           Shipment, Flight, Load: the planner's vocabulary, with its rules
├── use_cases/
│   ├── use_case_optimize_cargo.py    load a flight, choose a load, report the outcome
│   ├── optimization_response.py      the three possible outcomes
│   ├── ports/                        what the use case needs from the outside world
│   └── solving/                      preprocessing -> solver -> postprocessing
│       └── optimization/
│           ├── mip_highs/            the model, written for the HiGHS solver
│           └── enumeration/          tries every load; the reference the tests compare against
└── adapters/         reading JSON, printing the table
tests/                mirrors src/, plus end-to-end situations under tests/resources/
data/                 one folder per flight
```

The layout follows [`sefop-python-starter`](https://github.com/sefop/sefop-python-starter), with
fewer parts. Dependencies point inward: `adapters/` knows about `use_cases/`, never the reverse, and
`domain/` knows about nothing else.

**Planning your own flight.** There is one folder per flight under `data/`, each holding a
`data.json`:

```json
{
  "flightId": "SC101",
  "maxWeightKg": 1000,
  "shipments": [
    { "id": "S1", "customer": "Atlas Steel", "weightKg": 300, "revenueUsd": 3000 }
  ]
}
```

Copy a folder, rename it, edit the file, and pass the folder's name to `optimize_cargo`.

