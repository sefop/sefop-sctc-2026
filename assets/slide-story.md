# Agreed workshop slide story

The agreed structure is 18 slides for a 90-minute workshop, including questions.
No code is written during the workshop. All artifacts are prepared; the program and tests run
live. Attendees discuss the proposed questions in pairs and record their answers on ordinary
paper or in a notebook.

The story moves from general principles to a concrete example: recurring business decisions
require software; before a recommendation can be trusted, production needs two kinds of evidence:
validation (the right problem) and verification (the problem solved right); a decision-support
system is software, and because software is fragile and built with imperfect information,
obtaining and keeping that evidence requires learning quickly and adapting quickly and safely;
working on a DSS is therefore a cycle that goes round again with every change; engineering
practices support those abilities. The original cargo business request leads to a
knapsack model and a runnable system. A business change then shows the cycle starting again.

The workshop has four parts. Part I sets out the principles and introduces the example. Part II
validates the planner's request: interview, user stories, examples and the model. Part III
verifies the first version: why software needs design and testing, the example's design, and the
tests that show it computes the model. Part IV zooms out: the cycle runs again as the planner
asks for client diversity, and the workshop closes with what this profession needs and where to
keep learning.

The user stories and examples start with the original request and would grow when the change
arrives. Audience questions,
test proposals and decisions contribute to the walkthrough.

## Part I — Introduction: principles and the example

### 1. A decision-support system supports recurring business decisions

- Combines data, business rules, and mathematical models.
- Produces recommendations repeatedly as new inputs arrive.
- Helps a person make and act on a decision.
- Connecting idea: a DSS is only useful if people act on its recommendations, so what would make
  you trust one?

### 2. Audience: what would you need before trusting a recommendation?

- Imagine a mathematical model says "optimal."
- With your partner, identify two things you still need to know before acting.
- Write one question you would ask the team that built the system.
- Answer: "optimal" only means optimal for the model as it was coded. Before acting I need
  evidence on three things: the data is correct and current; the model states the business's
  real objective and rules; and the software computes what the model says, for example tests and
  a small case checked by hand. Good question for the team: "How do you know it is correct, and
  what did you leave out?" These needs fall into two groups: the right data and rules
  (validation) and code that computes the model (verification).
- Connecting idea: the audience's needs fall into two groups, and the next slide names them:
  validation and verification.

### 3. Deploying a tool requires validation and verification

- Visual (from the MIP 2025 deck): business problem → math model → coded model, two
  translations. Validation spans the first translation, verification the second.
- Validation asks "are we solving the right problem?": do the model's objective and rules match
  the business's real decision? It is a consulting problem, answered with requirements,
  acceptance criteria, and feedback from use.
- Verification asks "are we solving the problem right?": does the code compute exactly what the
  model states? It is a software problem, answered with design and automated tests. A
  recommendation goes to production only when both hold.
- Connecting idea: both kinds of evidence pass through code, so next comes why software makes them
  hard to obtain and keep.

### 4. A decision-support system is software, so the rules of software apply

- Validation and verification are hard to obtain and keep because a DSS is software: every
  recommendation passes through code that reads data, builds a model and reports the result.
  Software principles apply whether we know them or not: a sign error in a data-processing script
  retracted five published papers, and an unhandled overflow in reused code destroyed the Ariane 5
  rocket 37 seconds after launch.
- So trustworthy recommendations need software engineering, not only good mathematics.
- Connecting idea: next, the big picture: the cycle that takes a request all the way to the user.

### 5. The big picture: working on a DSS is a cycle

- Visual: a loop. Business request → clarify and record requirements → math model → design and
  code → tests → deploy → use: the planner decides → feedback → the next business request. The
  arc from request to math model is marked validation; design and code to tests is marked
  verification; deploy and use put the change in the user's hands; feedback starts validation
  again.
- One pass takes a request all the way to the user: a change helps the user only once it is
  deployed.
- Map of the workshop: Part I introduces the example; Part II validates the planner's request;
  Part III verifies the first version; Part IV zooms out: the cycle runs again, then what this
  profession needs and where to keep learning.
- Connecting idea: to see the cycle at work, we now follow one concrete DSS round it.

### 6. Our example DSS: choosing the cargo for each flight

- Visual: a generic illustration of a load planner at a desk beside a cargo aircraft being
  loaded, with shipments waiting. No text, numbers, ticks or formulas: it must reveal nothing of
  the model or of which shipments fly.
- Every flight, more shipments are waiting than the aircraft can carry, and a load planner
  decides which ones fly: a recurring decision, the kind a decision-support system supports.
- What the planner wants from a tool is not yet clear: it reaches us second-hand.
- Connecting idea: the request arrives as one vague sentence from a manager, so the audience must
  find out from the planner what is really needed.

## Part II — Validation: are we solving the right problem?

### 7. Audience: interview the planner to find the requirements

- A manager says: "I heard our cargo planner wants a tool that picks the best shipments for each
  flight."
- Interview the planner (Francisco). Scan the answers for at least: decisions, objectives,
  constraints, type of data, nature of data (deterministic or stochastic), and risks.
- With your partner, prepare two questions (1 minute); pairs then ask in turn, and every pair
  records the answers.
- Write each requirement as a user story: "As a <type of user>, I want <goal>, so that
  <reason>."
- Answer: decision: which shipments fly, each one yes or no; objective: the most revenue per
  flight; constraints: the aircraft's maximum weight is never exceeded, and a shipment flies whole
  or stays; type of data: per flight the weight limit, per shipment its customer, weight and
  revenue; nature of data: deterministic, since weights and revenues are booked before planning;
  risks: an overweight load is a safety incident, and a wrong booking can produce a nonsense
  recommendation. User stories:
  - As a load planner, I want the tool to propose which shipments fly on each flight, so that the
    flight earns the most revenue it can carry.
  - As a load planner, I want every proposed load to stay within the aircraft's maximum weight, so
    that the flight is always safe to operate.
  - As a load planner, I want each shipment loaded whole or left behind, so that every proposal is
    a load I can actually build.
  - As a load planner, I want to see which shipments fly and which stay, with the revenue and the
    weight used, so that I can check the proposal before I accept it.
  - As a load planner, I want the tool to tell me when a flight's data is wrong or missing, so
    that I never act on a recommendation built from bad data.
- Connecting idea: user stories say what the planner wants; concrete examples of what the planner
  would do make them checkable.

### 8. Examples show what the planner would do

- Example 1, weight limit 500 kg. Atlas Steel 500 kg, $3,000; Bighorn Auto 250 kg, $2,000; Cedar
  Pharma 250 kg, $1,800. The planner loads Bighorn and Cedar: $3,800 and 500 kg, more than the
  single most valuable shipment would earn.
- Example 2, weight limit 500 kg. Atlas Steel 300 kg, $3,000; Bighorn Auto 900 kg, $9,000; Cedar
  Pharma 300 kg, $800. Bighorn can never fly on this aircraft, however valuable; Atlas and Cedar
  together weigh 600 kg, so only Atlas flies: $3,000 and 300 kg.
- Each example is an acceptance criterion: a situation and the decision the planner expects. This
  is how validation becomes checkable.
- Connecting idea: the user stories and examples now become mathematics, the first translation,
  from business problem to math model.

### 9. The business rules lead to a knapsack model

- Whole-shipment choices become binary variables: $x_i \in \{0,1\}$.
- Revenue maximization becomes $\max \sum_i r_i x_i$.
- Aircraft capacity becomes $\sum_i w_i x_i \leq W$.
- Connecting idea: a model on paper recommends nothing; the second translation, from math model
  to coded model, is where verification begins.

## Part III — Verification: are we solving the problem right?

### 10. Software is a different kind of engineering

- Visual (from the Purdue workshop): civil engineering beside software engineering.
- A bridge tolerates tiny errors and is designed from requirements known reasonably well.
  Software is flexible and fragile at once: one wrong sign can change every recommendation while
  the program still runs, and it is built with highly imperfect information.
- Building software is a discovery process: users do not fully know what they want, they change
  their minds, and building reveals problems nobody foresaw. So the team must learn quickly and
  adapt its software quickly and safely.
- Connecting idea: adaptability make quick and safe change possible. This is achieved through
design and testing.

### 11. Design and testing make quick, safe change possible

- Design is how the code is structured into modules, each with one clear responsibility. A change
  stays small and isolated, and each module can be understood and checked on its own.
- Testing checks automatically that the code complies with what it should do: it runs the code on
  cases whose right answer is known, in seconds and as often as needed. That is verification, and
  it is the safety layer that catches a mistake the moment a change introduces it.
- Each needs the other: a clear design makes code testable, and tests make it safe to improve the
  design.
- Visual: 2 diagrams showing N modules connecting everything to each other, and then N modules connected
with less connections, indicating a more modularized design.
- Connecting idea: here we show the purpose of modularization, in the next slide we show how to 
evaluate a change.

### 12. What an automated test is

- A test is a small program that runs the code on a case whose right answer is known and checks
  the result. It has three steps: arrange the case, act by running the code, assert the expected
  result.
- Visual: the three steps applied to example 1 of slide 8. Arrange: a flight with a 500 kg limit
  and three shipments: 500 kg for $3,000, 250 kg for $2,000, and 250 kg for $1,800. Act: ask the
  tool for a load. Assert: the two 250 kg shipments fly, and the revenue is $3,800.
- A test runner runs every test automatically, in seconds, with the same result each time; a
  failed check names exactly what broke. Run after every change, it shows at once whether the
  change broke something.
- Connecting idea: with design and tests understood, here is how they look in our example,
  starting with its design.

### 13. A DSS example design

- A DSS is usually divided into the same modules: reading data, preprocessing, optimization,
  postprocessing, and presenting the result.
- Run the first version on flight SC101: the console announces each stage in a box: Read data,
  Preprocess, Solve, Postprocess, Result.
- Open the repository: each box is one place in `src/`. Reading data is
  `adapters/json_data_loader.py`; preprocessing, optimization and postprocessing are folders
  under `use_cases/solving/`; presenting the result is `adapters/console_result_writer.py`.
- Interpret the proposed load with the audience.
- Connecting idea: the program produces a load, but does it compute what the model states? Tests
  are the evidence.

### 14. Audience: the planner's examples become acceptance tests

- Example 2 of slide 8 as a test. Arrange: a 500 kg limit; shipments of 300 kg for $3,000, 900 kg
  for $9,000, and 300 kg for $800. Act: ask for a load. Assert: only the first shipment flies,
  earning $3,000.
- Predict with your partner: would this test catch code that ignores the weight limit? Code that
  splits a shipment?
- Then open the repository: the planner's examples are stored as test flights and run with every
  other test.
- Answer: yes to both. Ignoring the limit loads all three shipments (1,500 kg); splitting adds part
  of the 900 kg shipment to reach $5,000. Example 1 catches only the first bug, because its best
  load already uses whole shipments: not every example catches every bug, so tests are chosen to
  cover each requirement.
- Connecting idea: the tests pass, so the first version is verified and goes into the planner's
  hands.

## Part IV — Zooming out: the next cycle, the profession and SEFOP

### 15. The cycle runs again: the planner asks for client diversity

- Visual: the cycle from slide 5, going round a second time.
- In use, the planner notices that four of the six customers get nothing on a flight, and asks
  the tool to serve more customers within an acceptable revenue sacrifice.
- The request goes round the same cycle: validate it with user stories, examples and a new model;
  verify it with design and tests; deploy it; use it. Modular, tested software is what makes the
  second round fast and safe.
- Connecting idea: every round asks for the same skills; zooming out, here is what this
  profession needs.

### 16. What this profession needs

- Validation skills: understanding the business, interviewing users, turning requests into
  requirements and examples, and modeling.
- Verification skills: designing modular software and testing it automatically.
- Connect those skills to Francisco's experience and to students' career opportunities.
- Connecting idea: one workshop shows the tip of these skills; SEFOP is where to keep learning.

### 17. SEFOP: where to keep learning

- The SEFOP training hub and its book: github.com/sefop/sefop-training-hub
- This workshop's repository, to run and read at home: github.com/sefop/sefop-sctc-2026
- The discussion board, for questions after today: github.com/sefop/sefop-training-hub/discussions
- Connecting idea: with the materials shared, the floor opens for questions.

### 18. Questions and discussion

- What remains unclear about turning a business request into decision-support software?
- Where would you apply learning and adaptation in your own project?
- Connecting idea: there is no next slide; the next business request starts validation and
  verification again, back round the cycle of slide 5.

## Pacing

Pair discussions are included in these blocks.

| Minutes | Part | Slides | Focus |
| --- | --- | --- | --- |
| 0-15 | I | 1-6 | DSS characteristics, trust, validation and verification, a DSS is software, the cycle, and the example |
| 15-38 | II | 7-9 | Planner interview, user stories, examples, and the knapsack model |
| 38-65 | III | 10-14 | Software as a different kind of engineering, design and testing, what an automated test is, the repository tour, and the planner's examples as acceptance tests |
| 65-80 | IV | 15-17 | The cycle runs again, what the profession needs, and SEFOP |
| 80-90 | IV | 18 | Questions and discussion |

## Pair activity routine

Allow 30-45 seconds of individual thinking, then 1-2 minutes of pair discussion.
Each pair records one answer and alternates who writes. Hear two contrasting responses,
connect their reasoning to the requirements, design or evidence, and let everyone revise
their notes. Give the planner interview more discussion time.

Pairs keep three sections in their notes: business request, user stories and examples, and
evidence.
The presenter records the user stories from the interview, annotates the software
diagram with predictions, and compares proposed tests with the prepared checks.

## Planner's script (presenter only)

For the interview on slide 7. Francisco answers only what is asked, truthfully, and says "not for
now" to anything beyond version 1.

| If asked about | The planner says | Requirement it gives |
| --- | --- | --- |
| What "best" means | "I'm judged on the revenue each flight earns." | Maximize revenue |
| The aircraft's weight | "There is a maximum weight. It is never exceeded; it's safety." | Hard weight limit |
| Splitting a shipment | "No. A shipment flies whole or waits for a later flight." | Whole shipments |
| Volume or space | "Not for now; weight is what limits us." | Out of scope |
| Shipments that must fly | "None for now." | Out of scope |
| Customers | "Every shipment belongs to a customer, but today I only look at revenue." | Customer in the data, not in the objective; seeds Part II |
| What the tool should show | "Which shipments fly, which stay, the revenue and the weight used." | Output |
| What data exists | "For each flight, the weight limit; for each shipment, customer, weight and revenue." | Inputs |
| What you decide | "Which shipments fly on this flight. The aircraft, route and schedule are already fixed." | Decision: yes or no per shipment |
| How sure the numbers are | "Weights and revenues are booked before I plan, so I know them exactly." | Deterministic data |
| What could go wrong | "An overweight load is a safety incident; that must never happen. And a typo in a booking can make any tool recommend nonsense." | Risks: safety; bad data must be caught |

The "Customers" answer is deliberate: it plants the customer column that the business change in
Part II turns into a new objective.

## Demonstration boundaries

The customer-service change (client diversity) is mentioned on slide 15 as the next round of the
cycle; it is not built or demonstrated. Aircraft weight is a hard limit.

Deployment is local on Francisco's machine, without separate development, staging or production
environments. The remaining demonstration decisions are listed in
[instructions.md](instructions.md#what-to-settle-first).
