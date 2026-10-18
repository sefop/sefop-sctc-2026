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

## Visual conventions

- Format reference: `C:/Users/zente/Github/sefop-training-hub/workshops/2026-10-25-agifors-annual-symposium/Zenteno Smith - 2026 - Rethinking the embedded OR team a a specialized software team.pptx`.
- Follow its 16:9 format, Aptos Display headings, Aptos body text, pale background, navy
  typography and orange accents. Reference colors: pale `#F7F8FA`, navy `#0F2343` and
  `#07142B`, and orange `#F97316`. Slide 12 retains the book's green, yellow and blue test-level
  colors to connect its two figures.
- Each slide's `Visual` bullet specifies its agreed composition and on-screen text. The other
  content, answers, explanations and connecting ideas are speaking points for presenter notes,
  unless explicitly included in the visual. Keep illustrations and diagrams large and readable,
  with generous empty space.
- Supporting references are in `C:/Users/zente/Github/sefop-training-hub/book` and
  `C:/Users/zente/Github/sefop-training-hub/workshops`. `Purdue_Workshop.pptx` refers to the deck
  under `workshops/2026-06-29-purdue/` in that repository.

## Part I — Introduction: principles and the example

### 1. A decision-support system supports recurring business decisions

- Visual: use the AGIFORS template's pale background, navy Aptos Display heading, and orange
  accents. Across the slide, place three large, evenly spaced illustrations adapted from slide 2
  of the AGIFORS 2026 deck: fleet planning, crew scheduling, and disruption recovery. Under each,
  show only a short decision label and its cadence: "Plan the fleet / Annually", "Schedule crews /
  Monthly", and "Recover operations / Daily". Emphasize the cadence words in orange. Keep generous
  empty space and omit explanatory body bullets. Presenter notes carry the definition of a DSS,
  its combination of data, business rules and mathematics, the person's role in acting on the
  recommendation, and the transition to trust.
- Combines data, business rules, and mathematical models.
- Produces recommendations repeatedly as new inputs arrive.
- Helps a person make and act on a decision.
- Connecting idea: a DSS is only useful if people act on its recommendations, so what would make
  you trust one?

### 2. Audience: what would you need before trusting a recommendation?

- Visual: on the AGIFORS template's pale background, place a large screen on the left displaying
  only "OPTIMAL" in navy. On the right, show a person considering the result, with a large orange
  question mark between the screen and the person. Keep the composition spacious. Along the
  bottom, show the short activity instruction: "Discuss in pairs: two things you need to know;
  one question for the team." Presenter notes hold the activity routine, suggested answers,
  debrief and transition to validation and verification. Do not show answer categories or other
  clues before the audience discusses.
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

- Visual: adapt the book's `05-testing/assets/intro-verification-validation.svg` into the
  AGIFORS template's pale background, navy Aptos text and orange accents. Across the slide, show
  three large stages with simple icons: "Business problem → Mathematical model → Code". Under
  the first translation, place a bracket labeled "Validation" with "The right problem?";
  under the second, place a matching bracket labeled "Verification" with "Solved right?".
  Give both translations equal visual weight and keep the complete diagram visible at once.
  Omit the book figure's section-specific emphasis and explanatory body text. Presenter notes
  hold the full definitions, the consulting and software responsibilities, links back to the
  audience's questions, and why both kinds of evidence are needed before deployment.
- Validation asks "are we solving the right problem?": do the model's objective and rules match
  the business's real decision? It is a consulting problem, answered with requirements,
  acceptance criteria, and feedback from use.
- Verification asks "are we solving the problem right?": does the code compute exactly what the
  model states? It is a software problem, answered with design and automated tests. A
  recommendation goes to production only when both hold.
- Connecting idea: both kinds of evidence pass through code, so next comes why software makes them
  hard to obtain and keep.

### 4. A decision-support system is software, so the rules of software apply

- Visual: use two balanced panels on the AGIFORS template's pale background. Label the left
  panel "Research" and show five illustrated research papers, each stamped "RETRACTED", with
  the short caption "A data-processing error". Label the right panel "Industry" and reuse the
  Ariane 5 explosion photograph from slide 6 of `Purdue_Workshop.pptx`, with the short caption
  "An unhandled overflow". Use navy text and restrained orange accents, generous spacing and
  no explanatory body bullets. Presenter notes carry both stories, their details and sources,
  and the connection to software that produces business recommendations.
- Validation and verification are hard to obtain and keep because a DSS is software: every
  recommendation passes through code that reads data, builds a model and reports the result.
  Software principles apply whether we know them or not: a sign error in a data-processing script
  retracted five published papers, and an unhandled overflow in reused code destroyed the Ariane 5
  rocket 37 seconds after launch.
- So trustworthy recommendations need software engineering, not only good mathematics.
- Connecting idea: next, the big picture: the cycle that takes a request all the way to the user.

### 5. The big picture: working on a DSS is a cycle

- Visual: on the AGIFORS template's pale background, draw a large, spacious circular journey
  with eight short labels and simple icons: "Request → Requirements → Model → Design & code →
  Tests → Deploy → Use → Feedback", with feedback returning to the next request. Mark the arc
  from request through requirements to model "Validation", and the arc from design and code
  through tests "Verification", with equal visual emphasis. Put a person at "Use" to show that
  the user makes the decision. Use navy text and arrows, emphasizing the return from feedback to
  request in orange. Show the complete loop at once, without explanatory body bullets. Presenter
  notes hold the workshop's four-part map, what each stage means, and the point that a change
  helps the user once deployed. Reuse this same layout on slide 15 to highlight the second turn.
- One pass takes a request all the way to the user: a change helps the user only once it is
  deployed.
- Map of the workshop: Part I introduces the example; Part II validates the planner's request;
  Part III verifies the first version; Part IV zooms out: the cycle runs again, then what this
  profession needs and where to keep learning.
- Connecting idea: to see the cycle at work, we now follow one concrete DSS round it.

### 6. Our example DSS: choosing the cargo for each flight

- Visual: beneath the AGIFORS-style title, use one wide, realistic scene. A load planner at a
  desk occupies the left foreground; through a large window, a cargo aircraft is being loaded,
  with shipments waiting nearby. The computer screen contains only indistinct shapes. Use the
  image as the main visual, without explanatory captions or body bullets. No readable text,
  numbers, formulas, ticks or shipment-selection cues appear anywhere in the scene. Prepare a
  clean replacement for `planner_image.png`, whose objective, capacity display and shipment
  statuses would reveal the interview's answers. Presenter notes introduce the recurring cargo
  decision, that not everything can fly, and the second-hand request that leads to the interview.
- Every flight, more shipments are waiting than the aircraft can carry, and a load planner
  decides which ones fly: a recurring decision, the kind a decision-support system supports.
- What the planner wants from a tool is not yet clear: it reaches us second-hand.
- Connecting idea: the request arrives as one vague sentence from a manager, so the audience must
  find out from the planner what is really needed.

## Part II — Validation: are we solving the right problem?

### 7. Audience: interview the planner to find the requirements

- Visual: use the AGIFORS template's pale background, navy typography and orange accents. Put
  a small illustration of the planner from slide 6 in the center, surrounded by six clearly
  spaced prompts: "Decisions", "Objectives", "Constraints", "Data", "Uncertainty", and "Risks".
  Above, show the manager's request in a speech bubble: "I heard our cargo planner wants a tool
  that picks the best shipments for each flight." Below, show "Pairs · 1 minute · 2 questions".
  Give the prompts equal visual weight and show no answers or completed requirements. Presenter
  notes hold the full interview protocol, the planner's script, the user-story pattern, and the
  instruction to record each answer and turn the requirements into user stories.
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

- Visual: use two compact three-row tables side by side on the AGIFORS template's pale
  background. Label them "Example 1" and "Example 2", each with "500 kg limit" above it and
  columns "Customer", "Weight", and "Revenue". Use the exact customers and values below.
  Mark selected rows with an orange outline and a check; keep unselected rows unaccented.
  Beneath the first table, show "Bighorn + Cedar · $3,800 · 500 kg" prominently; beneath the
  second, show "Atlas · $3,000 · 300 kg". Use generous spacing, navy text and no explanatory
  paragraphs. Presenter notes carry the reasoning behind each choice and explain that these
  situations and expected decisions are acceptance criteria. Refer to example 1 in slide 12's
  presenter notes and reuse example 2's table on slide 14.
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

- Visual: on the AGIFORS template's pale background, use three spacious rows with a business
  rule on the left, an orange translation arrow in the middle, and a large mathematical
  statement on the right. Row 1: "Each shipment flies whole or stays" → $x_i \in \{0,1\}$.
  Row 2: "Earn the most revenue" → $\max \sum_i r_i x_i$. Row 3: "Stay within the weight limit"
  → $\sum_i w_i x_i \leq W$. Keep all three rows visible together and use navy text. A compact
  footer defines $i$ as a shipment, $x_i$ as its fly-or-stay choice, $r_i$ as its revenue, $w_i$
  as its weight and $W$ as the aircraft's weight limit. Add no explanatory body paragraphs.
  Presenter notes connect each statement to the interview and examples, explain the notation,
  and introduce the next translation from the mathematical model to code.
- Whole-shipment choices become binary variables: $x_i \in \{0,1\}$.
- Revenue maximization becomes $\max \sum_i r_i x_i$.
- Aircraft capacity becomes $\sum_i w_i x_i \leq W$.
- Connecting idea: a model on paper recommends nothing; the second translation, from math model
  to coded model, is where verification begins.

## Part III — Verification: are we solving the problem right?

### 10. Software is a different kind of engineering

- Visual: adapt slide 10 of `Purdue_Workshop.pptx` to the AGIFORS template's pale background,
  navy typography and orange accents. Reuse its construction-site and software-developer
  photographs, equally sized side by side. Under "Civil engineering", show "Requirements
  largely known" and "Small errors tolerated". Under "Software engineering", show "Requirements
  emerge" and "Tiny errors can matter". Use an orange footer: "Learn quickly · Change quickly
  and safely". Keep the complete comparison visible, with no explanatory body paragraphs.
  Presenter notes explain the comparison, software's flexibility and fragility, why building
  reveals requirements, and how design and testing support quick, safe change.
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
- Visual: on the AGIFORS template's pale background, show two large diagrams side by side,
  adapting the book's `04-design/assets/forces-without-with.svg` to a simpler comparison. On
  the left, six module boxes form a dense web of connections; on the right, the same six boxes
  have clear boundaries and fewer connections. Add small, visibly separate test boxes beside
  the modules on the right, with short links showing which module each test checks. Highlight
  one module in orange in each diagram, keeping the other modules navy or neutral. Use only
  the short captions "Changes spread" and "Changes stay manageable". Keep both diagrams visible
  together, without explanatory body bullets. Presenter notes explain modules and connections,
  how boundaries help contain changes and make modules testable, and how tests check behavior.
  Clarify that design makes changes manageable; it does not guarantee every change touches only
  one module. The next slide explains what the separate test boxes actually do.
- Connecting idea: here we show the purpose of modularization, in the next slide we show how to 
evaluate a change.

### 12. What an automated test is

- A test is a small program that runs the code on a case whose right answer is known and checks
  the result. It has three steps: arrange the case, act by running the code, assert the expected
  result.
- Visual: simplify and combine the book's `05-testing/assets/unit-test-pyramid.svg` and
  `05-testing/assets/unit-test-levels.svg` on the AGIFORS template's pale background with navy
  Aptos typography. Place a small three-level pyramid on the left. On the right, use three
  large columns, each showing the same simple program as a vertical chain: "Read → Compute →
  Report". In the "Unit" column, highlight one module; in "Integration", highlight connected
  modules tested together; in "End-to-end", highlight the whole program. Match those scopes
  to the pyramid's green unit level, yellow integration level and blue end-to-end level. Keep
  the shapes large and simple, and show both figures together. Along the bottom, show "Arrange
  → Act → Assert", with "Set up → Run → Check" beneath it. Keep the pyramid's cost, speed and
  test-count explanations in presenter notes. Notes also explain that every scope runs code
  and checks an expected result, and apply the three steps to example 1 of slide 8: arrange
  the 500 kg flight and its three shipments; ask for a load; check that Bighorn and Cedar fly,
  earning $3,800 at 500 kg. The notes explain automatic execution and repetition after changes.
- A test runner runs every test automatically, in seconds, with the same result each time; a
  failed check names exactly what broke. Run after every change, it shows at once whether the
  change broke something.
- Connecting idea: with design and tests understood, here is how they look in our example,
  starting with its design.

### 13. A DSS example design

- Visual: on the AGIFORS template's pale background, show five equally sized boxes with
  simple icons across the slide, joined by orange arrows: "Read data → Preprocess → Solve →
  Postprocess → Result". Use navy text and the exact stage names printed by the program,
  giving every stage equal visual weight. Keep the complete pipeline visible at once. A small
  footer reads "SC101 · Live demonstration". Show no code, source paths or console screenshot
  on the slide. Presenter notes hold `python -m cli optimize_cargo SC101`, explain each stage's
  responsibility, and guide the live console run and repository tour. Notes map the first and
  last stages to `adapters/json_data_loader.py` and `adapters/console_result_writer.py`, and the
  middle stages to the folders under `use_cases/solving/`. Explain that arrows show execution
  flow, then interpret the proposed load with the audience.
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

- Visual: use the AGIFORS template's pale background, navy typography and orange accents.
  On the left, reuse example 2's table from slide 8, with "500 kg limit" above it and
  "Expected: Atlas · $3,000 · 300 kg" below it. On the right, place two large question cards
  beneath "Would this test catch…": "Ignoring the weight limit?" and "Splitting a shipment?".
  A small footer reads "Predict in pairs · Explain why". Show no answers, fault outcomes or
  pass/fail marks before the discussion. Presenter notes hold the pair routine and debrief,
  connect the expected load to the automated assertions, and guide the switch to the repository
  and live test run. Keep code and test-runner output in the live demonstration.
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

- Visual: reuse slide 5's complete eight-stage circular journey, keeping its layout and labels
  recognizable on the AGIFORS template's pale background. Near "Use", add a compact callout of
  six customer icons: two filled and four outlined, labeled "2 of 6 customers served". Near
  "Feedback", add a planner's speech bubble asking "Can we serve more customers?". Emphasize
  the return from feedback to "Request" in orange, keeping the remaining stages readable in
  navy. Presenter notes explain the acceptable revenue sacrifice and trace the next turn through
  user stories, examples, a revised model, design, tests, deployment and use. This visual
  introduces the next iteration; the customer-service feature is not built or demonstrated.
- In use, the planner notices that four of the six customers get nothing on a flight, and asks
  the tool to serve more customers within an acceptable revenue sacrifice.
- The request goes round the same cycle: validate it with user stories, examples and a new model;
  verify it with design and tests; deploy it; use it. Modular, tested software is what makes the
  second round fast and safe.
- Connecting idea: every round asks for the same skills; zooming out, here is what this
  profession needs.

### 16. What this profession needs

- Visual: on the AGIFORS template's pale background, use three equally weighted, evenly spaced
  columns. Each contains one large, simple navy icon with a restrained orange accent and one
  label: "Business skills", "Software skills", and "People skills". Use a business/chart icon,
  a software/module icon, and a conversation/team icon respectively. Keep generous empty space
  and show no supporting lists, definitions or extra captions. Presenter notes leave room for
  Francisco to explain the three elements in his own words and connect them to his experience
  and students' career opportunities.
- Business skills.
- Software skills.
- People skills.
- Connect those skills to Francisco's experience and to students' career opportunities.
- Connecting idea: one workshop shows the tip of these skills; SEFOP is where to keep learning.

### 17. SEFOP: where to keep learning

- Visual: adapt the AGIFORS resources-slide layout to the template's pale background, navy
  Aptos typography and orange accents. On the left, show three spacious icon rows labeled
  "Read the book", "Run the workshop", and "Ask questions". Make the labels clickable links
  to the training hub, this workshop's repository and the discussion board respectively.
  On the right, place one large QR code pointing to `https://github.com/sefop/sefop-training-hub`,
  with `github.com/sefop/sefop-training-hub` displayed underneath. The training hub is the main
  visual destination. Use the URLs below for the individual resource links. Presenter notes
  explain what each resource offers and invite attendees to continue learning after today.
- The SEFOP training hub and its book: github.com/sefop/sefop-training-hub
- This workshop's repository, to run and read at home: github.com/sefop/sefop-sctc-2026
- The discussion board, for questions after today: github.com/sefop/sefop-training-hub/discussions
- Connecting idea: with the materials shared, the floor opens for questions.

### 18. Questions and discussion

- Visual: use the AGIFORS template's pale background as a quiet closing backdrop. On the left,
  place a large navy "Questions?" with a short orange accent line. On the right, repeat slide
  17's large training-hub QR code, pointing to `https://github.com/sefop/sefop-training-hub`,
  with `github.com/sefop/sefop-training-hub` underneath. Keep the composition spacious and leave
  it visible throughout the final discussion so attendees can access the resources. Presenter
  notes hold the two discussion prompts below and the closing connection to the lifecycle:
  the next business request starts another turn of validation and verification.
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
