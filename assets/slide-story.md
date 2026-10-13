# Agreed workshop slide story

The agreed structure is 15 slides for a 90-minute workshop, including questions.
No code is written during the workshop. All artifacts are prepared; the program and tests run
live. The audience participates through the planner interview, acceptance criteria, test
predictions and choosing among options.

One business request drives the entire lifecycle: serve more customers within specified revenue
allowances. The requirements table stays visible as the request is connected to the model,
software, acceptance criteria and tests. Careers and SEFOP connect the work to students' next steps.

## Slide list

| # | Slide title | Main idea to deliver |
| --- | --- | --- |
| 1 | What should go on this flight? | Introduce the planner's decision and the original revenue-maximizing knapsack. Run it to establish the starting point. |
| 2 | The business asks for more | The planner also wants to serve more customers. This competing objective creates a reason for the model to evolve. |
| 3 | Interview the planner before changing anything | The audience discovers what "served" means, how much revenue can be sacrificed, and what information the planner needs. |
| 4 | Requirements need acceptance criteria | Build the central requirements table: count distinct customers, preserve hard limits, respect revenue allowances, and present three comparable options. Define how each requirement will be checked. |
| 5 | Evolve the model from the business request | Connect shipments to customers. Establish maximum revenue, then maximize customers served within each permitted revenue sacrifice. |
| 6 | Design the software around the decision | Trace inputs, validation, solving, and presentation through a simple diagram. Explain how the program generates and communicates the three options. |
| 7 | What evidence would convince us? | Ask the audience to propose tests. Preserve existing behavior and check the new feature, including counting a customer only once when several shipments fly. |
| 8 | Run the checks | Run the prepared tests live and connect the results to the acceptance criteria. Show how testing supports changing the system confidently. |
| 9 | Put the tested change into use | Demonstrate the local deployment: update the runnable program to the tested version and launch it. |
| 10 | Same flight. Three new options. | Run the updated console program. Compare loaded shipments, cargo left behind, revenue, and customers served side by side. |
| 11 | You are the planner: choose an option | The audience chooses a load and explains the revenue-service tradeoff behind its decision. |
| 12 | What could change your choice? | Discuss information the model may lack: service history, useful partial deliveries, urgent deadlines, and future customer relationships. |
| 13 | A decision-support system keeps evolving | The planner makes the final decision. Recurring missing information can become the next requirement, restarting the lifecycle. |
| 14 | Your place in this work—and where to start | Connect each lifecycle step to career skills and Francisco's experience. Provide the repository QR code, SEFOP reading, and discussion link. |
| 15 | Questions and discussion | Invite questions about the business decision, model evolution, software process, and careers. |

## Pacing

| Minutes | Slides | Focus |
| --- | --- | --- |
| 0-10 | 1-2 | Original decision and business change |
| 10-28 | 3-4 | Interactive interview, requirements, acceptance criteria |
| 28-43 | 5-6 | Model and software design |
| 43-55 | 7-8 | Interactive testing discussion and live checks |
| 55-67 | 9-11 | Local deployment, console demonstration, audience choice |
| 67-75 | 12-13 | Missing information and continued evolution |
| 75-80 | 14 | Careers and SEFOP |
| 80-90 | 15 | Questions |

## Agreed business definitions

- A customer is served if at least one of their shipments flies. Several loaded shipments for
  that customer still count once.
- The original knapsack maximizes revenue within hard physical limits.
- The change maximizes distinct customers served for three acceptable revenue-sacrifice
  allowances relative to maximum achievable revenue. The allowance values remain to be agreed.
- Physical limits remain hard in both versions.
- The planner has information the model may lack. All four examples on slide 12 are discussion
  material; none is assumed to be part of the current model.
- The lifecycle walkthrough follows one requirement using prepared checkpoints, with only enough
  mathematics and architecture to explain the design decisions. Deployment is local, without
  separate development, staging or production environments.

The remaining demonstration decisions are listed in
[instructions.md](instructions.md#what-to-settle-first). Settle them before implementation.
