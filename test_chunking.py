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
