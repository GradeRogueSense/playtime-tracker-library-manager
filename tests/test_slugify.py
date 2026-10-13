from playtime_tracker.utils.slugify import slugify


def test_basic_slug():
    assert slugify("Hades II") == "hades-ii"


def test_unicode_folded():
    assert slugify("Pokémon™ Scarlet") == "pokemon-scarlet"


def test_empty_falls_back():
    assert slugify("   ") == "unnamed"


def test_collapses_separators():
    assert slugify("A  --  B__C") == "a-b-c"