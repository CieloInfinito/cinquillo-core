from cinquillo.carta import Carta

def test_carta_repr():
    carta = Carta('oros', 5)
    assert repr(carta) == "5 de oros"