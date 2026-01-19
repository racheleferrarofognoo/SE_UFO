import flet as ft
from geopy.distance import geodesic

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
    def populate_dd(self):
        self.populate_dd_anno()


    def populate_dd_anno(self):
        """ Metodo per popolare i dropdown """
        # TODO
        anni=self._model.get_anno()

        self._view.dd_year.options=[ft.dropdown.Option(a) for a in anni]

        self._view.page.update()

    def leggi_anno(self,e):
        self.populate_dd_forma()



    def populate_dd_forma(self):

        anno = self._view.dd_year.value

        shapes=self._model.get_shapes(anno)

        if anno is None:
            self._view.show_alert("seleziona anno!")
        else:
            self._view.dd_shape.options.clear()
            self._view.dd_shape.options = [ft.dropdown.Option(s) for s in shapes]

        self._view.page.update()



    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        anno = self._view.dd_year.value
        forma=self._view.dd_shape.value
        if anno is None:
            self._view.show_alert("seleziona anno!")
        elif forma is None:
            self._view.show_alert("seleziona forma!")
        else:
            self.grafo=self._model.build_graph(anno,forma)
            self._view.lista_visualizzazione_1.controls.clear()
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Numero di vertici: {self.grafo.number_of_nodes()} Numero di archi: {self.grafo.number_of_edges()}"))
            for nodo in self.grafo.nodes():
                peso=0
                for vicino in self.grafo.neighbors(nodo):
                    peso+=self.grafo[nodo][vicino]['weight']
                self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Nodo {nodo}, somma pesi su archi= {peso}"))

        self._view.page.update()




    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO

        if self.grafo is None:
            self._view.show_alert("crea grafo!")
        else:
            best_path=self._model.get_path()

            self._view.lista_visualizzazione_2.controls.clear()

            self._view.lista_visualizzazione_2.controls.append(
                ft.Text(f"Peso cammino massimo (Distanza Km): {self._model.calcola_distanza_totale(best_path)}")
            )
            for i in range(len(best_path) - 1):
                distanza=0
                s1 = best_path[i]
                s2 = best_path[i + 1]
                w = self._model.G[s1][s2]['weight']
                coord1 = (s1.lat, s1.lng)
                coord2 = (s2.lat, s2.lng)

                distanza += geodesic(coord1, coord2).km

                self._view.lista_visualizzazione_2.controls.append(ft.Text(f"{s1.id}--->{s2.id}: weight {w}  distance {distanza}"))

            self._view.page.update()





