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
    from napari.layers import Layer

    # Test beethoven
    layers = beethoven()
    layer = Layer.create(layers[0][0], layers[0][1], layers[0][2])
    assert len(layers) == 1

    # Test apple
    layers = apple()
    layer = Layer.create(layers[0][0], layers[0][1], layers[0][2])
    assert len(layers) == 1

    # Test bunny
    layers = bunny()
    layer = Layer.create(layers[0][0], layers[0][1], layers[0][2])
    assert len(layers) == 1

    # Test cow
    layers = cow()
    layer = Layer.create(layers[0][0], layers[0][1], layers[0][2])
    assert len(layers) == 1

    # Test mouse_limb1
    layers = mouse_limb1()
    layer = Layer.create(layers[0][0], layers[0][1], layers[0][2])
    assert len(layers) == 1

    # Test panther
    layers = panther()
    layer = Layer.create(layers[0][0], layers[0][1], layers[0][2])
    assert len(layers) == 1

    # Test mouse_limb2
    layers = mouse_limb2()
    layer = Layer.create(layers[0][0], layers[0][1], layers[0][2])
    assert len(layers) == 1

    # Test mouse_limb3
    layers = mouse_limb3()
    layer = Layer.create(layers[0][0], layers[0][1], layers[0][2])
    assert len(layers) == 1