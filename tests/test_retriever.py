import pytest
from retrieval.retriever import retrieve_idiom

def test_basic_retrieval():
    situation = "I want to describe something that never changes."
    top_k = 3
    results = retrieve_idiom(situation, top_k=top_k)

    # Check type and length
    assert isinstance(results, list)
    assert len(results) == top_k

    # Check that each entry is a string
    for item in results:
        assert isinstance(item, str)
        assert len(item) > 0

def test_empty_query():
    results = retrieve_idiom("", top_k=2)
    assert isinstance(results, list)
    assert len(results) == 2
    for item in results:
        assert isinstance(item, str)
        assert len(item) > 0
