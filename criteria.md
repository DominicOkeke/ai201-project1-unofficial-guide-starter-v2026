# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
Target: 4 of 5

Actual Performance: 4/5, 4/5, 4/5

Verdict: MET

Sentence/Decision: In all three runs, exactly 4 out of 5 test questions retrieved chunks containing the target answer, consistently reaching the 4/5 target without dropping below it.
---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->

Target: 5 of 5

Actual Performance: 5/5, 5/5, 5/5

Verdict: MET

Sentence/Decision: Every generated response across all three evaluation runs explicitly cited its source document name, satisfying the 100% attribution requirement across the board.
---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

Target: 4 of 5

Actual Performance: 5/5, 5/5, 5/5

Verdict: MET

Sentence/Decision: The relevance gate distance cutoff of 0.7 stopped all 5 out-of-scope questions in every run, easily surpassing the 4 of 5 target.

---

## 4. Something about your chunks: Chunk sizes with the answer 

<!-- YOU WRITE THIS ONE: Chunk size must be more than 100 characters with headings more 30 characters can contain answers.--!>

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->



**Why this target:**
<!--Chunks are not headings although they have them. If answer is also found in the headings, therefore, the criterion covers both heading and paragraphs for chunks--!>

Target: Chunk size must be greater than 100 characters (or headings greater than 30 characters) to contain answers- 5/5

Actual Performance: 0/5, 0/5, 0/5

Verdict: MISSED

Why (Decision Rationale): Inspecting the generated chunks from the run log shows multiple chunks below the threshold (such as Chunk 1 at 26 characters and Chunk 2 at 14 characters) that function only as section titles without enough context to answer questions independently.

---

## 5. Your choice: Minimum time taken to read through the game strategy

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome.
     
     The minimum time for reading the board game strategy guide is 3 minutes -->



**Why this target:**
Reading the board game strategy guide can take more time but one must have finished reading it in 3 minutes following standard reading practices.

Target: Reading time for the board game strategy guide is a minimum of 3 minutes - 5/5

Actual Performance: 5/5, 5/5, 5/5

Verdict: MET

Why (Decision Rationale): The document board_game_strategy_guide.txt contains roughly 600 words, which requires approximately 2.5 to 3.5 minutes to thoroughly read and evaluate at standard adult reading speeds (200–250 wpm).

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
