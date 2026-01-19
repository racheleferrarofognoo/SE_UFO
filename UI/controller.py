import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        lista_anni = self._model.load_years()
        for anno in lista_anni:
            self._view.dd_year.options.append(ft.dropdown.Option(anno))
        self._view.update()

    def populate_dd_shape(self):
        self._view.dd_shape.options.clear()
        anno_selezionato = self._view.dd_year.value
        if anno_selezionato is None:
            self._view.show_alert('Select year')
            return

        print("Anno selezionato nel dropdown:", anno_selezionato)

        shapes = self._model.load_shapes(anno_selezionato)
        for shape in shapes:
            self._view.dd_shape.options.append(ft.dropdown.Option(shape))
        self._view.update()

    def change_option_year(self, e):
        self.populate_dd_shape()

    def handle_graph(self, e):
        self._view.lista_visualizzazione_1.controls.clear()
        """ Handler per gestire creazione del grafo """
        if self._view.dd_year.value is None or self._view.dd_shape.value is None:
            self._view.show_alert('Select year and shape')

        self._model.build_graph(self._view.dd_year.value, self._view.dd_shape.value)
        nodi = self._model.get_num_of_nodes()
        archi = self._model.get_num_of_edges()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Numero di vertici: {nodi}, numero di archi: {archi}"))
        for nodo in self._model.somma_pesi_per_stato():
            self._view.lista_visualizzazione_1.controls.append(
                ft.Text(f"Nodo {nodo[0]}, somma pesi su archi = {nodo[1]}"))

        self._view.update()


    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
