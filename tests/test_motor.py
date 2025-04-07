from cinquillo.motor import MotorJuego
from cinquillo.bot_jugador import BotJugador

def test_motor_juega_turnos():
    jugadores = [BotJugador(f"Bot{i}") for i in range(4)]
    motor = MotorJuego()
    motor.nueva_partida(jugadores)
    for _ in range(200):
        if motor.partida.finalizada:
            break
        motor.jugar_turno()
    assert motor.partida.finalizada
    assert any(len(j.mano) == 0 for j in jugadores)


