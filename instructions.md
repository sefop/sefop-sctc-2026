# Instructions: SCTC 2026 workshop repository

This file records the design of the workshop and what this repository has to do for it. Read it
before writing any code. The agreed 15-slide story is in [slide-story.md](slide-story.md).
The business story and feature are agreed. Version 1 of the program, the original knapsack, is
implemented; see [Settled for version 1](#settled-for-version-1). The rest of the demonstration
contract must be settled before the feature is implemented, as described in
[What to settle first](#what-to-settle-first).

This workshop is in the context of SEFOP https://github.com/sefop. It is a 90-min workshop including questions.
The conference is : https://sctcconsultants.glueup.com/event/2026-sctc-annual-conference-save-the-date-october-11-14-2026-170072/

## The event

- **Conference:** 3rd Annual Southern Colorado Transportation Conference (SCTC 2026), Colorado State
  University Pueblo, Occhiato Student Center Ballroom.
- **Date:** Thursday, October 22, 2026, inside the 1:30-3:30 pm slot shared with the poster session,
  the industry exhibit and two other workshops.
- **Title on the published flyer:** "Airlines Optimization Workshop: Industry best practices for a
  decision-support system".
- **Length:** 90 minutes.
- **Speaker:** Francisco Zenteno Smith, Senior Operations Research Scientist, American Airlines,
  creator of SEFOP (Software Engineering Framework for Optimization Programs).
- **Host:** Dr. Himadri Sen Gupta, Industrial Engineering, faculty advisor of the IISE student
  chapter.
- **Audience:** graduate and undergraduate students who know some optimization but are not
  proficient in it. Assume little software background.

## What the workshop argues

- **Learning outcome:** attendees can explain why a solved model is not yet a decision someone can
  use, and trace a business request through requirements, acceptance criteria, design, testing,
  local deployment and a planner's decision.
- **Thesis:** "A model is finished when someone decides with it, not when the solver says optimal."
  Said aloud right after the opening problem: "and deciding with it requires being able to trust
  it."
- **The message to land:** the business problem is priority one, and the software is
  reverse-engineered from it.
  - The model is a living artifact: new business needs change the model and the software around it.
  - The model is a simplification of reality, not its twin.
  - Revenue and customer service compete. The business specifies acceptable revenue sacrifices;
    the model returns options, not one verdict.
  - The planner makes the final decision, with information the model left out.
  - Hard and negotiable limits are told apart explicitly, so "the planner decides" is not heard as
    "every limit can be relaxed". Aircraft weight is the inviolable example.

## How the session runs

Guided reverse engineering of one business change through the entire lifecycle. No code is written
during the workshop. All artifacts are prepared; Francisco runs the program and tests live on his
own machine. Attendees interview the planner, help define acceptance criteria, predict tests and
choose among the resulting options. Nobody is asked to reproduce anything on a laptop.

| Min | Slides | Block | Who acts |
| --- | --- | --- | --- |
| 0-10 | 1-2 | Original cargo decision, revenue-maximizing knapsack and the new customer-service request | Francisco |
| 10-28 | 3-4 | Interview the planner; build requirements and acceptance criteria | Audience, guided |
| 28-43 | 5-6 | Trace the request into model and software design, including three revenue-allowance options | Francisco, audience questions |
| 43-55 | 7-8 | Predict tests, then run prepared checks for existing and new behavior | Audience, Francisco |
| 55-67 | 9-11 | Deploy locally, run the updated console program and choose among three options | Francisco, audience |
| 67-75 | 12-13 | Discuss missing information and the next iteration of the living model | All |
| 75-80 | 14 | Career skills, Francisco's experience and SEFOP next steps | Francisco |
| 80-90 | 15 | Questions and discussion | All |

- The emphasis is on tracing one business requirement through the full lifecycle. The central
  artifact is a table built in minutes 10-28: business requirement, model element, software
  requirement, acceptance criterion. Keep it visible and refer back to it during design and tests.
  Use only enough mathematics and architecture to explain the decisions along that path.
- The interview block follows a bounded protocol: a concrete shipment table on screen, a minute of
  individual thinking, specific prompts, a visible requirements list, and a timed fallback of two or
  three scripted planner prompts about customer service, revenue sacrifice and useful output.
- Requirements the room raises that the prepared model lacks go on a visible "not in the model"
  list. That list is the evidence that the model is a simplification.
- The prepared change adds a customer-service objective to the original revenue-maximizing
  knapsack. A customer is served if at least one of their shipments flies; loading several
  shipments for the same customer still counts once. For each of three revenue-sacrifice
  allowances, maximize distinct customers served while respecting the corresponding minimum
  revenue and all hard physical limits. The allowance values remain to be agreed.
- Show existing tests protecting revenue-maximizing behavior and hard limits, and new tests
  checking customer counting, revenue allowances and the new output. Run them live in seconds.
- Show a simple local deployment of the tested version and its changed console output. All steps
  happen on Francisco's machine; there are no separate development, staging or production
  environments. The precise local update mechanism remains to be agreed. Broader release and
  monitoring practices are follow-up topics in the SEFOP book.
- Discuss all four examples of information the model may lack: previous service failures, whether
  partial delivery is useful, urgent downstream deadlines and future customer relationships.
  These are examples, not additional objectives already included in the model. Recurring omitted
  information can become a requirement for the next version.
- Closing request: "run tonight's program yourself". One QR code, to this repository. One slide
  connects lifecycle steps to career skills, Francisco's path and SEFOP next steps.

## What this repository is

- **Problem:** airline cargo loading. A load planner chooses what flies. The original version is
  a revenue-maximizing knapsack. The updated version maximizes distinct customers served within
  three specified revenue-sacrifice allowances, relative to maximum achievable revenue.
- **Shape:** follows [`sefop-python-starter`](https://github.com/sefop/sefop-python-starter)
  (local copy at `C:/Users/zente/Github/sefop-python-starter`): a command line over the model, with
  `src/cli.py`, `startup.py`, `domain/`, `use_cases/`, `adapters/`, `tests/` and `data/`. The
  starter solves food selection (maximize calories within a budget and a weight limit); here the
  same structure is renamed and adapted to cargo.
- **No web page.** `sefop-python-advanced` is too complex for this audience. The program runs in
  the terminal.
- **Both existing Python repositories stay unchanged.**
- **Runs offline** on Francisco's laptop. A screen recording of the demonstration is the fallback
  (a default not yet confirmed by Francisco).

### Requirements the program must meet

1. **Readable from the back of a room.** One short table per run: shipments loaded, shipments left
   behind, revenue, customers served, limits used. Large font on a light background when projected.
2. **Options side by side.** When the program returns more than one load, they appear in a single
   table so the trade-off is obvious at a glance. The planner's choice happens in Francisco's
   narration, so the output has to carry it.
3. **Two behaviors, in this order.** First, maximize revenue within hard physical limits. Then
   return three customer-service options for agreed revenue-sacrifice allowances, preserving
   those hard limits. Prepare an example that makes the tradeoffs visible.
4. **Outcomes named in the planner's language.** Invalid input, a normal result and any genuinely
   infeasible case have distinct messages. Infeasibility is not the feature driving this story.
5. **Tests that run on screen in seconds.** They pass before the feature and after it, and include
   new checks for distinct customer counting, revenue allowances and customer-service behavior.
6. **Simple to run for someone who follows the QR code:** download as ZIP or fork, create a virtual
   environment, `pip install`, one command. Accept any recent Python rather than one exact version,
   and keep the libraries to the minimum.
7. **A first page (`README.md`) with two entrances side by side:** how to run the program, and where
   to start reading in the SEFOP book, plus the link to the discussion board.
8. **A prepared local deployment checkpoint.** Demonstrate putting the tested version into use
   on the same machine, then run it to show the new console behavior. No live code writing.

### Suggestions to weigh while building

- Keep one exact solver, plus enumeration as the reference the tests compare against. Drop the
  starter's heuristic and its second solver.
- Say openly in the session and in the first page that a planner would not use a terminal. "A
  screen for the planner" is a future presentation requirement, with `sefop-python-advanced` as
  the place to see it.
- Keep aircraft weight and other physical limits hard in both versions. The tradeoff being
  negotiated in this feature is revenue sacrifice for customer service, not exceeding capacity.

## What to settle first

The demonstration contract, agreed with Francisco before any code. The repository skeleton starts
immediately after it; the planner's script is refined in parallel.

1. **The situation:** the flight, the planner, the shipments and customers in the prepared example.
2. **The inputs** the program reads.
3. **The exact three revenue-sacrifice allowances and tie handling.** The definition of service
   is agreed: any loaded shipment serves its customer, and each customer counts once. The option
   method is agreed: maximize customers served within each allowance relative to maximum revenue.
4. **The exact physical limits and data representation.** Physical limits stay hard; revenue
   sacrifice is the negotiated tradeoff.
5. **The planner's script and audience prompts.** Use the four agreed examples of omitted
   information to discuss how the planner's final decision can differ from a model's ranking.
6. **The prepared teaching checkpoints:** original knapsack run; requirements and acceptance
   criteria; model and software design; existing and new tests; local deployment; updated console
   comparison; audience choice and missing-information discussion.
7. **The local deployment mechanism and offline fallback.** Agree what the presenter updates and
   launches, and how each checkpoint can be reproduced without writing code live.

## Settled for version 1

Version 1 is the original revenue-maximizing knapsack, the starting point of slides 1 and 8. It is
implemented. The customer-service feature is not part of it.

- **Model:** each shipment flies or is left behind (0/1), with a revenue and a weight. Aircraft
  weight is the only limit and it is hard. There is no volume limit.
- **Customer:** every shipment names its customer in the input, the domain and the output table.
  The version 1 model ignores it.
- **Inputs:** `data/<flight>/data.json` with `flightId`, `maxWeightKg` and `shipments`
  (`id`, `customer`, `weightKg`, `revenueUsd`).
- **Prepared flight:** `SC101`, 1,000 kg, nine shipments, six invented customers. Maximum revenue
  is $9,600 with a single optimal load (S1-S4), serving two customers. Checked by enumeration,
  the most customers servable at each revenue level is: 4 customers at $9,200 (4.2% below the
  maximum), 5 at $8,800 (8.3%), 6 at $8,100 (15.6%). Allowances of 5%, 10% and 20% would
  therefore give three different options; the values themselves are still to be agreed.
  `SC001` is a three-shipment flight that can be checked by hand.
- **Command:** `python -m cli optimize_cargo <flight>`, use case `OptimizeCargo`. It is the only
  command.
- **Solver:** HiGHS (`highspy`) is the only solving path. Brute-force enumeration is the reference
  the tests compare it against.
- **Pipeline:** preprocessing sets aside shipments heavier than the weight limit, HiGHS solves,
  postprocessing orders the load as the flight lists it.
- **Output:** one plain-text table on the console, at most 80 columns. No files are written.
- **Outcomes:** a load (exit code 0); "No shipment fits on this flight" when every shipment alone
  exceeds the weight limit (1); "Cannot plan this flight: ..." naming what to correct when the
  data is missing or wrong (2). A 0/1 knapsack is never mathematically infeasible, because
  loading nothing always respects the limit, so "no shipment fits" stands in for infeasibility
  in this version.
- **Ties:** not handled in version 1. Any load with the maximum revenue is accepted, and tests
  assert the revenue, not the load.
- **Tooling:** Python 3.10 or newer; `requirements.txt` holds `highspy`, `pytest` and the project
  itself, `requirements-dev.txt` adds `black` and `mypy`; one CI workflow on Python 3.10 and 3.13.
- **First page:** the book entrance points to `sefop/sefop-training-hub` and the discussion board
  to its GitHub Discussions.

## Open items

- The three revenue-sacrifice allowance values, tie handling among customer-service options, and
  whether the feature is a second command or a change to `optimize_cargo`.
- The side-by-side options table.
- The planner's script.
- The local deployment mechanism and confirmation of the fallback recording.
- Whether American Airlines stories stay at a public level (working assumption: yes).
- Host checklist for Dr. Gupta: exact start and end inside 1:30-3:30 pm; separate room or ballroom
  floor; projector, audio and a board or flip chart for the requirements list; expected headcount;
  whether attendees stay or drift between posters and workshops.

## Done means

- The program runs with the commands on the first page, on a clean virtual environment.
- Each teaching event in the demonstration contract can be produced with one command.
- The tests pass and run in seconds.
- One full timed rehearsal has been run, and the fallback recording exists.
