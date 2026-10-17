# Agreed workshop slide story

The agreed structure is 22 slides for a 90-minute workshop, including questions.
No code is written during the workshop. All artifacts are prepared; the program and tests run
live. Attendees discuss the proposed questions in pairs and record their answers on ordinary
paper or in a notebook.

The story moves from general principles to a concrete example: recurring business decisions
require software; before a recommendation can be trusted, production needs two kinds of evidence:
validation (the right problem) and verification (the problem solved right); a decision-support
system is software, and because software is fragile and built with imperfect information,
obtaining and keeping that evidence requires learning quickly and adapting quickly and safely;
engineering practices support those abilities. The original cargo business request leads to a
knapsack model and a runnable system. Only then does an example business change introduce customer service and demonstrate how
the model and software evolve.

The workshop has four parts. Part I sets out the principles and builds the baseline system for
the original request. Part II validates the business change: what the planner needs and how the
model must change. Part III verifies it: how the software changes and what evidence shows it
works. Part IV returns to the planner, whose use and feedback start validation again.

The requirements table starts with the original request and grows when the change arrives.
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

- Imagine the solver reports "optimal."
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

### 3. Production requires validation and verification

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
- Connecting idea: these principles stay abstract until they are applied, so one concrete DSS now
  carries them through the rest of the workshop.

### 5. Our example DSS: choosing the cargo for each flight

- Visual: `assets/planner_image.png` (illustrative; its numbers are not those of flight SC101).
- Every flight, more shipments are waiting than the aircraft can carry, and a load planner
  decides which ones fly: a recurring decision, the kind a decision-support system supports.
- The original request is to maximize revenue within the weight limit.
- Each shipment must fly whole or stay behind.
- Connecting idea: the request sounds clear, but a model built on an untested assumption is a
  validation risk, so the audience clarifies it with the planner first.

### 6. Audience: clarify the planner's request

- Identify the business objective and the hard limit.
- Propose one question to ask before building the model.
- Record the planner's answer with your partner.
- Answer: the objective is to maximize revenue; the hard limit is the aircraft's weight. Useful
  questions: may the weight limit ever be exceeded? (never); can a shipment be split? (no, it flies
  whole or stays); is volume a limit too? (not in this version); must some shipments fly? (no).
- Connecting idea: the planner's answers must be written down in a form we can check:
  requirements with acceptance criteria.

### 7. Requirements tell us what success means

- Start the shared requirements table with revenue maximization and aircraft weight.
- Connect each requirement to an observable acceptance criterion; this is how validation becomes
  checkable.
- Keep this table as a reference throughout the workshop.
- Connecting idea: the agreed requirements now become mathematics, the first translation, from
  business problem to math model.

### 8. The business rules lead to a knapsack model

- Whole-shipment choices become binary variables: $x_i \in \{0,1\}$.
- Revenue maximization becomes $\max \sum_i r_i x_i$.
- Aircraft capacity becomes $\sum_i w_i x_i \leq W$.
- Connecting idea: a model on paper recommends nothing; the second translation, from math model
  to coded model, turns it into a program the planner can run.

### 9. Software turns the model into a usable recommendation

- Read and validate the flight's data.
- Prepare the instance, solve it, and present the result.
- Run the original program and interpret the proposed load.
- Connecting idea: the baseline works and the planner uses it, and then the business asks for
  something new.

## Part II — Validation: define and model the change

### 10. The system must support new business needs

- Business objectives and rules can evolve.
- Example request: serve more customers within acceptable revenue sacrifices.
- Aircraft weight remains a hard limit.
- Connecting idea: "serve more customers" can be read in several ways, so before changing
  anything the audience clarifies the new request.

### 11. Audience: clarify the new request

- What exactly does "a customer is served" mean?
- How much revenue may be sacrificed, and relative to what baseline?
- What output would help the planner compare alternatives?
- Answer: a customer is served when at least one of its shipments flies, and counts once however
  many fly. Revenue sacrifice is measured against the maximum achievable revenue, $R^*$, as a
  percentage, for example 5%, 10% and 20%. The planner needs the options side by side: loaded
  shipments, revenue, revenue given up and customers served.
- Connecting idea: the clarified answers extend the requirements table with new acceptance
  criteria.

### 12. Extend the requirements and acceptance criteria

- Count distinct customers; several loaded shipments for one customer count once.
- Respect each agreed revenue allowance and the aircraft weight limit.
- Present three comparable options that the planner can evaluate.
- Connecting idea: with the new requirements agreed, the model must change to express them, which
  completes the validation of the change.

### 13. The new requirement changes the optimization

- First establish the maximum achievable revenue, $R^*$.
- For each allowance $a$, maximize customers served while requiring revenue of at least $(1-a)R^*$.
- Preserve whole-shipment decisions and the hard weight limit.
- Connecting idea: the model has changed; verification starts by asking where in the software
  that change lands.

## Part III — Verification: implement and check the change

### 14. Audience: trace the request through the software

- Revisit the diagram of inputs, validation, solving, and presentation.
- Identify which responsibilities the new request affects.
- Explain one connection between a business requirement and a software change.
- Answer: data reading and validation barely change, since the customer is already in the data.
  Solving changes most: first find $R^*$, then maximize customers served for each allowance.
  Presentation changes from one load to three options. Example connection: "count each customer
  once" becomes one yes/no variable per customer that can be 1 only if one of its shipments flies.
- Connecting idea: the trace was easy to follow only because each responsibility lives in one
  place; next, how design makes that possible.

### 15. Design makes the effects of change understandable

- Give data handling, optimization, and presentation clear responsibilities.
- Make the affected components and their interactions explicit.
- Organize the software so those responsibilities can be checked independently.
- Connecting idea: responsibilities that can be checked one at a time invite the question of what
  evidence would show the change works; the audience proposes it.

### 16. Audience: propose evidence that the change works

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

### 17. Tests check the new behavior and protect existing behavior

- Check that the original revenue-maximizing behavior still works.
- Check customer counting, revenue allowances, and physical feasibility.
- Run the prepared tests and connect their results to the requirements table; tests are the
  verification evidence.
- Connecting idea: the tests pass, so the change is verified and can go back to the planner.

## Part IV — Back to the planner: use, feedback and the next cycle

### 18. Put the tested version into use

- Demonstrate the prepared local update.
- Launch the changed program on the same flight.
- Compare loaded shipments, revenue, and customers served across three options.
- Connecting idea: the program offers three options but does not decide; the planner does, so the
  audience takes the planner's seat.

### 19. Audience: choose a load and defend your decision

- Choose one of the three options with your partner.
- Explain the revenue-service tradeoff behind your choice.
- Identify one piece of missing information that could change your decision.
- Answer: there is no single right option; I am looking for a choice defended with the numbers.
  On SC101, serving 4, 5 or 6 customers instead of 2 gives up $400 (4.2%), $800 (8.3%) or
  $1,500 (15.6%). Missing information that could change the choice: service history, urgent
  deadlines, whether partial delivery is useful, and future customer relationships.
- Connecting idea: the information you missed while choosing is exactly the planner's feedback,
  and it starts the next cycle.

### 20. Planner feedback starts the next learning cycle

- Service history and urgent deadlines may affect the planner's choice.
- Partial-delivery usefulness and future customer relationships may also matter.
- Recurring missing information can become a requirement for the next version; feedback from use
  is validation starting again.
- Connecting idea: each pass through the cycle drew on business understanding, modeling, design
  and testing, which are skills that build careers.

### 21. These activities connect to professional skills

- Business understanding, modeling, software design, and testing contribute to usable decisions.
- Connect those skills to Francisco's experience and students' career opportunities.
- Share the repository, SEFOP reading, and discussion link.
- Connecting idea: with the materials shared, the floor opens for questions.

### 22. Questions and discussion

- What remains unclear about turning a business request into decision-support software?
- Where would you apply learning and adaptation in your own project?
- Connecting idea: there is no next slide; the next business request starts validation and
  verification again, back at slide 1.

## Pacing

Pair discussions are included in these blocks.

| Minutes | Part | Slides | Focus |
| --- | --- | --- | --- |
| 0-12 | I | 1-4 | DSS characteristics, trusting a recommendation, validation and verification, a DSS is software, and learning and adaptation |
| 12-30 | I | 5-9 | Original business request, requirements, knapsack derivation, software, and run |
| 30-45 | II | 10-13 | Example change, clarification, acceptance criteria and model change |
| 45-65 | III | 14-17 | Software trace, design, proposed evidence and tests |
| 65-80 | IV | 18-21 | Local deployment, audience decision, feedback, careers, and next steps |
| 80-90 | IV | 22 | Questions and discussion |

## Pair activity routine

Allow 30-45 seconds of individual thinking, then 1-2 minutes of pair discussion.
Each pair records one answer and alternates who writes. Hear two contrasting responses,
connect their reasoning to the requirements, design or evidence, and let everyone revise
their notes. Give the planner interview and final decision more discussion time.

Pairs keep four sections in their notes: business request, example change, evidence, and decision.
The presenter records clarification questions in the requirements table, annotates the software
diagram with predictions, and compares proposed tests with the prepared checks.

## Demonstration boundaries

The customer-service change is prepared. A customer is served if at least one of their shipments
flies, and each customer counts once. The three revenue-sacrifice allowances remain to be agreed.
Aircraft weight is hard in both versions. The planner makes the final decision; the four examples
of omitted information on slide 20 are discussion material, not implemented objectives.

Deployment is local on Francisco's machine, without separate development, staging or production
environments. The remaining demonstration decisions are listed in
[instructions.md](instructions.md#what-to-settle-first).
