from __future__ import annotations

import json

class ServerSettings:
    Servers : dict[str,ServerSettings] = {}

    def __init__(self, server_id : str, Settings : dict = {}) -> None: #constructor
        cusses = ["shit","fuck","bitch","hoe","nigga","nigger","faggot","slut"]
        self.id : str = server_id
        self.cuss = Settings.get("cuss", True) #use .get() to provide a default value in case its a new server
        self.cuss_keys = Settings.get("cuss_keys", cusses)

        self.strikes = Settings.get("strikes",{})

    def ToDict(self) -> dict: #Add anything here that u want to save
        result = {}
        result["cuss"] = self.cuss
        result["cuss_keys"] = self.cuss_keys
        result["strikes"] = self.strikes
        return result

    # INDIVIDUAL SERVERS
    @staticmethod
    def GetServer(server_id : str) -> ServerSettings:
        if not isinstance(server_id, str): server_id = str(server_id)
        return ServerSettings.Servers[server_id]

    @staticmethod
    def DeleteServer(server_id : str) -> None:
        if not isinstance(server_id, str): server_id = str(server_id)
        ServerSettings.Servers.pop(key=server_id)

    @staticmethod
    def AddServer(server_id : str, force=True) -> None:
        if not isinstance(server_id, str): server_id = str(server_id)
        if server_id in ServerSettings.Servers:
            if not force: return
        ServerSettings.Servers[server_id] = ServerSettings(server_id=server_id)

    # ALL SERVERS 
    @staticmethod
    def LoadServers(filename="data.json") -> None:
        try: 
            Data = json.load(open(filename, mode='r'))
            for server_id in Data:
                ServerSettings.Servers[server_id] = ServerSettings(server_id, Data[server_id])
        except:
            open(filename, mode='w').close()

    @staticmethod
    def SaveServers(filename="data.json") -> None:
        result = {}
        for server_id in ServerSettings.Servers:
            server : ServerSettings = ServerSettings.Servers[server_id]
            result[server_id] = server.ToDict()
        json.dump(result, open(filename, mode='w'), indent=4) # 'w' meaning write