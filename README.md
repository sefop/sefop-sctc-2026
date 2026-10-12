# sefop-sctc-2026

**Airlines Optimization Workshop: industry best practices for a decision-support system.**
3rd Annual Southern Colorado Transportation Conference (SCTC 2026), Colorado State University Pueblo.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![Tests](https://github.com/sefop/sefop-sctc-2026/actions/workflows/ci.yml/badge.svg)](https://github.com/sefop/sefop-sctc-2026/actions/workflows/ci.yml)


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

4. Plan the workshop flight:

   ```bash
   python -m cli optimize_cargo SC101
   ```

   You should see:

   ```text
   Flight SC101   weight limit 1,000 kg

   Shipment  Customer          Weight  Revenue  Decision
   --------  ----------------  ------  -------  -----------
   S1        Atlas Steel       300 kg   $3,000  LOADED
   S2        Atlas Steel       250 kg   $2,400  LOADED
   S3        Atlas Steel       200 kg   $1,900  LOADED
   S4        Bighorn Auto      250 kg   $2,300  LOADED
   S5        Bighorn Auto      150 kg   $1,300  left behind
   S6        Cedar Pharma      100 kg     $800  left behind
   S7        Dune Electronics  150 kg   $1,100  left behind
   S8        Elk Outfitters    100 kg     $700  left behind
   S9        Fremont Farms     200 kg   $1,200  left behind

   Shipments      4 loaded, 5 left behind
   Revenue        $9,600
   Weight used    1,000 of 1,000 kg
   ```

   `python -m cli optimize_cargo SC001` plans a three-shipment flight small enough to check by hand.

5. Run the tests. They finish in about a second; add `-v` to read their names, which are written
   as sentences a planner would recognize.

   ```bash
   pytest
   ```

## Business problem

A cargo flight has more shipments waiting than it can carry. A load planner decides which ones
fly. Each shipment belongs to a customer, has a weight, and earns a revenue if it flies. The
aircraft can carry only so much weight, and that limit is physical: it is never exceeded.

The program supports that decision. It recommends the load that earns the most revenue; the
planner makes the final call.

In the output above, the aircraft is full and revenue is as high as it can be. Look at the Customer
column, though: four customers have nothing on this flight. That observation is where the workshop
starts.

**What the planner gives the program.** One folder per flight under `data/`, each holding a
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

To plan your own flight, copy a folder, rename it, edit the file, and pass the folder's name to
`optimize_cargo`. The flights, customers and numbers here are invented for the workshop.

**What the program answers.**

| Situation | What you see | Exit code |
| --- | --- | --- |
| A load was chosen | The table above | 0 |
| The data is fine, but every shipment alone is heavier than the weight limit | `No shipment fits on this flight: ...` | 1 |
| The data is missing or wrong | `Cannot plan this flight: ...` followed by what to correct | 2 |

A shipment that alone is heavier than the weight limit is marked `left behind (over weight limit)`,
to tell it apart from a shipment that fits but lost out to more valuable cargo.

**A planner would not use a terminal.** A terminal is enough to follow one business request from
the planner's words to a tested program, which is what the workshop does. A screen for the planner
is a presentation requirement for a later version;
[`sefop-python-advanced`](https://github.com/sefop/sefop-python-advanced) shows the same ideas
behind a web application.

## Mathematical model

The decision is a 0/1 knapsack problem.

```text
Sets and parameters
    i            a shipment waiting for the flight
    revenue_i    revenue earned if shipment i flies (USD)
    weight_i     weight of shipment i (kg)
    W            weight limit of the aircraft (kg)

Decision variable
    x_i = 1 if shipment i flies, 0 if it is left behind

Objective
    maximize    sum over i of  revenue_i * x_i

Constraint
    sum over i of  weight_i * x_i  <=  W
```

- The weight limit is the only constraint, and it is hard.
- The customer of each shipment is in the data and in the output, but not in the model.
- When several loads earn the same highest revenue, the program returns any one of them.
- The model is a simplification of the planner's decision, not a copy of it.

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

The solver's answer is trusted because, on small flights, it earns exactly the same revenue as
trying every possible load one by one
(`tests/use_cases/solving/optimization/test_providers_agree_with_enumeration.py`).

To change the code, run all three checks before committing. The installation already brought in
the formatter and the type checker:

```bash
black src tests    # format
mypy               # check the type hints
pytest             # run the tests
```
