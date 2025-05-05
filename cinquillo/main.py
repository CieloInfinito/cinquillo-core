# main.py

from cinquillo.motor import MotorJuego
from cinquillo.bot_jugador import BotJugador
from cinquillo.jugador_humano import JugadorHumano
from cinquillo.carta import Carta

import csv
import re

def mostrar_estado_mesa(mesa):
    print("\nEstado actual de la mesa:")
    for palo in ['oros', 'copas', 'espadas', 'bastos']:
        jugadas = mesa.estado[palo]
        print(f"  {palo.capitalize():<8}: {sorted(jugadas)}")

def main():
    print("Bienvenido al Cinquillo contra un Bot\n")

    # Crear jugadores
    jugadores = [
        BotJugador("Bot1"),
        BotJugador("Bot2")
    ]

    # Crear motor de juego
    motor = MotorJuego()
    motor.nueva_partida(jugadores)

    # Mostrar manos iniciales
    print("\nManos iniciales:")
    for jugador in jugadores:
        print(f"{jugador.nombre}: {[str(carta) for carta in sorted(jugador.mano, key=lambda c: (c.palo, c.valor))]}")

    print("\nComienza la partida...\n")

    # Log inicial
    for entrada in motor.partida.log:
        print(entrada)

    # FORZAR que el primer jugador juegue el 5 de oros automáticamente
    jugador_inicial = motor.partida.jugadores[motor.partida.turno_actual]
    cinco_oros = next((c for c in jugador_inicial.mano if c.palo == 'oros' and c.valor == 5), None)

    if cinco_oros:
        jugador_inicial.mano.remove(cinco_oros)
        motor.partida.mesa.colocar_carta(cinco_oros)
        motor.partida.historial.append((jugador_inicial.nombre, cinco_oros))
        evento = f"{jugador_inicial.nombre} juega: 5 de oros"
        motor.partida.registrar_evento(evento)
        print(evento)
        mostrar_estado_mesa(motor.partida.mesa)
        motor.partida.siguiente_turno()

    # Jugar turnos normales
    while not motor.partida.finalizada:
        jugador = motor.partida.jugadores[motor.partida.turno_actual]
        print(f"\nTurno de {jugador.nombre}")

        if jugador.tiene_jugada_valida(motor.partida.mesa):
            carta = jugador.jugar(motor.partida.mesa)
            if carta:
                motor.partida.mesa.colocar_carta(carta)
                motor.partida.historial.append((jugador.nombre, carta))
                evento = f"{jugador.nombre} juega: {carta}"
                motor.partida.registrar_evento(evento)
                print(evento)
        else:
            evento = f"{jugador.nombre} pasa"
            motor.partida.registrar_evento(evento)
            print( evento)

        mostrar_estado_mesa(motor.partida.mesa)

        if any(len(j.mano) == 0 for j in motor.partida.jugadores):
            motor.partida.finalizada = True
            ganador = [j for j in motor.partida.jugadores if len(j.mano) == 0][0]
            evento = f"{ganador.nombre} ha ganado la partida."
            motor.partida.registrar_evento(evento)
            print(evento)
            break

        motor.partida.siguiente_turno()

    # Mostrar resumen final
    print("\nEstado final de las manos:")
    for jugador in jugadores:
        print(f"{jugador.nombre} - Cartas restantes: {[str(carta) for carta in jugador.mano]}")

    print("\nRegistro completo de la partida:")
    for entrada in motor.partida.log:
        print(entrada)

    # Guardar log en archivo de texto
    with open("log_partida.txt", "w", encoding="utf-8") as f:
        f.write("REGISTRO DE LA PARTIDA\n")
        f.write("=======================\n\n")
        for entrada in motor.partida.log:
            f.write(f"{entrada}\n")
        f.write("\nEstado final de las manos:\n")
        for jugador in jugadores:
            f.write(f"{jugador.nombre} - Cartas restantes: {[str(carta) for carta in jugador.mano]}\n")

    print("\nLog guardado en 'log_partida.txt'")



    # Guardar log estructurado
    with open("log_partida_estructurado.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["accion", "jugador", "juega", "numero", "palo"])

        turno = 0
        for linea in motor.partida.log:
            if "juega:" in linea:
                try:
                    jugador, resto = linea.split(" juega:")
                    carta_str = resto.strip()  # "5 de bastos"
                    # Extraer número y palo
                    match = re.match(r"(\d+)\s+de\s+(\w+)", carta_str)
                    if match:
                        numero, palo = match.groups()
                        writer.writerow([turno, jugador.strip(), 1, int(numero), palo])
                        turno += 1
                except ValueError:
                    continue  # línea mal formada

            elif "pasa" in linea:
                jugador = linea.split(" pasa")[0].strip()
                writer.writerow([turno, jugador, 0, "", ""])
                turno += 1

    print("Log estructurado guardado en 'log_partida_estructurado.csv'")

if __name__ == "__main__":
    main()

