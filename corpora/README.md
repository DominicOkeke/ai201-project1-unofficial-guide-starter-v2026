# The corpora

Three corpora ship with this starter for your project, plus a fourth
(`practice`) that your instructor uses in class. Pick one of the three in
Milestone 1.

They are deliberately different from each other in **shape** — how long the
documents are, and how the useful information sits inside them. That
difference is the point: the right chunk size for short posts is not the
right chunk size for long sectioned guides, and Milestone 3 is where that
starts to matter.

All three were written for this course. No real people are named.

To switch corpus, either edit `CORPUS` in `config.py`, add
`AI201_CORPUS=name` to your `.env`, or pass `--corpus name` on the command
line. Re-run `python app.py index` after switching.

## `campus_life`

**Short posts about student life at a university.** Eighty-eight documents, most of them one to three short paragraphs — the kind of thing one student writes to answer another's question. Dining halls, dorms, courses, and the administrative rules nobody explains properly. Useful information tends to sit in a single sentence.

*Pick this if* you want the closest thing to the brief's framing, and short documents where a chunk can easily hold a whole thought.

88 documents · 27,908 characters · about 317 characters per document

## `advice_threads`

**Question-and-answer threads, with several people replying.** Twenty-three threads, each with three to five replies of very uneven length, disagreeing with each other as often as not. Real answers are spread across replies rather than sitting in one place.

*Pick this if* you want messier material. Chunking is harder here — a reply boundary and a useful boundary are not the same thing — and that makes for a more interesting Milestone 3.

23 documents · 12,490 characters · about 543 characters per document

## `city_guides`

**Long structured travel guides.** Fourteen documents — nine town guides, plus five that cut across all of them (eating, walking, regional transport, seasons, accessibility). Each is one to three thousand characters, divided into labelled sections — getting there, getting around, where to eat, when to go. Information is organised by heading and spread across a paragraph rather than packed into a sentence.

*Pick this if* you want to think about splitting on structure rather than on length. Fixed-size chunks cut through these headings badly, which is exactly the problem worth solving.

14 documents · 28,958 characters · about 2,068 characters per document

## `practice`

Not for your project. This is the small corpus your instructor uses for the
in-class follow-along, kept separate so nothing done in class touches your
graded work. It's twenty-eight documents about a board game that doesn't
exist — twenty-four short ones of a paragraph or two, and four longer sectioned
guides that a fixed-size chunker cuts straight through the middle of.

28 documents · 15,901 characters · about 567 characters per document

## Bringing your own documents

You're allowed to. Make a folder at `corpora/your_name/documents/`, put
`.txt` or `.md` files in it, and point `CORPUS` at it.

Two honest warnings. You take on the cleaning work the provided corpora
already did, and it earns no extra points. And you'll need to check that
your relevance cutoff still separates in-corpus from out-of-corpus
questions, since 0.6 was chosen against these three.

That check is Milestone 4, and it is the same check that makes 0.6 a cutoff
rather than a number. Treat the default as a starting point, not an answer —
it was set against the corpora above at their shipped chunk settings, and
changing the chunking moves the distances underneath it. Measuring it
yourself is the milestone.

Sample Chunk
5 Chunks Generated from the New def split_document function with Help Functions: Def _get_max_size_for_text(text: str) and def _split_text_by_paragraphs_and_sentences(text: str) -> list[str]:

======================================================================
Chunk 1  |  source: board_game_card_list.txt#0  |  produced by: chunker.py::split_documents
======================================================================
What's in the cargo deck

======================================================================
Chunk 2  |  source: board_game_history.txt#0  |  produced by: chunker.py::split_documents
======================================================================
About the game

======================================================================
Chunk 3  |  source: board_game_ports.txt#3  |  produced by: chunker.py::split_documents
======================================================================
Selling cargo at a port that accepts it earns two coins. Selling anywhere else earns one.

======================================================================
Chunk 4  |  source: board_game_setup.txt#3  |  produced by: chunker.py::split_documents
======================================================================
Shuffle the cargo deck and deal four cards face up to the market row.

======================================================================
Chunk 5  |  source: board_game_strategy_guide.txt#35  |  produced by: chunker.py::split_documents
======================================================================
If you are choosing between one more sale and one
more delivery, deliver.



## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. System answers correctly when chunks contain the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 5. System admits when information is missing | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

---

### Per-Question Breakdown

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Is there a strategy note past the first game? | PASS | PASS | PASS |
| By how much does most new players sail? | PASS | PASS | PASS |
| Once you have contracts open, what matters more than price? | FAIL | FAIL | FAIL |
| What is the constraint in the early game rather than position? | PASS | PASS | PASS |
| What are the worth of crew tokens if unspent? | PASS | PASS | PASS |

---

### Raw Output Evidence

**Criterion 2 Evidence (Source Citations):**
* File: `generator.py` -> Function: `generate_response()`
* Question: "What are the worth of crew tokens if unspent?" (Run 1)
> Unspent crew tokens are worth two points each. 
> 
> Sources: 
> - `board_game_strategy_guide.txt`
> - `board_game_crew.txt`
> - `board_game_designer_notes.txt`

**Criterion 3 Evidence (Relevance Gate):**
* File: `retrieval.py` -> Function: `check_relevance_gate()`
> Out-of-scope questions (the gate should refuse these):
> - Refused (best distance 0.825): What is the capital of Mongolia?
> - Refused (best distance 0.844): How do I change the oil in a diesel engine?
> - Refused (best distance 0.729): Who won the 1994 World Cup?
> - Refused (best distance 0.834): What is the recommended dosage of ibuprofen for a headache?
> - Refused (best distance 0.828): How do I write a for loop in Rust?
> -> Gate refused 5 of 5 (Cutoff: 0.7)

## Diagnoses (Milestone 3)

### 1. Diagnosis for Criterion 4 Miss (Chunk Sizes with the Answer)
* **Pipeline Stage:** **Chunking (`chunker.py`)**
* **Mechanism:** The custom helper functions `_get_max_size_for_text` and `_split_text_by_paragraphs_and_sentences` split documents on raw line breaks without enforcing a minimum character threshold for standalone chunks. As a result, standalone document headers—such as Chunk 1 (`"What's in the cargo deck"`, 26 chars) and Chunk 2 (`"About the game"`, 14 chars)—were indexed as independent chunks. Because these header chunks contain no body text or surrounding context, they fail the >100 character threshold and provide zero semantic content to the generator during retrieval.

---

### 2. Diagnosis for Question 3 Failure ("Once you have contracts open, what matters more than price?")
* **Pipeline Stage:** **Retrieval (`store.py::search` / `retrieval.py`)**
* **Mechanism:** Semantic vector search failed to retrieve the chunk containing the answer ("Routing plan"). Because the prompt asks about an abstract tradeoff ("what matters more than price"), dense embedding similarity assigned lower scores to the specific strategy file containing the routing plan tradeoff and instead pulled top-k generic contract setup files (`board_game_contracts.txt`, `board_game_variants.txt`, `board_game_setup_variants.txt`). Because the necessary chunk was missing from the retrieved context, the generator strictly adhered to its prompt instructions and responded that it did not have enough information.

### Pattern Across Misses

Looking across the evaluation results, the system's failures stem from two distinct structural patterns across the pipeline rather than isolated, random errors:

1. **Heading Isolation Pattern (Chunking Stage):** 
   * **The Pattern:** The custom splitting logic isolates structural section headings (e.g., `"What's in the cargo deck"`, 26 chars; `"About the game"`, 14 chars) into standalone chunks whenever line breaks occur. 
   * **Impact:** Because these chunks contain no trailing paragraph text or surrounding context, they continuously fail the >100 character minimum size threshold (Criterion 4 Miss) and dilute the retrieval index with zero-information vector entries.

2. **Abstract Semantic Tradeoff Pattern (Retrieval Stage):** 
   * **The Pattern:** Dense vector embeddings perform well on direct, factual lookup questions (e.g., crew token values, early game constraints, starting strategy notes), but fail when questions query abstract concepts or tradeoffs (e.g., Question 3: *"what matters more than price"*).
   * **Impact:** Cosine distance similarity ranks general setup and rules documents higher than specific strategy files containing phrase-level tradeoffs like "routing plan." Because the crucial chunk is missing from top-k, the grounding prompt correctly forces a refusal ("I don't have enough information"), causing a failure on that question.

---

### Target Tightening Assessment

While Criteria 1, 2, 3, and 5 were marked **MET**, cleared targets do not imply an optimal system. Specifically:
* **Criterion 3 (Relevance Gate):** The target was set at 4 of 5 out-of-scope questions stopped, but the gate stopped 5 of 5 in every run with distances ranging from `0.729` to `0.844`. This target was set conservatively low given the clear distance gap.
* **Tightened Target for Next Unit:** Tighten Criterion 3 to **5 of 5 (100%)** out-of-scope questions stopped, while lowering the distance cutoff threshold from `0.70` to `0.65` to test closer out-of-corpus boundary questions.