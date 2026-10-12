# sefop-sctc-2026

**Airlines Optimization Workshop: industry best practices for a decision-support system.**
3rd Annual Southern Colorado Transportation Conference (SCTC 2026), Colorado State University Pueblo.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![CI](https://github.com/sefop/sefop-sctc-2026/actions/workflows/ci.yml/badge.svg)](https://github.com/sefop/sefop-sctc-2026/actions/workflows/ci.yml)

A cargo flight has more shipments waiting than it can carry. A load planner decides what flies.
This repository is the program from the workshop: it reads one flight, chooses the shipments that
earn the most revenue without exceeding the aircraft's weight limit, and prints the result for the
planner.

> A model is finished when someone decides with it, not when the solver says optimal.

## Two ways in

| Run the program | Read why it is built this way |
| --- | --- |
| You need Python 3.10 or newer and about five minutes. Follow [Run it yourself](#run-it-yourself) below. | The program follows SEFOP, the Software Engineering Framework for Optimization Programs. Start reading at the [SEFOP training hub](https://github.com/sefop/sefop-training-hub). |
| Then change a shipment in `data/SC101/data.json` and run it again. | Questions, about the workshop or about your own project: ask on the [discussion board](https://github.com/sefop/sefop-training-hub/discussions). |

## Run it yourself

1. Get the code: on GitHub choose **Code → Download ZIP** and unzip it, or fork and clone the
   repository. Open a terminal in the project folder.

2. Create a virtual environment and activate it:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux
   ```

3. Install what the program needs (the HiGHS solver, the test runner and the program itself):

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

The aircraft is full and revenue is as high as it can be. Look at the Customer column, though:
four customers have nothing on this flight. That observation is where the workshop starts.

`python -m cli optimize_cargo SC001` plans a three-shipment flight small enough to check by hand.

## Run the tests

```bash
pytest
```

About 125 tests run in under a second. Add `-v` to read their names; they are written as
sentences a planner would recognize, such as `test_a_load_never_exceeds_the_weight_limit`.

```bash
pytest -m "not integration"   # unit tests only
pytest -m integration         # only the tests that run the real command end to end
```

## The decision

Each shipment either flies or is left behind. The program maximizes total revenue, subject to one
hard physical limit: the weight the aircraft can carry.

```text
maximize    sum of revenue_i * x_i
subject to  sum of weight_i  * x_i  <=  weight limit
            x_i is 0 or 1            (1 = shipment i flies)
```

This is the classic knapsack problem. It is a simplification of the planner's real decision, not a
copy of it. The customer of each shipment is in the data and in the output, but this version of the
model does not use it.

## The input

One folder per flight under `data/`, each holding a `data.json`:

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

## What the program can tell you

| Situation | What you see | Exit code |
| --- | --- | --- |
| A load was chosen | The table above | 0 |
| The data is fine, but every shipment alone is heavier than the weight limit | `No shipment fits on this flight: ...` | 1 |
| The data is missing or wrong | `Cannot plan this flight: ...` followed by what to correct | 2 |

A shipment that alone is heavier than the weight limit is marked `left behind (over weight limit)`,
to tell it apart from a shipment that fits but lost out to more valuable cargo.

When several loads earn the same highest revenue, the program returns any one of them.

Add `--verbose` before the command to see each step the program takes:
`python -m cli --verbose optimize_cargo SC101`.

## How the code is organized

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

## A planner would not use a terminal

A terminal is enough to follow one business request from the planner's words to a tested program,
which is what the workshop does. It is not what a planner would work with. A screen for the planner
is a presentation requirement for a later version;
[`sefop-python-advanced`](https://github.com/sefop/sefop-python-advanced) shows the same ideas
behind a web application.

## If you change the code

```bash
pip install -r requirements-dev.txt
black src tests    # format
mypy               # check the type hints
pytest             # run the tests
```

## License

[MIT](LICENSE)
