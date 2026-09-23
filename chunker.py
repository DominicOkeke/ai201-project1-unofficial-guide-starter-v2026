"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.


from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    One piece of one document.

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    
    The starter's original chunker. Fixed-size character windows with overlap.
    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    
    Split documents into chunks. ⚠️ REPLACE THE BODY OF THIS IN MILESTONE 3.

    Right now it just calls the fallback. That is the plain, generic behaviour
    the brief is talking about.

    When you write your own strategy, set `produced_by` to
    "chunker.py::split_documents" so your README's Sample Chunks section names
    the right function. `app.py chunks` prints that string for you.

    Things worth thinking about before you write any code:
      - Are your documents short posts or long guides?
      - Is the useful information in one sentence, or spread over a paragraph?
      - Would splitting on paragraph breaks keep more thoughts intact than
        splitting on a character count?
    
    return fallback_split(documents)


def describe(chunks: list[Chunk]) -> str:
    A one-line summary, printed after indexing.
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
"""   
"""
Stage 2 of the pipeline: splitting documents into chunks.

`split_documents` splits documents cleanly by paragraphs and sentences,
adjusting maximum chunk size depending on whether content consists of short headings/posts 
(max 30 chars) or longer text paragraphs (max 100 chars).
"""

from dataclasses import dataclass
import re

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _get_max_size_for_text(text: str) -> int:
    """
    Determines maximum chunk size limit based on content type:
    - Headings: 150 characters
    - Paragraphs / Sentences: 400 characters
    """
    cleaned = text.strip()
    if cleaned.startswith("#") or len(cleaned) <= 50:
        return 150
    return 400


def _split_text_by_paragraphs_and_sentences(text: str) -> list[str]:
    """Splits raw text into complete paragraphs or sentences adhering to size limits."""
    # Split text into paragraphs first by double newlines
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    pieces: list[str] = []

    for para in paragraphs:
        max_size = _get_max_size_for_text(para)

        if len(para) <= max_size:
            pieces.append(para)
        else:
            # Split paragraph into sentences on sentence-ending punctuation
            sentences = [
                s.strip()
                for s in re.split(r"(?<=[.!?])\s+", para)
                if s.strip()
            ]
            current_piece = []
            current_length = 0

            for sentence in sentences:
                sentence_limit = _get_max_size_for_text(sentence)

                if len(sentence) > sentence_limit:
                    if current_piece:
                        pieces.append(" ".join(current_piece))
                        current_piece = []
                        current_length = 0

                    words = sentence.split()
                    temp_chunk = []
                    temp_len = 0
                    for word in words:
                        if temp_len + len(word) + (1 if temp_chunk else 0) <= sentence_limit:
                            temp_chunk.append(word)
                            temp_len += len(word) + (1 if temp_chunk else 0)
                        else:
                            if temp_chunk:
                                pieces.append(" ".join(temp_chunk))
                            temp_chunk = [word]
                            temp_len = len(word)
                    if temp_chunk:
                        pieces.append(" ".join(temp_chunk))
                    continue

                if current_length + len(sentence) + (1 if current_piece else 0) <= sentence_limit:
                    current_piece.append(sentence)
                    current_length += len(sentence) + (1 if current_piece else 0)
                else:
                    if current_piece:
                        pieces.append(" ".join(current_piece))
                    current_piece = [sentence]
                    current_length = len(sentence)

            if current_piece:
                pieces.append(" ".join(current_piece))

    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks using paragraph/sentence boundaries with custom limits:
    - 30 characters for headings & short posts
    - 100 characters for longer text paragraphs
    """
    chunks: list[Chunk] = []

    for doc in documents:
        pieces = _split_text_by_paragraphs_and_sentences(doc.text)

        for index, piece in enumerate(pieces):
            chunks.append(
                Chunk(
                    text=piece,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))