class ConnectionManager:
    def __init__(self):
        self.active = {}
    
    async def connect(self, sid, user):
        self.active[sid] = user
    
    async def disconnect(self, sid):
        self.active.pop(sid, None)

manager = ConnectionManager()