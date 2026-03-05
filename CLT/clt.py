from manim import *
from os import path

import random

class CLT(Scene):
    
    def cargar(self):
        imagenes = {}
        for x in range(11):
            if x == 0:
                imagenes['b'] = ImageMobject(path.join('assets', 'b.png'))
            elif x == 1:
                imagenes[1] = ImageMobject(path.join('assets', 'a.png'))
            else:
                imagenes[x] = ImageMobject(path.join('assets', f'{x}.png'))
        return imagenes
    
    def construct(self):
        img_cartas = self.cargar()
        
        s_lentos = 2
        s_rapidos = 1500
        n_cartas = 10
        
        frecuencias = [0] * 91 #array de 91 ceros (total de sumas posibles)
        
        histograma = BarChart(
            values=frecuencias,
            y_range=[0, 5, 1],
            y_length=3,
            x_length=10,
            bar_colors=[BLUE]
        )
        histograma.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(histograma))
        
        # Primera iteracion
        for i in range(s_lentos):
            # seleccion valores de cartas
            valores = [random.randint(1, 10) for _ in range(n_cartas)]
            sum_mano = sum(valores)
            
            mano_completa = Group() 
            
            for i in valores:
                mano_completa.add(img_cartas[i].copy()) #creacion de la mano

            mano_completa.arrange_in_grid(rows=2, cols=5, buff=(0.05, 0.5)) #placement
            mano_completa.to_edge(UP, buff=0.5)
                
            self.play( #animacion de entrada
                LaggedStart(
                    *[FadeIn(c, shift=UP*0.5) for c in mano_completa],
                    lag_ratio=0.15
                ),
                run_time=1
            )
            
            # muestra suma
            sum_text = Text(f"Suma: {sum_mano}", font_size=32, color=GRAY_B)
            sum_text.next_to(mano_completa, DOWN, buff=0.2)
            
            self.play(Write(sum_text))
            
            # actualiza histograma
            freq_index = sum_mano - 10
            frecuencias[freq_index] += 1
            
            max_f = max(frecuencias) 
            y_max = max(5, max_f + 2) #actualiza el max del y axis
            
            histograma_2 = BarChart(
                values=frecuencias,
                y_range=[0, y_max, max(1, y_max // 5)],
                y_length=3,
                x_length=10,
                bar_colors=[BLUE]
            )
            histograma_2.move_to(histograma)
            
            self.play(ReplacementTransform(histograma, histograma_2))
            histograma = histograma_2
            self.wait(1)
            
            # borra todo excepto el titulo para la siguiente iteracion
            if i < s_lentos - 1:
                self.play(
                    FadeOut(mano_completa, shift=DOWN*0.5),
                    FadeOut(sum_text)
                )
            else:
                self.play(
                    FadeOut(mano_completa),
                    FadeOut(sum_text),
                )
                
        #Samples rapidos
        for i in range(s_rapidos):
            #mismo de antes, obtiene valores, suma, actualiza frecuencias
            valores = [random.randint(1, 10) for _ in range(n_cartas)]
            sum_mano = sum(valores)
            freq_index = sum_mano - 10
            frecuencias[freq_index] += 1
            
            #crea la mano
            mano_completa = Group() 
            for v in valores:
                mano_completa.add(img_cartas[v].copy())

            mano_completa.arrange_in_grid(rows=2, cols=5, buff=(0.05, 0.5))
            mano_completa.scale(0.5)
            mano_completa.to_corner(UL)
            
            #muestra suma
            sum_text = Text(f"Suma: {sum_mano}", font_size=18, color=GRAY_B)
            sum_text.next_to(mano_completa, DOWN, buff=0.2)
                
            max_f = max(frecuencias)
            y_max = max(5, max_f + max_f // 10 + 1) #actualiza el max del y axis (min 5, max 10% mas)

            histograma_2 = BarChart( #nuevo histograma
                values=frecuencias,
                y_range=[0, y_max, max(1, y_max // 5)],
                y_length=3,
                x_length=10,
                bar_colors=[BLUE]
            )
            histograma_2.move_to(histograma) #sobreescribe el anterior
            
            # actualiza sin animacion
            self.remove(histograma)
            self.add(mano_completa, sum_text, histograma_2)
            
            histograma = histograma_2
            
            self.wait(1/60) #1 frame por iteracion
            
            # borra todo excepto el titulo para la siguiente iteracion
            self.remove(mano_completa, sum_text)
            
        self.wait(2)
        
        # cleanup
        self.play(
            FadeOut(histograma)
        )
