# Agreed workshop slide story

The agreed structure is 22 slides for a 90-minute workshop, including questions.
No code is written during the workshop. All artifacts are prepared; the program and tests run
live. Attendees discuss the proposed questions in pairs and record their answers on ordinary
paper or in a notebook.

The story moves from general principles to a concrete example: recurring business decisions
require software; building that software requires learning quickly and adapting quickly and
safely; engineering practices support those abilities. The original cargo business request leads
to a knapsack model and a runnable system. Only then does an example business change introduce
customer service and demonstrate how the model and software evolve.

The requirements table starts with the original request and grows when the change arrives.
The same software diagram is revisited to trace the affected responsibilities. Audience questions,
test proposals and decisions contribute to the walkthrough.

## Slides

### 1. A decision-support system supports recurring business decisions

- Combines data, business rules, and mathematical models.
- Produces recommendations repeatedly as new inputs arrive.
- Helps a person make and act on a decision.

### 2. Building decision-support software requires learning and adaptation

- Requirements and model assumptions begin with incomplete information.
- Small errors can produce plausible but incorrect recommendations.
- Teams must learn quickly and adapt their software quickly and safely.

### 3. Audience: what would you need before trusting a recommendation?

- Imagine the solver reports "optimal."
- With your partner, identify two things you still need to know before acting.
- Write one question you would ask the team that built the system.

### 4. The engineering lifecycle supports learning and adaptation

- Requirements and acceptance criteria make expectations explicit.
- Design and tests help teams implement and check changes.
- Use and feedback reveal what the next iteration needs.

### 5. The planner needs to decide what flies

- Shipments are waiting, and the aircraft cannot carry everything.
- The original request is to maximize revenue within the weight limit.
- Each shipment must fly whole or stay behind.

### 6. Audience: clarify the planner's request

- Identify the business objective and the hard limit.
- Propose one question to ask before building the model.
- Record the planner's answer with your partner.

### 7. Requirements tell us what success means

- Start the shared requirements table with revenue maximization and aircraft weight.
- Connect each requirement to an observable acceptance criterion.
- Keep this table as a reference throughout the workshop.

### 8. The business rules lead to a knapsack model

- Whole-shipment choices become binary variables: $x_i \in \{0,1\}$.
- Revenue maximization becomes $\max \sum_i r_i x_i$.
- Aircraft capacity becomes $\sum_i w_i x_i \leq W$.

### 9. Software turns the model into a usable recommendation

- Read and validate the flight's data.
- Prepare the instance, solve it, and present the result.
- Run the original program and interpret the proposed load.

### 10. The system must support new business needs

- Business objectives and rules can evolve.
- Example request: serve more customers within acceptable revenue sacrifices.
- Aircraft weight remains a hard limit.

### 11. Audience: clarify the new request

- What exactly does "a customer is served" mean?
- How much revenue may be sacrificed, and relative to what baseline?
- What output would help the planner compare alternatives?

### 12. Extend the requirements and acceptance criteria

- Count distinct customers; several loaded shipments for one customer count once.
- Respect each agreed revenue allowance and the aircraft weight limit.
- Present three comparable options that the planner can evaluate.

### 13. The new requirement changes the optimization

- First establish the maximum achievable revenue, $R^*$.
- For each allowance $a$, maximize customers served while requiring revenue of at least $(1-a)R^*$.
- Preserve whole-shipment decisions and the hard weight limit.

### 14. Audience: trace the request through the software

- Revisit the diagram of inputs, validation, solving, and presentation.
- Identify which responsibilities the new request affects.
- Explain one connection between a business requirement and a software change.

### 15. Design makes the effects of change understandable

- Give data handling, optimization, and presentation clear responsibilities.
- Make the affected components and their interactions explicit.
- Organize the software so those responsibilities can be checked independently.

### 16. Audience: propose evidence that the change works

- Design a small example that catches counting shipments instead of customers.
- Write the expected result before running anything.
- Propose one additional check for revenue allowance or aircraft weight.

### 17. Tests check the new behavior and protect existing behavior

- Check that the original revenue-maximizing behavior still works.
- Check customer counting, revenue allowances, and physical feasibility.
- Run the prepared tests and connect their results to the requirements table.

### 18. Put the tested version into use

- Demonstrate the prepared local update.
- Launch the changed program on the same flight.
- Compare loaded shipments, revenue, and customers served across three options.

### 19. Audience: choose a load and defend your decision

- Choose one of the three options with your partner.
- Explain the revenue-service tradeoff behind your choice.
- Identify one piece of missing information that could change your decision.

### 20. Planner feedback starts the next learning cycle

- Service history and urgent deadlines may affect the planner's choice.
- Partial-delivery usefulness and future customer relationships may also matter.
- Recurring missing information can become a requirement for the next version.

### 21. These activities connect to professional skills

- Business understanding, modeling, software design, and testing contribute to usable decisions.
- Connect those skills to Francisco's experience and students' career opportunities.
- Share the repository, SEFOP reading, and discussion link.

### 22. Questions and discussion

- What remains unclear about turning a business request into decision-support software?
- Where would you apply learning and adaptation in your own project?

## Pacing

Pair discussions are included in these blocks.

| Minutes | Slides | Focus |
| --- | --- | --- |
| 0-12 | 1-4 | DSS characteristics, learning and adaptation, and the engineering lifecycle |
| 12-30 | 5-9 | Original business request, requirements, knapsack derivation, software, and run |
| 30-65 | 10-17 | Example change, clarification, acceptance criteria, model and software adaptation, and tests |
| 65-80 | 18-21 | Local deployment, audience decision, feedback, careers, and next steps |
| 80-90 | 22 | Questions and discussion |

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
