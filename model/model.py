import copy
from datetime import datetime

import networkx as nx
from geopy.distance import geodesic

from database.dao import DAO



class Model:
    def __init__(self):
        self._nodes = []
        self._edges = []
        self.G = nx.Graph()
        self._idMap = {}
        self.soluzione_best=[]


    def get_anno(self):
        anni=DAO.get_anno()
        return anni


    def get_shapes(self,anno):
        shapes=DAO.get_all_shapes(anno)
        return shapes




    def build_graph(self,anno,forma):
        self.G.clear()
        self._nodes=[]
        self._edges=[]
        states = DAO.get_states()
        states_a_f=DAO.get_states_by_anno(anno,forma)
        archi=DAO.get_archi()
        for s in states:
            if s.id.lower() in states_a_f:
                s.avvistamenti=states_a_f[s.id.lower()]
            self._idMap[s.id] = s
            self.G.add_node(s)


        for arco in archi:
            s1=arco['s1']
            s2=arco['s2']

            if s1==s2:
                continue

            if s1 in self._idMap and s2 in self._idMap:
                nodo1=self._idMap[s1]
                peso1=nodo1.avvistamenti
                nodo2=self._idMap[s2]
                peso2=nodo2.avvistamenti
                peso_totale=peso1+peso2
                self.G.add_edge(nodo1,nodo2,weight=peso_totale)

        self._nodes=list(self.G.nodes())

        return self.G

    def get_path(self):
        self.best_path=[]
        self.best_distance=0
        partial=[]
        for n in self._nodes:
            partial.clear()
            partial.append(n)
            self.ricorsione(partial,0)

        return self.best_path

    def ricorsione(self,partial,peso_ultimo_arco):

        distanza_attuale=self.calcola_distanza_totale(partial)

        if distanza_attuale>self.best_distance:
            self.best_distance=distanza_attuale
            self.best_path=copy.deepcopy(partial)


        ultimo_nodo=partial[-1]
        vicini=self.G.neighbors(ultimo_nodo)

        for vicino in vicini:
            peso=self.G[ultimo_nodo][vicino]['weight']

            if peso>peso_ultimo_arco:

                partial.append(vicino)
                self.ricorsione(partial,peso)
                partial.pop()





    def calcola_distanza_totale(self, path):
        distanza = 0
        if len(path) < 2:
            return 0

        for i in range(len(path) - 1):
            n1 = path[i]
            n2 = path[i+1]


            coord1 = (n1.lat, n1.lng)
            coord2 = (n2.lat, n2.lng)

            distanza += geodesic(coord1, coord2).km

        return distanza


























