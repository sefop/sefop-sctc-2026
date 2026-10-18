# SCTC 2026 presentation sources

The finished presentation is `SCTC-2026-Airlines-Optimization-Workshop.pptx` in the repository root.
It has 18 slides, using the agreed visuals in `assets/slide-story.md`, and presenter notes on
every slide. The deck is self-contained: its images and QR code are embedded.

Diagrams, module boxes, tables, labels and mathematical statements are editable PowerPoint
objects. The three airline icons include SVG originals and PNG fallbacks. Photographs are embedded
images. The original AGIFORS slide masters and 16:9 format are retained; visible objects use Aptos,
Aptos Display, the pale background, navy typography and orange accents of that reference.

## Presenter use

Open the root `.pptx` in PowerPoint. Use Presenter View or the Notes pane to read the explanations,
activity instructions, expected answers, sources, pacing and live-demonstration commands.
Slides 13 and 14 cue the prepared program and test demonstrations. Slide 15 introduces the next
business request without demonstrating the customer-diversity feature.

The presenter notes for slide 14 distinguish the effects of defects before and after
preprocessing. They also distinguish acceptance criteria from a test's execution scope.

The three labels on slide 17 are hyperlinks. The QR code on slides 17 and 18 opens
`https://github.com/sefop/sefop-training-hub`.

## Images and references

See `sources.json` for the original workshop decks and source slides. The source decks themselves
are unchanged. The existing `assets/planner_image.png` is also unchanged.

`cargo-planner.png` was generated with the built-in imagegen tool. Its exact prompt is in
`image-prompt.txt`. It intentionally has no readable labels, numerical inputs, mathematical rules,
or shipment-selection indicators. The planner image on slide 7 is a PowerPoint crop of this same
image.

The testing and modularity diagrams are native PowerPoint adaptations of figures from the
SEFOP book, identified in the corresponding slide's notes.

## Rebuild

Install `python-pptx` and `Pillow` into a Python environment and run:

```powershell
python assets/presentation/build_presentation.py
```

The script also recognizes the development dependencies in `.cache/presentation-python`.
It reads the story and local image assets, and uses the original AGIFORS deck listed in
`sources.json` when that deck is available. Rebuilding replaces the generated root presentation.

Temporary slide renders and the layout audit are in `.cache/presentation-render`.
