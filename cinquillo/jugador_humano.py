# cinquillo/jugador_humano.py
from .jugador import Jugador
from .carta import Carta
from .mesa import Mesa

class JugadorHumano(Jugador):
    def jugar(self, mesa: Mesa) -> Carta | None:
        print(f"\nTu mano: ")
        for idx, carta in enumerate(self.mano):
            print(f"{idx}: {carta}")

        # Filtrar jugadas válidas
        jugadas_validas = [(i, carta) for i, carta in enumerate(self.mano) if mesa.puede_colocar(carta)]

        if not jugadas_validas:
            print("No tienes jugadas válidas. Pasas turno.\n")
            return None

        print("\nCartas que puedes jugar:")
        for nuevo_idx, (mano_idx, carta) in enumerate(jugadas_validas):
            print(f"{nuevo_idx}: {carta} (índice en mano: {mano_idx})")

        # Pedir elección
        while True:
            eleccion = input("Escribe el número de la carta que quieres jugar (según lista anterior): ")
            if eleccion.isdigit():
                eleccion = int(eleccion)
                if 0 <= eleccion < len(jugadas_validas):
                    idx_mano, carta_elegida = jugadas_validas[eleccion]
                    self.mano.pop(idx_mano)  # Quitar de la mano
                    return carta_elegida
            print("Entrada inválida. Intenta de nuevo.")
