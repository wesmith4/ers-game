from src.objects import *
import streamlit as st
import plotly.express as px

"""
# ERS Game
"""

numPlayers = st.number_input(
    "Choose number of players:", value=3, min_value=2, max_value=6, step=1
)
slappingSkills = {}

if numPlayers:
    for i in range(numPlayers):
        slappingSkills["player%s" % i] = st.slider(
            "Player %s slapping skill" % i,
            min_value=0.00,
            max_value=1.00,
            step=0.01,
            value=0.50,
        )

playGame = st.button("Play Game")

if playGame:
    players = [Player("player%s" % num) for num in range(numPlayers)]
    game = Game(players)
    game.shuffle_and_deal()
    with st.spinner():
        game.play()
    results = game.getResults()

    px.line(results, x="turn", y="cards", color="player", title="ERS Game")
