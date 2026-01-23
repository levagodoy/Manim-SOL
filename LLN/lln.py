from manim import *
import numpy as np

class LLN(Scene):
    def construct(self):
        # Variables mínimas
        intentos = 10000
        EV = 0.5
        
        # Variables aleatorias
        flips = np.random.randint(0, 2, intentos) # 0 = sello, 1 = cabeza
        conjunto_intentos = np.arange(1, intentos + 1)
        
        promedio = np.cumsum(flips) / conjunto_intentos
        varianza = promedio * (1 - promedio)
        error_estandar = np.sqrt(varianza / conjunto_intentos)
        
        # Objeto grafico
        grafico = Axes(
            x_range = [0, intentos, 2000], 
            y_range = [0, 1, 0.1],
            x_length = 10,
            y_length = 6,
            axis_config = {'color': BLUE},
            x_axis_config = {'numbers_to_include': np.arange(0, intentos + 1, 2000)},
            y_axis_config = {'numbers_to_include': [0, 0.5, 1]}
        ).to_edge(DOWN)
        
        proporcion = MathTex(r"\hat{p}_{\text{Cabezas}}")
        x_label = grafico.get_x_axis_label('(n) Intentos')
        y_label = grafico.get_y_axis_label(proporcion)
        
        # Linea central (EV)
        target_line = grafico.get_horizontal_line(
            grafico.c2p(intentos, EV),
            color = RED
        ).set_stroke(width=2).set_opacity(0.5)
        
        target_label = Tex(f'Valor Esperado ({EV})', color = RED, font_size = 22)
        target_label.next_to(target_line, UP, buff=0.1)
        
        # Creacion puntos de toda la animacion
        camino = VMobject(color = YELLOW, stroke_width = 1)
        puntos = [grafico.c2p(n, avg) for n, avg in enumerate(promedio, start=1)]
        camino.set_points_as_corners(puntos)
        
        # Trackers
        n_tracker = ValueTracker(1)
        
        # Labels
        n_label = Integer(0).set_color(WHITE)
        n_texto = Tex('Intentos: ')
        n_group = VGroup(n_texto, n_label).arrange(RIGHT)
        
        avg_label = DecimalNumber(0, num_decimal_places=3).set_color(YELLOW)
        avg_texto = Tex('Media: ')
        avg_group = VGroup(avg_texto, avg_label).arrange(RIGHT)
        
        se_label = DecimalNumber(0, num_decimal_places=4).set_color(ORANGE)
        se_texto = Tex('Error Estándar: ')
        se_group = VGroup(se_texto, se_label).arrange(RIGHT)
        
        stats = VGroup(n_group, avg_group, se_group).arrange(DOWN, aligned_edge=LEFT).scale(0.6)
        stats.to_corner(UR)
        
        # Updaters
        n_label.add_updater(lambda m: m.set_value(int(n_tracker.get_value())))
        avg_label.add_updater(lambda m: m.set_value(
            promedio[int(n_tracker.get_value() - 1)]
        ))
        se_label.add_updater(lambda m: m.set_value(
            error_estandar[int(n_tracker.get_value() - 1)]
        ))
        
        # Animacion
        self.add(grafico, x_label, y_label, target_line, target_label, stats)
        
        self.play(
            Create(camino),
            n_tracker.animate.set_value(intentos),
            run_time=14,
            rate_func=linear
        )
        self.wait(2)