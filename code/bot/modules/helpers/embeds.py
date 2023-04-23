from discord import Embed, User, Colour

# CHALLENGES

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

# MATCHES

def match_in_progress(challenger: User, opponent: User) -> Embed:
    e = Embed(title=f"{challenger.display_name} vs {opponent.display_name} - In Progress <a:discordIsTyping:1005500222899765308>")
    e.color = Colour.green()
    return e

def match_ended(challenger: User, opponent: User) -> Embed:
    e = Embed(title=f"{challenger.display_name} vs {opponent.display_name} - Match Ended")
    e.color = Colour.light_gray()
    return e

# META

def lobbies(available_lobbies: "list[str]", busy_lobbies: dict):
    e = Embed(title="GTCGTGTM lobbies:")
    e.color = Colour.green()
    if busy_lobbies:
        pass
        field = "\n".join(map(lambda code: "• " + code, busy_lobbies.keys()))
        e.add_field(name="In Progress:", value=field)
    if available_lobbies:
        field = "\n".join(map(lambda code: "• " + code, available_lobbies))
        e.add_field(name="Available:", value=field)
    return e