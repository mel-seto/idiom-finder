import pytest
from verification.verifier import verify_idiom_exists
from singletons import CC_DICT


@pytest.mark.integration
@pytest.mark.parametrize(
    "idiom, expected",
    [
        # ChiD idioms
        ("对症下药", True),
        ("画蛇添足", True),
        ("自相矛盾", True),

        # CC-CEDICT idioms
        ("一成不变", True),
        ("铁面无私", True),
        ("德才兼备", True),

        # Wiktionary-only
        ("临危不惧", True),
        ("心旷神怡", True),

        # Nonexistent idiom
        ("完全不存在的成语", False),
    ]
)
def test_verify_idiom_integration(idiom, expected):
    result = verify_idiom_exists(idiom)
    assert result is expected
