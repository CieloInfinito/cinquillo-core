from cinquillo.carta import Carta
from cinquillo.bot_jugador import BotJugador
from cinquillo.mesa import Mesa

def test_bot_juega_si_puede():
    mesa = Mesa()
    bot = BotJugador("Bot")
    cinco = Carta('oros', 5)
    seis = Carta('oros', 6)
    bot.mano = [seis, cinco]
    jugada = bot.jugar(mesa)
    assert jugada == cinco
    mesa.colocar_carta(jugada)
    assert seis in bot.mano