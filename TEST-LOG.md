# Side-by-side test log (11 Nov 2026, chat.qwen.ai, guest session, Thinking mode, one try each, new chat per prompt)

| model | prompt | sent (UTC) | thinking ended | answer done | notes |
|---|---|---|---|---|---|
| Qwen4-Max-Preview | build | ~16:54:10 | — | ≤17:06:30 (~12 min) | 973-line HTML, 38,061 bytes, sha256 04568da4…; app shows "Thinking completed" (no duration shown) |
| Qwen4-Max-Preview | code | 17:09:43 | — | ≤17:12:07 (~2.5 min) | 119-line answer, no code fence (app shows it unindented; the message Copy button keeps indentation); sha256 b633bee0…; **20/20 hidden tests**, no banned calls |
| Qwen4-Max-Preview | reason | ~17:13:10 | — | <17:13:40 | **44 (correct)**, explains why not 48 |

Build (Qwen4-Max-Preview), recorded with virtual time, keys F@6s B@14s Space@22s: free flock OK, fish outline OK (with eye), giant bird = spread-wing outline (blocky, totem-eagle look), returns to free flight OK; no console errors; JS 2.4 ms/frame median (6.8 p95).

Note: the first Qwen3.8-Max build request (sent 17:13:57) was cut off ("The request is ended!") when I opened a second chat in the same guest session to run the code prompt in parallel. The guest session allows one request at a time. This was my error, not the model's; the attempt isn't counted and the build prompt is re-sent after the other prompts, one at a time.
| Qwen3.8-Max | code | ~17:18:10 | — | ≤17:35:07 (~17 min) | 177-line answer, no fence (partly shown as a code block); sha256 a529458a…; **20/20 hidden tests**, no banned calls; ~17 min, mostly thinking |
| Qwen3.8-Max | reason | 17:36:30 | — | after the user cleared a slider check (~17:40–17:43) | **44 (correct)**, shorter explanation; the bot-check pause makes its time not comparable |
| Qwen3.8-Max | build (re-sent) | 17:44:08 | — | ≤18:02:51 (~19 min) | 608-line HTML, 22,888 bytes, sha256 d7a855e7…; no console errors; JS 4.7 ms/frame median (9.7 p95) |

Build verdicts (same recorder, same key times):
- Qwen4-Max-Preview: free flock ✓, dusk sky ✓, fish ✓ (dense, clean outline with an eye), giant bird ✓ (spread wings, blocky tail), Space ✓. ~12 min.
- Qwen3.8-Max: free flock ✓, dusk sky ✓ (with a tree), fish ✓ (recognizable but loose, stretched, sparse), giant bird ✓ (spread wings, loose), Space ✓. ~19 min. Its UI also lists "click = hawk" (not tested).
Overall: tie on correctness in all three tests; Qwen4-Max-Preview was faster in this run (build ~12 vs ~19 min, code ~2.5 vs ~17 min) and its visual result was cleaner. Times are from one run in the free app and depend on server load.
Extra code checks (after the fact, both answers): 19/20 each; both fail only 200-deep nested parentheses (recursion limit, not in the spec).

## Exact times (from screenshot timestamps, UTC; done times are upper bounds)
- Qwen4-Max-Preview build: sent ~16:54:10, done ≤17:06:30 → ~12 min
- Qwen4-Max-Preview code: sent 17:09:43, done ≤17:12:07 → ~2.5 min
- Qwen4-Max-Preview reason: sent ~17:12:58, done ≤17:13:26 → <30 s
- Qwen3.8-Max code: sent ~17:18:10, done ≤17:35:07 → ~17 min
- Qwen3.8-Max reason: sent ~17:36:30; a bot-check slider appeared (cleared by the user), answer seen 17:43:19 → time not comparable
- Qwen3.8-Max build: sent 17:44:08, done ≤18:02:51 → ~19 min
(Earlier minute counts in the table above were estimated from polling and are superseded by this list.)

## GTA-clone test (viewer request, 12 Nov 2026)
Logged-in account this time (guest sends were blocked: "log in for more generation credits"). Agent Mode chip removed, Thinking mode, one try each, new chat, one request at a time.
Gameplay script for both (tests/gta_keys.txt): E at 1 s (get in car), drive with W + turns 1.6–26 s, brake, E at 27 s (get out), walk.
| model | sent (UTC) | done | notes |
|---|---|---|---|
| Qwen4-Max-Preview | 15:55:32 | | At ~16:01 the page showed "The request is ended!", but the request kept running on Qwen's server (Regenerate answered "The chat is in progress!"; no second request was started). Reloading at 16:11 re-attached to the same, still-thinking request. Still one try. Thinking ended ≈16:54 (code visible 16:54:53); answer complete ≤17:29:14 → ~1 h 34 min total (~59 min thinking, ~35 min writing). 2,409-line HTML "NEON BAY · mini open world", 116,119 bytes, sha256 94e9dcfd…; title screen with Casual/Classic/Chaos modes. |
| Qwen3.8-Max | 17:32:10 | | chat /c/66a571a6-11da-462a-8369-9f07bd290f21 |
