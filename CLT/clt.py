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
        card_images = self.cargar()
        
        n_samples = 5   
        n_cartas = 10
        for iteration in range(n_samples):
            # seleccion valores de cartas
            valores = [random.randint(1, 10) for _ in range(n_cartas)]
            sum_mano = sum(valores)
            
            mano_completa = Group() 

            for i in valores:
                mano_completa.add(card_images[i].copy())

            # 3. Let Manim handle the rows and columns automatically
            # buff=(x, y) controls horizontal vs vertical spacing
            mano_completa.arrange_in_grid(rows=2, cols=5, buff=(0.05, 0.5))
                
            self.play(
                LaggedStart(
                    *[FadeIn(c, shift=UP*0.5) for c in mano_completa],
                    lag_ratio=0.15
                ),
                run_time=1
            )
            
            # Display Sum
            sum_text = Text(f"Sum: {sum_mano}", font_size=48, color=GRAY_B)
            sum_text.next_to(mano_completa, DOWN, buff=0.8)
            
            self.play(Write(sum_text))
            self.wait(1)
            
            # 5. Cleanup
            # Fade out everything except title to prepare for next loop
            if iteration < n_samples - 1:
                self.play(
                    FadeOut(mano_completa, shift=DOWN*0.5),
                    FadeOut(sum_text)
                )
            else:
                # Final cleanup
                self.play(
                    FadeOut(mano_completa),
                    FadeOut(sum_text),
                )

if __name__ == "__main__":
    clt = CLT()
    clt.construct()