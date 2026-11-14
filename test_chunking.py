import pytest
from src.chunking import chunk_text, clean_text

def test_clean_text():
    assert clean_text("hello   world\n\n\nnext") == "hello world\n\nnext"

def test_blank_text():
    assert chunk_text("   ") == []

def test_splits_long_text():
    text = " ".join(f"word{i}" for i in range(100))
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(chunks)

def test_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text("some text", chunk_size=10, overlap=10)


Why are we using these tests?

When developing a text-processing application (such as an AI/RAG pipeline, search engine, document processor, or QA automation project), 
we need confidence that our code works correctly even after future changes. These tests automatically validate that behavior.

Test	                    Purpose
test_clean_text()	     Confirms text cleaning removes extra spaces and excessive blank lines.
test_blank_text()	     Ensures empty or whitespace-only input returns no chunks.
test_splits_long_text()  Checks that large text is properly divided into multiple chunks and no chunk is empty.
test_invalid_overlap()	Validates input parameters and prevents invalid chunking configurations.
