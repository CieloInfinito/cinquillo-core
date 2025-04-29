# cinquillo/bot_jugador.py
from .jugador import Jugador
from .carta import Carta
from .mesa import Mesa

class BotJugador(Jugador):
    def jugar(self, mesa: Mesa) -> Carta | None:
        # Juega la primera carta válida por orden
        for carta in sorted(self.mano, key=lambda c: (c.palo, c.valor)):
            if mesa.puede_colocar(carta):
                self.mano.remove(carta)
                return carta

        # No tiene jugada válida
        return None
