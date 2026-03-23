# Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").

When I first ran the game, the hints were completely backwards — guessing higher than the secret number would tell me to "Go HIGHER" instead of "Go LOWER," making the game impossible to win by following the hints. The secret number's type kept switching between `int` and `str` on every other attempt (even vs odd), which broke the comparison logic and sometimes made winning impossible even with the correct guess. The Hard difficulty had a narrower range (1–50) than Normal (1–100), which is the opposite of what you'd expect. The score calculation was inconsistent: wrong "Too High" guesses would randomly add or subtract 5 points depending on the attempt number, and winning gave fewer points than expected due to an off-by-one error (`attempt_number + 1` instead of `attempt_number`). Finally, the UI always displayed "Guess a number between 1 and 100" regardless of the selected difficulty, and the attempts counter started at 1 instead of 0, costing the player one attempt.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude Code (Claude Opus 4.6) as my AI pair programmer throughout this project. One correct suggestion was identifying that the hints in `check_guess()` were reversed — when `guess > secret`, the original code displayed "Go HIGHER!" instead of "Go LOWER!". Claude correctly diagnosed this by reading the conditional logic and I verified it by checking the debug panel: guessing 60 when the secret was 50 now correctly says "Go LOWER." One initially misleading aspect was that the AI's original buggy code in `check_guess` had a `TypeError` fallback that silently converted values to strings for comparison — this looked like a "safety net" but actually masked the real bug (the even/odd string cast in `app.py`). Removing both the string cast and the fallback was the correct fix, which I verified by playing multiple rounds and confirming the game works on every attempt number.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I verified fixes through both automated pytest tests and manual playtesting in the Streamlit app. For example, `test_hint_message_says_lower_when_too_high` checks that guessing 60 against a secret of 50 returns a message containing "LOWER" — this directly tests the reversed-hints bug. I also ran the game manually several times, using the Developer Debug Info panel to compare my guess against the secret and confirm the hint direction was correct. Claude Code generated the full pytest suite targeting each specific bug: hint direction, score calculation, parse edge cases, and difficulty ranges. I reviewed each test to make sure it actually tested the right behavior rather than just passing trivially.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

Streamlit reruns the entire Python script from top to bottom every time the user interacts with the app (clicks a button, types input, etc.). Without `st.session_state`, any variable defined in the script would be re-initialized on every rerun — so a line like `secret = random.randint(1, 100)` would generate a new number each time. I'd explain it to a friend like this: "Imagine your entire program restarts every time someone clicks a button. `session_state` is like a sticky note that survives the restart — you write values there so they persist." The key fix was using `if "secret" not in st.session_state` to only generate the secret once, and making sure the New Game button explicitly sets a new `st.session_state.secret` when the player wants to restart.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is writing targeted pytest cases for each specific bug before considering it "fixed" — it forces you to articulate exactly what correct behavior looks like and catches regressions. Next time, I would be more skeptical of AI-generated "safety" code like try/except fallbacks that silently change types; these often mask bugs rather than fixing them. This project reinforced that AI-generated code can look plausible and even "defensive" while containing subtle logic errors — the reversed hints and string-cast trick would pass a casual code review but completely break the game. Always play-test and write tests, even when the code looks clean.
