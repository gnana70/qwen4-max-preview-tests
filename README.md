# Qwen4-Max-Preview vs Qwen3.8-Max: same prompts, real outputs

Companion repo for the Singularity Feed video **[Qwen 4-Max Is Here: I Tested It Against Qwen 3.8-Max](https://youtu.be/G1SexwcKHtU)**.

Every file in `games/` and `answers/` is the model's answer **exactly as it came out of the Qwen app**, copied with the app's Copy button and checked with SHA-256 (see `TEST-LOG.md`). Nothing was edited. Open any `.html` file in a browser to try it.

## How the test was run
- App: [chat.qwen.ai](https://chat.qwen.ai), Thinking mode, one try per model, a new chat for every prompt, no follow-ups.
- 11 Nov 2026: the first three tests (guest session). 12 Nov 2026: the GTA-clone test, requested by a viewer (logged-in free account).
- The exact prompts are in `prompts.json`.
- Times are from screenshot timestamps of one run in a free app, so they depend on server load.

## Results

| Test | Qwen4-Max-Preview | Qwen3.8-Max |
|---|---|---|
| **Murmuration** – one HTML file, ~800 birds, F = fish, B = giant bird ([prompt](prompts.json)) | Works first try; tight, clean shapes (the fish has an eye). ~12 min. [`games/qwen4-max-preview_murmuration.html`](games/qwen4-max-preview_murmuration.html) | Works first try; shapes recognizable but loose. ~19 min. [`games/qwen3.8-max_murmuration.html`](games/qwen3.8-max_murmuration.html) |
| **Coding** – `evaluate(expr)` from scratch, 20 hidden tests | 20/20, ~2.5 min. [`answers/qwen4-max-preview_evaluate.py`](answers/qwen4-max-preview_evaluate.py) | 20/20, ~17 min. [`answers/qwen3.8-max_evaluate.py`](answers/qwen3.8-max_evaluate.py) |
| **Clock question** – right angles in 24 h (answer: 44) | 44, and explains why not 48 | 44 |
| **GTA clone** (viewer request) – top-down open world, car entry, traffic, police, minimap | "NEON BAY": title screen, 3 modes, enter/exit cars, traffic, pedestrians, minimap, speedometer, courier jobs. 2,409 lines, ~1 h 34 min. [`games/qwen4-max-preview_gta-neon-bay.html`](games/qwen4-max-preview_gta-neon-bay.html) | Running now; added when it finishes |

Extra code check (run afterwards on both answers, `tools/check_extra.py`): 19/20 each; both fail only on 200-deep nested parentheses (Python's recursion limit, not in the spec).

## Try the games
Download the repo (Code → Download ZIP) and double-click a file in `games/`.
- Murmuration: **F** fish, **B** giant bird, **Space** free flight.
- NEON BAY: **Enter** to start, **WASD / arrows** move and drive, **E** get in / out, **Space** handbrake, **M** map, **H** horn, **P** pause.

## Re-run the checks
```bash
pip install playwright && python -m playwright install chromium
python tools/check_code.py answers/qwen4-max-preview_evaluate.py      # 20 hidden cases
python tools/check_extra.py answers/qwen4-max-preview_evaluate.py     # 20 extra cases
python tools/record_html.py games/qwen4-max-preview_murmuration.html out.mp4          # needs ffmpeg
python tools/record_html.py games/qwen4-max-preview_gta-neon-bay.html gta.mp4 --seconds 34 --keys "$(cat tools/gta_keys.txt)"
```
`record_html.py` plays a page with a fixed virtual clock (requestAnimationFrame, performance.now and Math.random are controlled), so every run gives the same frames and both models get exactly the same key presses.

## Notes
- One Qwen3.8-Max murmuration request was cut off when I opened a second chat in the same guest session (guest mode runs one request at a time); it was re-sent and not counted.
- In the GTA test, the Qwen app's page lost its live connection a few times ("The request is ended!"), but the same request kept running on Qwen's side and finished; it was not re-sent.
- Small test, not a benchmark.
