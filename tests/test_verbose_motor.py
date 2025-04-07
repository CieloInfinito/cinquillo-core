from cinquillo.motor import MotorJuego
from cinquillo.bot_jugador import BotJugador

def test_verbose_motor():
    jugadores = [BotJugador(f"Bot{i}") for i in range(4)]
    motor = MotorJuego()
    motor.nueva_partida(jugadores)

    print("=== MANOS INICIALES ===")
    for jugador in jugadores:
        print(f"{jugador.nombre}: {[str(carta) for carta in sorted(jugador.mano, key=lambda c: (c.palo, c.valor))]}")

    print("\n=== COMIENZO DEL JUEGO ===")
    for turno in range(100):
        if motor.partida.finalizada:
            print(f"\n🏁 Partida finalizada en {turno} turnos.")
            break
        jugador = motor.partida.jugadores[motor.partida.turno_actual]
        mano_antes = list(jugador.mano)
        carta = jugador.jugar(motor.partida.mesa)
        if carta:
            motor.partida.mesa.colocar_carta(carta)
            motor.partida.historial.append((jugador.nombre, carta))
            print(f"🃏 {jugador.nombre} juega {carta}")
        else:
            print(f"⏭ {jugador.nombre} pasa (sin jugada válida)")
        motor.partida.siguiente_turno()

    else:
        print("\n⚠️ La partida no se resolvió en 100 turnos.")

    print("\n=== ESTADO FINAL DE LA MESA ===")
    for palo, valores in motor.partida.mesa.estado.items():
        print(f"{palo}: {sorted(valores)}")

    print("\n=== MANOS FINALES ===")
    for jugador in jugadores:
        print(f"{jugador.nombre}: {[str(carta) for carta in jugador.mano]}")