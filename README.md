# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

     This project is a grounded Retrieval-Augmented Generation (RAG) system built to query and deliver verifiable answers from reference documents.

Key Features & Workflow
Document Ingestion & Chunking: Loads raw text documents and cleanly splits them into meaningful chunks based on natural paragraph (\n\n) and sentence boundaries.

Vector Embedding & Storage: Converts text chunks into vector embeddings and indexes them using ChromaDB for similarity search.

Relevance Gating: Evaluates the distance score of the top-retrieved chunk against a configured cutoff (RELEVANCE_CUTOFF = 0.70). If a query is out-of-scope or lacks sufficient context in the corpus, the system refuses to answer rather than risking hallucinations.

Grounded Answer Generation: When a query passes the relevance gate, the context is passed to the LLM with strict grounding instructions to answer using only the retrieved documents and explicitly cite the source file.

## Chunking Strategy

**Chunk size:**
**Overlap:**

Strategy Chosen: Sentence- and paragraph-aware chunking with dynamic character limits.

Chunk Sizing Logic:

Headings / Short Lines: Max limit of 150 characters.

Paragraphs / Main Text: Max limit of 500 characters.

Rationale: Fixed-size windowing chopped sentences mid-thought, causing incomplete context and inflated semantic distance scores. Splitting by double newlines (\n\n) first and falling back to punctuation boundaries keeps complete rules and strategy points intact.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `` — produced by:[text](corpora/advice_threads/documents/thread_laptop_specs.txt) ``

```THREAD: How much laptop do I actually need for CS courses?

--- reply 1 (31 votes) ---
Less than the recommended spec page says. 16GB of RAM is the one number worth paying for; everything else you'll never notice.

--- reply 2 (18 votes) ---
Adding: the lab machines exist and are better than anything you'll buy. For the heavy assignments people just use those.

--- reply 3 (12 votes) ---
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.
```

**Chunk 2** — source: `` — produced by:[text](corpora/campus_life/documents/course_cs_210_exams.txt) ``

```CS 210 Data Structures — assessment

Two midterms and a final, all drawn from lecture material rather than the textbook. Midterms are curved, the final is not.

Do the labs even though they're only 10% — the exams reuse the lab problems.

```

**Chunk 3** — source: `` — produced by: [text](corpora/campus_life/documents/course_phys_130_workload.txt)``

```
Workload for PHYS 130 Mechanics


People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `` — produced by:[text](corpora/practice/documents/board_game_strategy_guide.txt) ``

```
Strategy notes for players past their first game

Nothing here is a rule. It is what tends to be true, and a table that disagrees
with all of it can still be playing correctly.

The opening

Most new players sail too much and load too little. Cargo is the constraint in
the early game rather than position, and a boat sitting at a good port with an
empty hold has spent its turns badly. Taking the leftmost market card repeatedly
is usually stronger than paying two or three coins for a better card, at least
until you hold a contract that names a specific type. Coins spent early on the
right-hand end of the market row are coins you rarely get back.

The middle of the game

Once you have contracts open, route planning matters more than price. The six
ports each accept two cargo types, and they run along the track so that
neighbouring ports share a type: timber and salt, then salt and wool, then wool
and fish, then fish and iron, then iron and timber. That overlap means a hold
with two adjacent types can often be emptied in one stretch of the track without
doubling back. The sixth port takes whichever two types were chosen at setup,
which is what makes the far end of the track worth the sailing.

The last few turns

The deck running out ends the game, so count what is left in it once it looks
thin. A contract you cannot finish before the deck empties is worth one coin to
discard and nothing to keep. Crew tokens are two points each if unspent, which
means spending your last token to squeeze out a two-coin sale is exactly break
even, and spending it to complete a contract is clearly worth it. Deciding that
in advance is easier than deciding it under time pressure.

Where the points actually come from

A worked example is worth more than a principle here. Nine coins, two contracts
and one unspent crew token scores seventeen. Three coins, four contracts and no
crew scores fifteen. The player with three times fewer coins came within two
points, and the difference between those two players was contracts, not trade.
Coins rarely decide a game. If you are choosing between one more sale and one
more delivery, deliver.

Playing against people who know this

Since the cargo distribution is even — twelve each of five types — counting what
has already appeared is legitimate and moderately effective late on. Assume an
experienced opponent is doing it, and assume they can see which contract you are
setting up for from the types in your hold.
```

**Chunk 5** — source: `` — produced by: ``

```
corpora/practice/documents/board_game_strategy_guide.txt
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->
--- Source: corpora/practice/documents/board_game_strategy_guide.txt

**Question:**
  What are the worth of crew tokens if unspent?

**Answer:**

```
 According to `board_game_strategy_guide.txt`, crew tokens are worth two points each if left unspent at the end of the game.
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. 
     
     Here are your 5 in-scope best distances and 5 out-of-scope best distances based on your actual test queries:

1. In-Scope Questions & Best Distances
1."What is the constraint in the early game rather than position?"

   Best Distance: 0.625

2."How many coins do you get to discard an unfinished contract?"
    
  Best Distance: 0.638

3."What are the worth of crew tokens if unspent?"

Best Distance: 0.647

4."Once you have contracts open, what matters more than price?"

Best Distance: 0.655

5."What score did the worked example yield with nine coins, two contracts, and one token?"

Best Distance: 0.612

2. Out-of-Scope Questions & Best Distances
(From OUT_OF_SCOPE / non-corpus queries)

1."What is the capital of France?"

   Best Distance: 0.842

2."How do I reset my campus WiFi password?"

   Best Distance: 0.811

3."When does the dining hall close on Sundays?"

   Best Distance: 0.795

4."Who won the 2022 World Cup?"

   Best Distance: 0.863

5."What is the syllabus for STAT 150?"

   Best Distance: 0.789

Distance Gap & Cutoff Summary
In-Scope Range: 0.612 – 0.655 (Highest: 0.655)

Out-of-Scope Range: 0.789 – 0.863 (Lowest: 0.789)

Chosen Cutoff: 0.70 (Placed cleanly in the gap between 0.655 and 0.789).-->

Explanation

The gap between in-scope queries (highest 0.655) and out-of-scope queries (lowest 0.789) lies between 0.66 and 0.78. Setting RELEVANCE_CUTOFF = 0.70 allows all valid strategy questions to pass while reliably blocking off-topic requests.

| Question | In corpus? | Best distance |
|---|---|---|
|  |  |  |

In-Scope Distance Range: 0.612 to 0.655 (Highest in-scope distance: 0.655)

Out-of-Scope Distance Range: 0.789 to 0.863 (Lowest out-of-scope distance: 0.789)

## What This Does

This project is a grounded Retrieval-Augmented Generation (RAG) system built to query and deliver verifiable answers from specific reference documents (such as board game strategy guides or campus life documentation). 

### Key Features & Workflow:
1. **Document Ingestion & Chunking:** Loads raw text documents and cleanly splits them into meaningful chunks based on natural paragraph (`\n\n`) and sentence boundaries rather than rigid character counts.
2. **Vector Embedding & Storage:** Converts text chunks into vector embeddings and indexes them using ChromaDB for similarity search.
3. **Relevance Gating:** Evaluates the distance score of the top-retrieved chunk against a configured cutoff (`RELEVANCE_CUTOFF = 0.70`). If a query is out-of-scope or lacks sufficient context in the corpus, the system refuses to answer rather than risking hallucinations.
4. **Grounded Answer Generation:** When a query passes the relevance gate, the context is passed to the LLM with strict grounding instructions to answer using *only* the retrieved documents and explicitly cite the source file.

---



## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

AI was used as a collaborative partner during development to refine code design, optimize chunking logic, and debug runtime issues.

### Specific Examples:

**1.**Developing the Sentence & Paragraph Chunking Function:**
   * **What I asked:** I provided the original fixed-window starter chunker and asked AI to rewrite `split_documents` to split text by paragraphs (`\n\n`) first and fall back to sentence boundaries (`. `, `! `, `? `).
   * **What came back:** The generated code successfully split sentences using regex, but it defaulted to a generic 800-character limit and lacked specific limits for short headings.
   * **What I changed:** I modified the sizing helper function (`_get_max_size_for_text`) to dynamically adjust character limits (150 chars for headings/short posts vs. 500 chars for paragraphs) and added logic to prevent slicing sentences across chunk boundaries.

**2.**Diagnosing Relevance Gate Refusals & Distance Calibration:**
   * **What I asked:** I asked AI why valid in-scope questions were being rejected with `"I don't have enough information about that"` despite targeting the correct corpus.
   * **What came back:** AI explained that my retrieved chunk distances (`0.625`–`0.655`) were slightly higher than the starter's strict `0.60` cutoff, causing the relevance gate to block valid context.
   * **What I changed:** I ran 5 in-scope queries alongside 5 out-of-scope queries to measure the distance gap. Based on the observed gap (`0.655` max in-scope vs. `0.789` min out-of-scope), I updated `config.py` to set `RELEVANCE_CUTOFF = 0.70`, allowing all valid queries through while maintaining strict refusal for off-topic prompts.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 0/5 | 0/5 | 0/5 | MISSED |
| 4. Chunk sizes with the answer |5 of 5 |0/5|0/5|0/5|MISSED |
| 5.Minimum time taken to read strategy |5 of 5 |5/5 |5/5 |5/5 |MET|

**Did it help?**
 No — the change backfired and made overall system performance worse.**

While implementing Hybrid Search successfully improved semantic retrieval for abstract concept queries (resolving Question 3 and raising Criterion 1 from 4/5 to 5/5), assigning a static fallback distance of 0.450 to pure BM25 hits severely compromised the relevance gate. Because 0.450 falls below the 0.60 relevance cutoff threshold, the gate allowed 100% of out-of-scope test questions through, causing Criterion 3 performance to drop catastrophically from 5/5 (MET) to 0/5 (MISSED).
<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

The change backfired and made performance worse.

How We Know:
The Positive Impact: Integrating Hybrid Search (BM25 + Dense Vectors) successfully resolved Question 3 ("Once you have contracts open, what matters more than price?"), bringing Criterion 1 (Retrieved chunk contains answer) from 4/5 up to 5/5.

The Backfire (Regression): To handle pure BM25 keyword matches, non-vector results were assigned a fixed fallback distance of 0.450. Because 0.450 is lower than your system's 0.60 relevance gate threshold, the gate incorrectly classified all out-of-scope questions (e.g., "What is the capital of Mongolia?") as relevant in-corpus queries. As a result, Criterion 3 (Gate stops out-of-corpus questions) collapsed from 5/5 down to 0/5.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->
### 1. Criterion 3: Relevance Gate Calibration (Regression)
* **Status:** MISSED (0/5)
* **Root Cause:** Introducing Hybrid Search assigned a fixed fallback distance of `0.450` to non-vector / pure BM25 keyword matches. Because `0.450` is lower than the `0.60` relevance gate cutoff threshold, out-of-corpus queries (e.g., *"What is the capital of Mongolia?"*) were incorrectly classified as relevant, letting 100% of out-of-scope questions bypass the gate.

### 2. Criterion 4: Isolated Header Chunks (<100 Characters)
* **Status:** MISSED (0/5)
* **Root Cause:** The splitting logic in `chunker.py` isolates structural document headers (e.g., `"About the game"`, 14 chars) into standalone chunks whenever line breaks occur.
*
* **Why Stopped:** Scope was restricted to testing a single pipeline improvement during Milestone 4.

---

* **Why Stopped:** Milestone 4 focused on measuring a single targeted change (Hybrid Search implementation). Fixing the resulting distance calibration side effect requires a second iteration pass.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

In the next unit, I would rewrite **Criterion 3 (Relevance Gate)** to measure relative distance margins rather than relying on a hardcoded absolute cutoff threshold like `0.60`. Testing against fixed distance cutoffs breaks easily when switching retrieval architectures (such as moving from pure dense vectors to hybrid sparse/dense RRF scoring). A threshold tied to the distance gap between top-1 and top-5 results would be much more robust across model and search changes.

* **Proposed Fix:** Re-calibrate the BM25 fallback distance in `store.py` from `0.450` to `0.850` (or dynamically weight RRF scores into a normalized distance between `0.0` and `1.0`) so ungrounded keyword hits fail the `0.60` cutoff gate.

 **Proposed Fix:** Update `chunker.py` to enforce a minimum chunk length threshold (e.g., merging any chunk under 100 characters into the subsequent paragraph chunk).










Milestone 2/3 vs. Milestone 4 ("After") Comparison
Your Hybrid Search implementation changed how distances are assigned to chunks. Pure BM25 hits are assigned a fallback distance of 0.450.

Because your relevance gate threshold is configured at 0.60, assigning a default distance of 0.450 to out-of-scope queries caused a catastrophic regression on Criterion 3.

Side-by-Side Comparison:
Criterion,Target,Before Fix (Milestone 2/3),After Fix (Hybrid Search),Verdict Change
1. Retrieved chunk contains answer,4 of 5,4/5 (Failed Q3),5/5 (Distances lowered across all 5 Qs),IMPROVED
2. Every answer names a source,5 of 5,5/5,5/5,UNCHANGED
3. Gate stops out-of-corpus questions,4 of 5,5/5 (Refused all 5 with dist 0.72–0.84),0/5 (Let all 5 through with dist 0.450),FAILED (REGRESSION)
4. Chunk sizes with the answer,5 of 5,0/5 (Header chunks <100 chars),0/5 (Shortest chunk still 10 chars),UNCHANGED
5. Minimum time taken to read strategy,5 of 5,5/5,5/5,UNCHANGED