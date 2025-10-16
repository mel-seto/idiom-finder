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

@pytest.mark.parametrize(
    "situation, idiom",
    [
        ("to return from a rewarding journey", "满载而归"),
        ("everywhere all at once", "无所不在"),
    ],
)
def test_definition_returns_correct_idiom(situation, idiom):
    """if input situation is the same as the embedded English definition, 
    RAG implementation should return the correct Chinese idiom"""
    top_k_idioms = retrieve_idiom(situation, top_k=3)
    assert any(idiom in s for s in top_k_idioms)
