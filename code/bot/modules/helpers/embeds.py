from discord import Embed, User, Colour

def closed_challenge(challenger: User, opponent: User) -> Embed:
    e = Embed(title=f"{challenger.display_name} has challenged {opponent.display_name} to a game of GTCG The Game:tm:!")
    e.color = Colour.green()
    return e

def open_challenge(challenger: User) -> Embed:
    e = Embed(title=f"{challenger.display_name} has opened a challenge to a game of GTCG The Game:tm:!")
    e.color = Colour.green()
    return e

def decline_challenge(opponent: User) -> Embed:
    e = Embed(title=f"Challenge declined by {opponent.display_name}.")
    e.color = Colour.red()
    return e

def cancel_challenge(challenger: User) -> Embed:
    e = Embed(title=f"Challenge cancelled by {challenger.display_name}.")
    e.color = Colour.red()
    return e