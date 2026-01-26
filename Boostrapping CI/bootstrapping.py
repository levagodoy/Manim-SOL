from manim import *
from os import path
from collections import Counter

import numpy as np
import pandas as pd




class Bootstrap(Scene):
    def cargar_csv(self):
        csv = pd.read_csv(path.join('Assets', 'sample_casen2017.csv'))
        csv = csv[csv['sexo'] == 2]

        np.random.seed(0)
        def bs_mean(n):
            for x in range(n):
                sample = csv.sample(n = len(csv), replace = True)
                mean = sample['yautcor'].mean()
                yield mean
                
        data = np.fromiter(bs_mean(5000), dtype= int, count=5000)
        
        hist, ejes = np.histogram(data, bins= 40)
        
        valores = list(hist)
        labels = [f'{int(eje)}' for eje in ejes[:-1]]
        
        return valores, labels
    
    
    def construct(self):
        valores, labels = self.cargar_csv()
        
        codigo = Code(
            code_file = 'algorithm.R',
            language = 'R',
            background = 'window',
            background_config={"stroke_color": "maroon"}
        )
        codigo.scale(0.5)
        '''
        chart = BarChart(
            values = valores,
            bar_names = labels,
            y_range = [0, 600, 50],
            x_length = 10,
            y_length=6,
            x_axis_config = {'font_size': 8}
        )
        
        self.add(chart)
        '''
        
        bloque1 = (codigo[2][0], codigo[2][1], codigo[2][2], codigo[2][3], codigo[2][4],
                   codigo[2][5], codigo[2][6])
        
        data_b = (codigo[2][1], codigo[2][2], codigo[2][3])
        
        
        box1 = SurroundingRectangle(*bloque1, corner_radius=0.1, buff = 0.05)
        box2 = SurroundingRectangle(*data_b, corner_radius=0.1, buff = 0.05)
        box3 = SurroundingRectangle(*codigo[2][4], corner_radius=0.1, buff = 0.05)
        box4 = SurroundingRectangle(*codigo[2][5], corner_radius=0.1, buff = 0.05)
        
        self.add(codigo)
        self.play(Create(box1))
        self.wait()
        self.play(ReplacementTransform(box1, box2))
        self.wait()
        self.play(ReplacementTransform(box2, box3))
        self.wait()
        self.play(ReplacementTransform(box3, box4))
        self.wait()
        self.play(ReplacementTransform(box4, box1))