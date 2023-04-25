

class MatchManager():

    def __init__(self):
        self.lobbies = [
            "jcx27n",
            "kp8c99",
            "djmrx4",
            "rzwcfg",
            "dytfzs"
        ]
        self.available_lobbies = []
        self.busy_lobbies = {}

        for code in self.lobbies:
            self.available_lobbies.append(code)

    def get_lobbies(self):
        return self.available_lobbies, self.busy_lobbies

    def lobbies_available(self) -> int:
        return len(self.available_lobbies)
    
    def start_match(self) -> str:
        if not self.available_lobbies:
            return ""
        lobby_code = self.available_lobbies.pop(0)
        self.busy_lobbies[lobby_code] = None
        return lobby_code
    
    def end_match(self, lobby_code: str):
        if lobby_code in self.busy_lobbies.keys():
            self.busy_lobbies.pop(lobby_code)
            self.available_lobbies.append(lobby_code)
            print(self.available_lobbies)