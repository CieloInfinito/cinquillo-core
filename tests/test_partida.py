from cinquillo.partida import Partida
from cinquillo.bot_jugador import BotJugador
from cinquillo.carta import Carta

def test_partida_creacion_y_inicio():
    jugadores = [BotJugador(f"Bot{i}") for i in range(4)]
    partida = Partida(jugadores)
    partida.iniciar()
    total_cartas = sum(len(j.mano) for j in jugadores)
    assert total_cartas == 40
    assert any(Carta('oros', 5).valor == c.valor and Carta('oros', 5).palo == c.palo
               for j in jugadores for c in j.mano)