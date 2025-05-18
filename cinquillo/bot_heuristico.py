# cinquillo/bot_heuristico.py
from .jugador import Jugador
from .carta import Carta
from .mesa import Mesa

class BotHeuristico(Jugador):
    def jugar(self, mesa: Mesa) -> Carta | None:
        jugables = [carta for carta in self.mano if mesa.puede_colocar(carta)]

        if not jugables:
            return None  # No hay jugadas válidas

        # Crear un set para acceso rápido a las cartas propias
        valores_mano = {
            (c.palo, c.valor)
            for c in self.mano
        }

        # Buscar jugables que tengan consecutiva en mano
        for carta in jugables:
            consecutivos = [(carta.palo, carta.valor - 1), (carta.palo, carta.valor + 1)]
            if any(consec in valores_mano for consec in consecutivos):
                self.mano.remove(carta)
                return carta

        # Si ninguna tiene consecutiva, jugar la primera jugable
        carta = jugables[0]
        self.mano.remove(carta)
        return carta
