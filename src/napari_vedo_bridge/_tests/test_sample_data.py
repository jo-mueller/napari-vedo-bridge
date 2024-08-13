def test_sample_data():
    from .._sample_data import (
        beethoven,
        apple,
        bunny,
        cow,
        mouse_limb1,
        panther,
        mouse_limb2,
        mouse_limb3,
    )

    # Test beethoven
    layers = beethoven()
    assert len(layers) == 1

    # Test apple
    layers = apple()
    assert len(layers) == 1

    # Test bunny
    layers = bunny()
    assert len(layers) == 1

    # Test cow
    layers = cow()
    assert len(layers) == 1

    # Test mouse_limb1
    layers = mouse_limb1()
    assert len(layers) == 1

    # Test panther
    layers = panther()
    assert len(layers) == 1

    # Test mouse_limb2
    layers = mouse_limb2()
    assert len(layers) == 1

    # Test mouse_limb3
    layers = mouse_limb3()
    assert len(layers) == 1