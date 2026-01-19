import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.id_map = {}
        self.nodi = []
        self.archi = []

    def load_years(self):
        return DAO.get_all_years()

    def load_shapes(self,year):
        return DAO.get_shapes(year)

    def build_graph(self, year, shape):
        self.G.clear()

        stati = DAO.get_all_states() #lista di oggetti
        self.nodi.clear()
        for state in stati:
            self.nodi.append(state)
        self.G.add_nodes_from(self.nodi)

        self.id_map = {s.id: s for s in stati}
        #creo archi
        self.archi.clear()
        edges = DAO.get_edges(year, shape) #lista di tuple (e1,e2,weight)
        for e in edges:
            self.archi.append((self.id_map[e[0]], self.id_map[e[1]], e[2]))
        self.G.add_weighted_edges_from(self.archi)

    def somma_pesi_per_stato(self):
        risultato = []
        for nodo in self.G.nodes():
            somma = 0
            for a in self.G.edges(nodo, data = True): #restituisce una lista di tuple (nodo, vicino, weight), se non metto data = True non restituice l'attributo
                somma += a[2]['weight']
            risultato.append((nodo.id, somma))
        return risultato

    def get_num_of_nodes(self):
        return self.G.number_of_nodes()

    def get_num_of_edges(self):
        return self.G.number_of_edges()







