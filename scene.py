"""

Created on Tue Oct  4 09:57:29 2022

@author: Judith Alejandra Hinojosa Rábago
"""
from manim import *

# Para correr el código "manim -qm scene.py Mapa"
class Mapa(ZoomedScene, MovingCameraScene):
# inspirado de TheoremofBeethoven
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=2,
            zoomed_display_width=6,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
                },
            **kwargs
        )

    def construct(self):
        tipLW = (0.1, 0.15) # Length,  With


        # MOSTRAR LA INTEGRAL
        integral = MathTex(
            "\\int_{-2}^{2}","\\! \\sin(-5x)",
            "\\, dx", font_size=20
        ).shift(UP * 2.5)

        self.add(integral)
        self.wait()
        

        # EMPEZAR MAPA ¿DEFINIDA O INDEFINIDA?

        ## DEFINIDA
        definida_tex = Tex('Definida', font_size=20).next_to(integral, DL, buff=0.5)
        integral_def = MathTex(
            "\\int_{a}^{b}","\\! f(x)",
            "\\, dx", font_size=20
        ).next_to(definida_tex, DOWN, buff=0)
        def_line = Line(
                start = integral.get_bottom(), end = definida_tex.get_top(), buff=0.3
            ).add_tip(tip_length=tipLW[0], tip_width=tipLW[1])

        ## INDEFINIDA
        indefinida_tex = Tex('Indefinida', font_size=20).next_to(integral, DR, buff=0.5)
        integral_indef = MathTex(
            "\\int","\\! f(x)",
            "\\, dx", font_size=20
        ).next_to(indefinida_tex, DOWN, buff=0)
        indef_line = Line(
                start = integral.get_bottom(), end = indefinida_tex.get_top(), buff=0.3
            ).add_tip(tip_length=tipLW[0], tip_width=tipLW[1])
        
        # ELEGIR DEFINIDA

        ## OBTENEMOS UN FRAME QUE PODAMOS COLOCAR APARTE DONDE SE 
        ## MUESTRE LO DEL FRAME PRINCIPAL CON ZOOM
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        ## ENFOCAMOS LA INTEGRAL
        frame.move_to(integral)
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(PURPLE)
        zoomed_display.shift(DOWN * 3)

        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)
        self.add_foreground_mobject(zd_rect)

        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))

        self.play(Create(frame))

        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)
        self.wait()

        ## AGRUPAMOS OBJETOS RELACIONADOS CON DEFINIDA
        def_int = VGroup(definida_tex, integral_def)
        
        ## DIBUJAMOS ¿DEFINIDA O INDEFINIDA?
        self.play(Create(
            VGroup(def_line, def_int)
            ),
            Create(
            VGroup(indef_line, indefinida_tex, integral_indef)
            ), run_time=2)

        ## SEÑALAMOS CON CON AMARILLO EL SÍMBOLO DE INTEGRAL QUE ESPECIFICA DE -2 A 2
        self.play(integral.animate.set_color_by_tex("-2", YELLOW))
        self.wait()


        ## ESCALA EN      x   y     z
        scale_factor = [0.75, 1.25, 0]
        ## SEÑALAMOS CON AMARILLO EL SÍMBOLO DE INTEGRAL DEFINIDA QUE VA DE a A b
        self.play(frame.animate.move_to(def_int).scale(scale_factor), 
                    zoomed_display.animate.scale(scale_factor),
                    integral_def.animate.set_color_by_tex("b", YELLOW))
        self.wait()

        ## REMOVEMOS EL ZOOM
        self.play(
            self.get_zoomed_display_pop_out_animation(), 
            unfold_camera, rate_func=lambda t: smooth(1 - t)
            )
        self.play(Uncreate(zoomed_display_frame), FadeOut(frame))
        self.wait()

        ## REMOVEMOS EL COLOR DE LA INTEGRAL Y DE LA DEFINICIÓN DE INTEGRAL DEFINIDA
        integral.set_color_by_tex("-2", WHITE)
        integral_def.set_color_by_tex("b", WHITE)

        ## CONTINUAMOS DEBAJO DE "DEFINIDA"
        # ¿ES CONTINUA?
        continua_tex = Tex('¿Es continua en [a, b]?', font_size=20).next_to(def_int, DOWN, buff=0.5)
        continua_line = Line(
                start = def_int.get_bottom(), end = continua_tex.get_top(), buff=0.3
            ).add_tip(tip_length=tipLW[0], tip_width=tipLW[1])
        
        self.play(Create(
            VGroup(continua_line, continua_tex)
            ))
        self.wait()

        ## "SÍ"
        # ENTONCES ¿VA DE -a A a?
        """
        ########## Nota ###########
        Ver como poner símbolos UTF-8 en latex para poner "¿"
        """
        s_tex = MathTex(
            "\\int_{-a}^{a}","\\! f(x)",
            "\\, dx \\! ?", font_size=20
        ).next_to(continua_tex, DOWN, buff=0.5)
        s_line = Line(
                start = continua_tex.get_bottom(), end = s_tex.get_top(), buff=0.3
            ).add_tip(tip_length=tipLW[0], tip_width=tipLW[1])
        si_tex = Tex('Sí', font_size=20).next_to(s_line, LEFT, buff=0.05)
        self.play(Create(
            VGroup(s_line, si_tex, s_tex)
            ))
        self.wait()

        ## "SÍ"
        # ENTONCES ¿f(-x) = f(x)?
        par_tex = MathTex(
            "f(-x)","=",
            "f(x) \\! ?", font_size=20
        ).next_to(s_tex, DOWN, buff=0.5)
        par_line = Line(
                start = s_tex.get_bottom(), end = par_tex.get_top(), buff=0.3
            ).add_tip(tip_length=tipLW[0], tip_width=tipLW[1])
        si1_tex = Tex('Sí', font_size=20).next_to(par_line, LEFT, buff=0.05)
        self.play(Create(
            VGroup(par_line, si1_tex, par_tex)
            ))
        self.wait()

        ## SE TRASLADA LA CÁMARA PARA QUE SE VEAN LOS ÚLTIMOS OBJETOS
        """
        ########## Nota ###########
        Ver como trasladar la función que se resuelve 
        para mantenerla siempre en el frame actual
        """
        self.play(self.camera.frame.animate.next_to(continua_tex, DOWN, buff=0))
        self.wait()

        """
        ########## Nota ###########
        Ver como conservar el frame, ir a otro dende se explique 
        como es una función par e impar y volver al mapa
        """
        
