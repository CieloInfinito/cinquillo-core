import gymnasium as gym
from gymnasium import spaces

import numpy as np
from cinquillo.motor import MotorJuego
from cinquillo.bot_jugador import BotJugador
from cinquillo.carta import Carta

class CinquilloEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.motor = MotorJuego()
        self.agent = BotJugador("Agente")
        self.opponent = BotJugador("Oponente")
        self.jugadores = [self.agent, self.opponent]

        self.palos = ['oros', 'copas', 'espadas', 'bastos']
        self.valores = list(range(1, 8)) + list(range(10, 13))

        self.action_space = spaces.Discrete(40)
        # Observación: mano del agente (40), estado mesa (40), cartas del oponente (1 valor)
        self.observation_space = spaces.MultiBinary(81)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.motor.nueva_partida(self.jugadores)
        obs = self._get_obs()
        return obs, {}

    def step(self, action):
        reward = -0.01  # Penalización leve por turno
        done = False
        jugada_valida = False

        carta_idx = action
        carta = self._indice_a_carta(carta_idx)

        if carta in self.agent.mano:
            if self.motor.partida.mesa.puede_colocar(carta):
                self.agent.mano.remove(carta)
                self.motor.partida.mesa.colocar_carta(carta)
                jugada_valida = True
                reward = 1.0 + 0.2 * (40 - len(self.agent.mano))  # bonificación por progreso
                if len(self.agent.mano) == 0:
                    reward = 10.0
                    done = True
            else:
                reward = -1.0  # castigo por jugar ilegal
        else:
            reward = -1.0  # acción inválida (no tiene esa carta)

        self.motor.partida.siguiente_turno()

        # Turno del oponente
        oponente = self.opponent
        jugadas_validas = [c for c in oponente.mano if self.motor.partida.mesa.puede_colocar(c)]
        if jugadas_validas:
            carta_op = self.np_random.choice(jugadas_validas)
            oponente.mano.remove(carta_op)
            self.motor.partida.mesa.colocar_carta(carta_op)
        self.motor.partida.siguiente_turno()

        if len(oponente.mano) == 0:
            reward = -5.0
            done = True

        # Penaliza pasar si tenía jugadas válidas
        if not jugada_valida and any(self.motor.partida.mesa.puede_colocar(c) for c in self.agent.mano):
            reward -= 0.5

        obs = self._get_obs()
        info = {}
        return obs, reward, done, False, info  # el cuarto valor es \"truncated\"

    def _get_obs(self):
        obs = np.zeros(81, dtype=np.int8)

        for carta in self.agent.mano:
            idx = self._carta_a_indice(carta)
            obs[idx] = 1

        for palo in self.palos:
            for valor in self.motor.partida.mesa.estado[palo]:
                idx = self._carta_a_indice(Carta(palo, valor)) + 40
                obs[idx] = 1

        obs[80] = len(self.opponent.mano)  # tamaño mano oponente
        return obs

    def _carta_a_indice(self, carta):
        p_idx = self.palos.index(carta.palo)
        v_idx = self.valores.index(carta.valor)
        return p_idx * len(self.valores) + v_idx

    def _indice_a_carta(self, idx):
        p_idx = idx // len(self.valores)
        v_idx = idx % len(self.valores)
        return Carta(self.palos[p_idx], self.valores[v_idx])

    def render(self, mode="human"):
        print("\nMesa:")
        for palo in self.palos:
            print(f"{palo}: {sorted(self.motor.partida.mesa.estado[palo])}")
        print("\nMano agente:", [str(c) for c in self.agent.mano])
        print("Mano oponente:", len(self.opponent.mano))
