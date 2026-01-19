from dataclasses import dataclass

@dataclass
class State:
    id:str
    name:str
    capital:str
    lat:int
    lng:int
    area:int
    population:int
    neighbors:str

    def __hash__(self):
        return hash(self.id)



    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
