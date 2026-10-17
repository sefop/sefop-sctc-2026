# Agreed workshop slide story

The agreed structure is 23 slides for a 90-minute workshop, including questions.
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
knapsack model and a runnable system. Only then does an example business change introduce customer service and demonstrate how
the model and software evolve.

The workshop has four parts. Part I sets out the principles and builds the baseline system for
the original request. Part II validates the business change: what the planner needs and how the
model must change. Part III verifies it: how the software changes and what evidence shows it
works. Part IV returns to the planner, whose use and feedback start validation again.

The user stories and examples start with the original request and grow when the change arrives.
The same software diagram is revisited to trace the affected responsibilities. Audience questions,
test proposals and decisions contribute to the walkthrough.

## Part I — Introduction: principles and baseline

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
  recommendation goes to production only when both hold, and every change asks both again.
- Connecting idea: both kinds of evidence pass through code, so next comes why software makes them
  hard to obtain and keep.

### 4. A decision-support system is software, so the rules of software apply

- Validation and verification are hard to obtain and keep because a DSS is software: every
  recommendation passes through code that reads data, builds a model and reports the result.
  Software principles apply whether we know them or not: a sign error in a data-processing
  script retracted five published papers.
- Software is a different kind of engineering. A bridge tolerates tiny errors and is designed
  from well-known requirements; software is flexible and fragile at once, and is built with
  highly imperfect information.
- Building it is a discovery process: users do not fully know what they want, they change their
  minds, and building reveals problems nobody foresaw. So the team must learn quickly and adapt
  its software quickly and safely, to keep both kinds of evidence as the problem changes.
- Connecting idea: these characteristics mean the work is never done once; next, the big picture:
  the full cycle of working on a DSS.

### 5. The big picture: working on a DSS is a cycle

- Visual: a loop. Business request → clarify and record requirements → math model → design and
  code → tests → deploy → use: the planner decides → feedback → the next business request. The
  arc from request to math model is marked validation; design and code to tests is marked
  verification; deploy and use put the change in the user's hands; feedback starts validation
  again.
- Validation and verification are not one-time gates. Every business change goes round the whole
  cycle, and a change helps the user only once it is deployed.
- Map of the workshop: Part I goes round once for the original request; Part II validates a
  business change; Part III verifies it; Part IV deploys it, puts it in the planner's hands and
  collects the feedback that starts the next round.
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
  is how validation becomes checkable, and the same two examples return in Part III as automated
  tests.
- Connecting idea: the user stories and examples now become mathematics, the first translation,
  from business problem to math model.

### 9. The business rules lead to a knapsack model

- Whole-shipment choices become binary variables: $x_i \in \{0,1\}$.
- Revenue maximization becomes $\max \sum_i r_i x_i$.
- Aircraft capacity becomes $\sum_i w_i x_i \leq W$.
- Connecting idea: a model on paper recommends nothing; the second translation, from math model
  to coded model, turns it into a program the planner can run.

### 10. Software turns the model into a usable recommendation

- Read and validate the flight's data.
- Prepare the instance, solve it, and present the result.
- Run the original program and interpret the proposed load.
- Connecting idea: the baseline works and the planner uses it, and then the business asks for
  something new.

## Part II — Validation: define and model the change

### 11. The system must support new business needs

- Business objectives and rules can evolve.
- Example request: serve more customers within acceptable revenue sacrifices.
- Aircraft weight remains a hard limit.
- Connecting idea: "serve more customers" can be read in several ways, so before changing
  anything the audience clarifies the new request.

### 12. Audience: clarify the new request

- What exactly does "a customer is served" mean?
- How much revenue may be sacrificed, and relative to what baseline?
- What output would help the planner compare alternatives?
- Answer: a customer is served when at least one of its shipments flies, and counts once however
  many fly. Revenue sacrifice is measured against the maximum achievable revenue, $R^*$, as a
  percentage, for example 5%, 10% and 20%. The planner needs the options side by side: loaded
  shipments, revenue, revenue given up and customers served.
- Connecting idea: the clarified answers extend the user stories and examples with new acceptance
  criteria.

### 13. Extend the requirements and acceptance criteria

- Count distinct customers; several loaded shipments for one customer count once.
- Respect each agreed revenue allowance and the aircraft weight limit.
- Present three comparable options that the planner can evaluate.
- Connecting idea: with the new requirements agreed, the model must change to express them, which
  completes the validation of the change.

### 14. The new requirement changes the optimization

- First establish the maximum achievable revenue, $R^*$.
- For each allowance $a$, maximize customers served while requiring revenue of at least $(1-a)R^*$.
- Preserve whole-shipment decisions and the hard weight limit.
- Connecting idea: the model has changed; verification starts by asking where in the software
  that change lands.

## Part III — Verification: implement and check the change

### 15. Audience: trace the request through the software

- Revisit the diagram of inputs, validation, solving, and presentation.
- Identify which responsibilities the new request affects.
- Explain one connection between a business requirement and a software change.
- Answer: data reading and validation barely change, since the customer is already in the data.
  Solving changes most: first find $R^*$, then maximize customers served for each allowance.
  Presentation changes from one load to three options. Example connection: "count each customer
  once" becomes one yes/no variable per customer that can be 1 only if one of its shipments flies.
- Connecting idea: the trace was easy to follow only because each responsibility lives in one
  place; next, how design makes that possible.

### 16. Design makes the effects of change understandable

- Give data handling, optimization, and presentation clear responsibilities.
- Make the affected components and their interactions explicit.
- Organize the software so those responsibilities can be checked independently.
- Connecting idea: responsibilities that can be checked one at a time invite the question of what
  evidence would show the change works; the audience proposes it.

### 17. Audience: propose evidence that the change works

- Design a small example that catches counting shipments instead of customers.
- Write the expected result before running anything.
- Propose one additional check for revenue allowance or aircraft weight.
- Answer: a flight where counting shipments and counting customers disagree. Example: limit
  200 kg; Atlas Steel has three 60 kg shipments, Bighorn Auto and Cedar Pharma one 100 kg shipment
  each, and the allowance is large enough that revenue does not bind. Counting shipments loads
  Atlas's three (3 shipments, 1 customer); counting customers serves 2 (for example Bighorn and
  Cedar). Expected result, written first: 2 customers served. Extra checks: the weight limit is
  never exceeded; revenue is at least $(1-a)R^*$; with a 0% allowance the answer equals the
  original optimum.
- Connecting idea: the audience's proposed evidence is now compared with the prepared tests, run
  live.

### 18. Tests check the new behavior and protect existing behavior

- Check that the original revenue-maximizing behavior still works.
- Check customer counting, revenue allowances, and physical feasibility.
- Run the prepared tests and connect their results to the user stories and examples; tests are the
  verification evidence.
- Connecting idea: the tests pass, so the change is verified and can go back to the planner.

## Part IV — Back to the planner: use, feedback and the next cycle

### 19. Put the tested version into use

- Demonstrate the prepared local update.
- Launch the changed program on the same flight.
- Compare loaded shipments, revenue, and customers served across three options.
- Connecting idea: the program offers three options but does not decide; the planner does, so the
  audience takes the planner's seat.

### 20. Audience: choose a load and defend your decision

- Choose one of the three options with your partner.
- Explain the revenue-service tradeoff behind your choice.
- Identify one piece of missing information that could change your decision.
- Answer: there is no single right option; I am looking for a choice defended with the numbers.
  On SC101, serving 4, 5 or 6 customers instead of 2 gives up $400 (4.2%), $800 (8.3%) or
  $1,500 (15.6%). Missing information that could change the choice: service history, urgent
  deadlines, whether partial delivery is useful, and future customer relationships.
- Connecting idea: the information you missed while choosing is exactly the planner's feedback,
  and it starts the next cycle.

### 21. Planner feedback starts the next learning cycle

- Visual: the cycle from slide 5 again, with the arrow from feedback back to the business request
  highlighted.
- Service history and urgent deadlines may affect the planner's choice.
- Partial-delivery usefulness and future customer relationships may also matter.
- Recurring missing information can become a requirement for the next version; feedback from use
  is validation starting again.
- Connecting idea: each pass through the cycle drew on business understanding, modeling, design
  and testing, which are skills that build careers.

### 22. These activities connect to professional skills

- Business understanding, modeling, software design, and testing contribute to usable decisions.
- Connect those skills to Francisco's experience and students' career opportunities.
- Share the repository, SEFOP reading, and discussion link.
- Connecting idea: with the materials shared, the floor opens for questions.

### 23. Questions and discussion

- What remains unclear about turning a business request into decision-support software?
- Where would you apply learning and adaptation in your own project?
- Connecting idea: there is no next slide; the next business request starts validation and
  verification again, back round the cycle of slide 5.

## Pacing

Pair discussions are included in these blocks.

| Minutes | Part | Slides | Focus |
| --- | --- | --- | --- |
| 0-14 | I | 1-5 | DSS characteristics, trusting a recommendation, validation and verification, a DSS is software, learning and adaptation, and the cycle of working on a DSS |
| 14-30 | I | 6-10 | Original business request, requirements, knapsack derivation, software, and run |
| 30-45 | II | 11-14 | Example change, clarification, acceptance criteria and model change |
| 45-65 | III | 15-18 | Software trace, design, proposed evidence and tests |
| 65-80 | IV | 19-22 | Local deployment, audience decision, feedback, careers, and next steps |
| 80-90 | IV | 23 | Questions and discussion |

## Pair activity routine

Allow 30-45 seconds of individual thinking, then 1-2 minutes of pair discussion.
Each pair records one answer and alternates who writes. Hear two contrasting responses,
connect their reasoning to the requirements, design or evidence, and let everyone revise
their notes. Give the planner interview and final decision more discussion time.

Pairs keep four sections in their notes: business request, example change, evidence, and decision.
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

The customer-service change is prepared. A customer is served if at least one of their shipments
flies, and each customer counts once. The three revenue-sacrifice allowances remain to be agreed.
Aircraft weight is hard in both versions. The planner makes the final decision; the four examples
of omitted information on slide 21 are discussion material, not implemented objectives.

Deployment is local on Francisco's machine, without separate development, staging or production
environments. The remaining demonstration decisions are listed in
[instructions.md](instructions.md#what-to-settle-first).
