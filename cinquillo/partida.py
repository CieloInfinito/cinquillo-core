# cinquillo/partida.py (actualizado)

from .mesa import Mesa
from .carta import Carta
from .jugador import Jugador
import random

class Partida:
    def __init__(self, jugadores: list[Jugador]):
        self.jugadores = jugadores
        self.mesa = Mesa()
        self.turno_actual = 0
        self.historial = []  # (jugador, carta)
        self.finalizada = False
        self.log: list[str] = []  # ✅ Nuevo atributo

    def registrar_evento(self, mensaje: str):
        self.log.append(mensaje)

    def iniciar(self):
        baraja = [Carta(palo, valor) for palo in ['oros', 'copas', 'espadas', 'bastos']
                  for valor in list(range(1, 8)) + list(range(10, 13))]
        random.shuffle(baraja)
        num_jugadores = len(self.jugadores)
        for jugador in self.jugadores:
            jugador.mano.clear()

        for i, carta in enumerate(baraja):
            self.jugadores[i % num_jugadores].mano.append(carta)

        for i, jugador in enumerate(self.jugadores):
            if any(carta.palo == 'oros' and carta.valor == 5 for carta in jugador.mano):
                self.turno_actual = i
                self.registrar_evento(f"{jugador.nombre} tiene el 5 de oros y comienza la partida.")
                break

        # Asegurar que el 5 de oros esté en juego
        if not any(Carta('oros', 5).valor == c.valor and Carta('oros', 5).palo == c.palo
                   for j in self.jugadores for c in j.mano):
            self.jugadores[0].mano.append(Carta('oros', 5))
            self.registrar_evento("⚠️ Se añadió manualmente el 5 de oros a un jugador.")

    def siguiente_turno(self):
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        if any(len(j.mano) == 0 for j in self.jugadores):
            self.finalizada = True
            self.registrar_evento("✅ La partida ha terminado: un jugador se quedó sin cartas.")
