from cinquillo.carta import Carta
from cinquillo.mesa import Mesa

def test_puede_colocar_cinco():
    mesa = Mesa()
    carta = Carta('copas', 5)
    assert mesa.puede_colocar(carta)

def test_colocar_y_validar_carta():
    mesa = Mesa()
    cinco = Carta('espadas', 5)
    seis = Carta('espadas', 6)
    cuatro = Carta('espadas', 4)
    mesa.colocar_carta(cinco)
    assert mesa.puede_colocar(seis)
    assert mesa.puede_colocar(cuatro)