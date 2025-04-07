from cinquillo.carta import Carta
from cinquillo.mesa import Mesa
from cinquillo.reglas import Reglas

def test_reglas_validacion():
    mesa = Mesa()
    cinco = Carta('bastos', 5)
    assert Reglas.es_jugada_valida(cinco, mesa)