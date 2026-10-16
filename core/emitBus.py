# Este es el sistema de eventos, se encarga de conectar todo Maisapaint

class Emit:

    def __init__(self):

        # Crea un diccionario donde se guardan las referencias a las funciones

        self.eventListeners = {}
        
    def conect(self, eventName, function):

        # Recibe un nombre y la referencia de una funcion/metodo

        if eventName not in self.eventListeners:
            self.eventListeners[eventName] = []

        # Lo agrega al final del diccionario
            
        self.eventListeners[eventName].append(function)
        
    def emit(self,eventName, *args, **kwargs):

        #Primero das el nombre de la señal, y luego los argumentos que recibira la funcion a llamar

        if eventName in self.eventListeners:
            for function in self.eventListeners[eventName]:

                # Llama a la funcion

                function(*args, **kwargs)
                
# Objeto que guarda todas las funciones

bus = Emit()