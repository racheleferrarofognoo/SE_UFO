from dataclasses import dataclass

@dataclass
class State:
    id:str
    name:str
    capital:str
    lat:float
    lng:float
    area:int
    population:str
    neighbors:str
    avvistamenti: int=0

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    def __hash__(self):
        return hash(self.id)