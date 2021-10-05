from src.objects import *
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="ERS Simulation")
"""
# ERS Game

## Rules

### THE PACK
A standard 52-card deck is used and can include Jokers.

### THE DEAL
Deal cards one at a time face down, to each player until all the cards have been dealt evenly. Without looking at any of the cards, each player squares up their hand into a neat pile in front of them.

### THE PLAY
Starting to the left of the dealer players pull the top card off their pile and place it face-up in the middle. If the card played is a number card, the next player puts down a card, too. This continues around the table until somebody puts down a face card or an Ace (J, Q, K, or A).

When a face card or an ace is played, the next person in the sequence must play another face card or an ace in order for play to continue.

If the next person in the sequence does not play a face card or an ace within their allotted chance, the person who played the last face card or an ace wins the round and the whole pile goes to them. The winner begins the next round of play.

The only thing that overrides the face card or an ace rule is the slap rule. The first person to slap the pile of cards when the slap rule is put into effect is the winner of that round. If it cannot be determined who was the first to slap the pile, the person with the most fingers on top wins.

### SLAP RULES
Double – When two cards of equivalent value are laid down consecutively. Ex: 5, 5
Sandwich – When two cards of equivalent value are laid down consecutively, but with one card of different value between them. Ex: 5, 7, 5
Top Bottom – When the same card as the first card of the set is laid down.
Tens – When two cards played consecutively (or with a letter card in between) add up to 10. For this rule, an ace counts as one. Ex: 3, 7 or A, K, 9
Jokers – When jokers are used in the game, which should be determined before game play begins. Anytime someone lays down a joker, the pile can be slapped.
Four in a row – When four cards with values in consistent ascending or descending order is placed. Ex: 5, 6, 7, 8 or Q, K, A, 2
Marriage – When a queen is placed over or under a king. Ex: Q, K or K,Q

You must add one or two cards to the bottom of the pile if you slap the pile when it was not slappable.

Continue playing even if you have run out of cards. As long as you don't slap at the wrong time, you are still allowed to "slap in" and get cards! Everyone should try to stay in the game until you have a single winner who obtains all the cards

### HOW TO KEEP SCORE
The player, who has all of the cards at the end of the game, wins.
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
    players = [
        Player("player%s" % num, slappingSkills["player%s" % num])
        for num in range(numPlayers)
    ]
    game = Game(players)
    game.shuffle_and_deal()
    with st.spinner():
        game.play()
    results = game.getResults()
    # st.write(results)
    # st.write([player.slapping_skill for player in game.players])
    # st.write(game.slapping_prob_cutoffs)

    fig = px.line(
        results, x="turn", y="cards", color="player", title="ERS Game"
    )
    st.plotly_chart(fig)
