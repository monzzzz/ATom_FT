
from manim import *
import numpy as np
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.fft import fft, fftfreq

class PresentationIntro(Scene):
    def construct(self):
        title = Text("Fourier Transform", font_size=32)
        credits = Text("Presented by Elmond, Claire, Irene, and Ella", font_size=10)

        title.move_to(UP * 4)       # start above screen
        credits.move_to(DOWN * 4) 
        
        title_target = ORIGIN + UP * 0.2
        credits_target = ORIGIN + DOWN * 0.2

        self.play(title.animate.move_to(title_target), run_time=1.5)
        self.play(credits.animate.move_to(credits_target), run_time=1.5)
        self.wait(1)
        # fade out
        self.play(FadeOut(credits))
        
        line1 = Text('"Almost every function in the world can be represented', font_size=12)
        line2 = Text('as a sum of sinusoids"', font_size=12)

        big_fourier_text = VGroup(line1, line2).arrange(DOWN, center=True, aligned_edge=ORIGIN).move_to(ORIGIN)
        
        self.play(
            Transform(title, big_fourier_text),
            run_time=1
        )
        self.wait(2)
        # clear screen
        self.play(FadeOut(title), run_time=1)

class SignalandFSIntro(Scene):
    def construct(self):
        self.wait(1)
        title = Text("Two Types of Signals", font_size=20)
        title.move_to(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        periodic_title = Text("Periodic Signals", font_size=12, color=BLUE).move_to(LEFT   + UP * 0.5)
        nonperiodic_title = Text("Non-Periodic Signals", font_size=12, color=RED).move_to(RIGHT  + UP * 0.5)
        
        self.play(Write(periodic_title), Write(nonperiodic_title))
        
        # Show periodic signal example
        periodic_axes = Axes(
            x_range=[0, 4*np.pi], y_range=[-2, 2],
            x_length=1.1, y_length=1.1,
            tips=False
        ).next_to(periodic_title, DOWN, buff=0.3)
        
        periodic_wave = periodic_axes.plot(lambda x: np.sin(x), color=BLUE)
        
        # Show non-periodic signal example  
        nonperiodic_axes = Axes(
            x_range=[0, 4*np.pi], y_range=[-2, 2],
            x_length=1.1, y_length=1.1,
            tips=False
        ).next_to(nonperiodic_title, DOWN, buff=0.3)
        
        nonperiodic_wave = nonperiodic_axes.plot(
            lambda x: np.sin(x) * np.exp(-x/4) + 0.3*np.sin(3*x), 
            color=RED
        )
        
        self.play(Create(periodic_axes), Create(nonperiodic_axes))
        self.play(Create(periodic_wave), Create(nonperiodic_wave))
        self.wait(1)
        
        self.play(
            FadeOut(periodic_axes),
            FadeOut(periodic_wave),
            FadeOut(nonperiodic_axes),
            FadeOut(nonperiodic_wave),
            run_time=1
        )
        
        
        # Fourier Series title on the left
        fourier_series_title = Text("(Fourier Series)", font_size=10, color=BLUE).next_to(periodic_title, DOWN * 0.3, buff=0.3)
        self.play(Write(fourier_series_title))
        
        
        # Fourier TRansform title on the right
        
        fourier_transform_title = Text("(Fourier Transform)", font_size=10, color=RED).next_to(nonperiodic_title, DOWN * 0.3, buff=0.3)
        self.play(Write(fourier_transform_title))
        
        # Applications for periodic signals - positioned where graph will be replaced
        periodic_apps = VGroup(
            Text("• Audio waves", font_size=10),
            Text("• AC power", font_size=10),
            Text("• Heartbeats", font_size=10)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(periodic_axes.get_center() + UP * 0.2)
        
        # Applications for non-periodic signals - positioned where graph will be replaced
        nonperiodic_apps = VGroup(
            Text("• Speech signals", font_size=10),
            Text("• Images", font_size=10),
            Text("• Transients", font_size=10)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(nonperiodic_axes.get_center() + UP * 0.2)
        
        # Fade out graphs and replace with applications
        
        self.play(Write(periodic_apps), Write(nonperiodic_apps))
        self.wait(1.5)
        
        # Highlight and zoom to Fourier Transform
        highlight_box = SurroundingRectangle(
            VGroup(periodic_title, periodic_apps, fourier_series_title),
            color=YELLOW, buff=0.2
        )
        
        self.play(Create(highlight_box))
        self.wait(0.5)
        
        # Zoom into the highlighted box and fade everything else
        everything_else = VGroup(
            title, nonperiodic_title, nonperiodic_apps, fourier_transform_title
        )

        
        # Fade out everything except Fourier Transform text
        self.play(
            FadeOut(everything_else),
            FadeOut(periodic_title),
            FadeOut(periodic_apps),
            FadeOut(highlight_box),
            FadeOut(fourier_transform_title),
            run_time=1.5
        )
        
        # Create new text without brackets for the transformation
        big_fourier_text = Text("Fourier Series", font_size=20, color=WHITE).move_to(UP)
        
        # Transform the Fourier Transform text - replace with version without brackets
        self.play(
            Transform(fourier_series_title, big_fourier_text),
            run_time=1
        )
        
        definition_text = Text("Decomposes signals into constituent frequencies", font_size=12).next_to(fourier_series_title, DOWN * 0.5, buff=0.3)
        self.play(Write(definition_text))
        self.wait(1)
        
        # Create the main signal (left graph) - combination of two frequencies
        main_axes = Axes(
            x_range=[0, 4*np.pi], y_range=[-3, 3],
            x_length=1, y_length=1,
            tips=False
        ).move_to(LEFT * 1.5 + DOWN * 0.5)
        
        # Combined signal: sin(x) + sin(3x)
        main_signal = main_axes.plot(
            lambda x: np.sin(x) + np.sin(3*x), 
            color=BLUE
        )
        
        main_title = Text("Original Signal", font_size=12).next_to(main_axes, UP, buff=0.2)
        
        # Create first frequency component (top right)
        freq1_axes = Axes(
            x_range=[0, 4*np.pi], y_range=[-2, 2],
            x_length=1, y_length=0.5,
            tips=False
        ).move_to(RIGHT)
        
        freq1_signal = freq1_axes.plot(lambda x: np.sin(x), color=RED)
        freq1_title = Text("xHz Frequency", font_size=10).next_to(freq1_axes, UP * 0.8, buff=0.1)
        
        freq2_axes = Axes(
            x_range=[0, 4*np.pi], y_range=[-2, 2],
            x_length=1, y_length=0.5,
            tips=False
        ).move_to(RIGHT + DOWN * 0.8)
        
        freq2_signal = freq2_axes.plot(lambda x: np.sin(3*x), color=GREEN)
        freq2_title = Text("yHz Frequency", font_size=10).next_to(freq2_axes, UP * 0.8, buff=0.1)
        
        arrow1 = Arrow(
            start=main_axes.get_right() + RIGHT * 0.1 ,
            end=freq1_axes.get_left() + LEFT * 0.1,
            color=YELLOW,
            stroke_width=2,
            tip_length=0.2,
            buff=0.1
        )
        
        arrow2 = Arrow(
            start=main_axes.get_right() + RIGHT * 0.1,
            end=freq2_axes.get_left() + LEFT * 0.1,
            color=YELLOW,
            stroke_width=2,
            tip_length=0.2,
            buff=0.1
        )
        
        # Animation sequence
        self.play(Create(main_axes), Write(main_title))
        self.play(Create(main_signal))
        self.wait(1)
        
        # Show the decomposition
        self.play(Create(arrow1), Create(arrow2))
        self.wait(0.5)
        
        self.play(
            Create(freq1_axes), Create(freq2_axes),
            Write(freq1_title), Write(freq2_title)
        )
        self.play(Create(freq1_signal), Create(freq2_signal))
        self.wait(2)
        # clear screen
        self.play(FadeOut(VGroup(
            main_axes, main_signal, main_title,
            arrow1, arrow2,
            freq1_axes, freq1_signal, freq1_title,
            freq2_axes, freq2_signal, freq2_title,
            definition_text
        )))  
         

class FourierSeriesMain(Scene):
    def construct(self):
        title = Text("Fourier Series", font_size=20)
        title.move_to(UP)
        self.add(title)
        
        self.wait(0.5)
        
        # Create the main signal (contains frequency 1 and 3)
        signal_axes = Axes(
            x_range=[0, 4*np.pi], y_range=[-3, 3],
            x_length=1, y_length=0.8,
            tips=False
        ).move_to(LEFT * 1.2 + DOWN * 0.2)
        
        signal = signal_axes.plot(lambda x: np.sin(x) + np.sin(3*x), color=BLUE)
        main_freq_label = Text("frequency 1 +  frequency 3", font_size=8, color=BLUE).next_to(signal_axes, UP * 0.8, buff=0.1)
        signal_label = Text("Signal: sin(x) + sin(3x)", font_size=12, color=BLUE).next_to(main_freq_label, UP * 0.8, buff=0.1)
        
        self.play(Create(signal_axes), Write(signal_label), Write(main_freq_label))
        self.play(Create(signal))
        self.wait(1)
        
        # Test with frequency that IS in the signal (frequency = 1)
       
        
        test_axes1 = Axes(
            x_range=[0, 4*np.pi], y_range=[-2, 2],
            x_length=1, y_length=0.8,
            tips=False
        ).move_to(RIGHT * 0.9 + DOWN * 0.2)
        
        test_freq_text1 = Text("Test: Multiply by sin(x) (frequency 1)", font_size=10, color=GREEN).next_to(test_axes1, UP * 0.8, buff=0.1)
        self.play(Write(test_freq_text1))
        
        # Multiply signal by sin(x) - this should give non-zero average
        multiplied_signal1 = test_axes1.plot(
            lambda x: (np.sin(x) + np.sin(3*x)) * np.sin(x), 
            color=GREEN
        )
        
        self.play(Create(test_axes1))
        self.play(Create(multiplied_signal1))
        
        # Show that average is non-zero
        avg_line1 = DashedLine(
            test_axes1.c2p(0, 0.5), 
            test_axes1.c2p(4*np.pi, 0.5), 
            color=RED
        )
        avg_text1 = Text("Average ≠ 0", font_size=8, color=RED).next_to(avg_line1, RIGHT * 0.4)

        self.play(Create(avg_line1), Write(avg_text1))
        self.wait(2)
        
        # Clear and test with frequency NOT in signal
        
        test_axes2 = Axes(
            x_range=[0, 4*np.pi], y_range=[-2, 2],
            x_length=1, y_length=0.8,
            tips=False
        ).move_to(RIGHT * 0.9 + DOWN * 0.2)
        
        test_freq_text2 = Text("Test: Multiply by sin(2x) (frequency 2)", font_size=10, color=ORANGE).next_to(test_axes2, UP * 0.8, buff=0.1)
        
        # Multiply signal by sin(2x) - this should give zero average
        multiplied_signal2 = test_axes2.plot(
            lambda x: (np.sin(x) + np.sin(3*x)) * np.sin(2*x), 
            color=ORANGE
        )
        
        # Show that average is zero
        avg_line2 = DashedLine(
            test_axes2.c2p(0, 0), 
            test_axes2.c2p(4*np.pi, 0), 
            color=RED
        )
        avg_text2 = Text("Average = 0", font_size=8, color=RED).next_to(avg_line2, RIGHT * 0.4)
        
        # Transform from 1 to 2
        self.play(
            Transform(test_axes1, test_axes2), 
            Transform(test_freq_text1, test_freq_text2), 
            Transform(multiplied_signal1, multiplied_signal2), 
            Transform(avg_line1, avg_line2), 
            Transform(avg_text1, avg_text2)
        )
        self.wait(2)
        
        test_axes3 = Axes(
            x_range=[0, 4*np.pi], y_range=[-2, 2],
            x_length=1, y_length=0.8,
            tips=False
        ).move_to(RIGHT * 0.9 + DOWN * 0.2)
        
        test_freq_text3 = Text("Test: Multiply by sin(3x) (frequency 3)", font_size=10, color=PURPLE).next_to(test_axes3, UP * 0.8, buff=0.1)
        
        # Multiply signal by sin(3x) - this should give non-zero average
        multiplied_signal3 = test_axes3.plot(
            lambda x: (np.sin(x) + np.sin(3*x)) * np.sin(3*x), 
            color=PURPLE
        )
        
        # Show that average is non-zero
        avg_line3 = DashedLine(
            test_axes3.c2p(0, 0.5), 
            test_axes3.c2p(4*np.pi, 0.5), 
            color=RED
        )
        avg_text3 = Text("Average ≠ 0", font_size=8, color=RED).next_to(avg_line3, RIGHT * 0.4)
    
        # Transform from 1 (which is now showing 2) to 3 - use the original references
        self.play(
            Transform(test_axes1, test_axes3), 
            Transform(test_freq_text1, test_freq_text3), 
            Transform(multiplied_signal1, multiplied_signal3), 
            Transform(avg_line1, avg_line3), 
            Transform(avg_text1, avg_text3)
        )
        self.wait(2)
        
        # Final explanation - use the original references since they now contain the final state
        self.play(
            FadeOut(test_freq_text1), FadeOut(test_axes1), 
            FadeOut(multiplied_signal1), FadeOut(avg_line1), FadeOut(avg_text1)
        )


        
        # Create summary table
        table_title = Text("Summary Table", font_size=12, color=YELLOW).move_to(UP * 0.5 + RIGHT * 1)
        self.play(Write(table_title))
        
        # Create table headers
        freq_header = Text("Frequency", font_size=8, color=YELLOW).move_to(RIGHT * 0.3 + UP * 0.2)
        avg_header = Text("Average", font_size=8, color=YELLOW).move_to(RIGHT * 1 + UP * 0.2)
        present_header = Text("Part of Signal?", font_size=8, color=YELLOW).move_to(RIGHT * 1.7 + UP * 0.2)
        
        # Create table rows
        freq1_row = Text("1", font_size=8, color=GREEN).move_to(RIGHT * 0.3 + DOWN * 0.1)
        avg1_row = Text("≠ 0", font_size=8, color=GREEN).move_to(RIGHT * 1 + DOWN * 0.1)
        present1_row = Text("✓ YES", font_size=8, color=GREEN).move_to(RIGHT * 1.7 + DOWN * 0.1)
        
        freq2_row = Text("2", font_size=8, color=ORANGE).move_to(RIGHT * 0.3 + DOWN * 0.4)
        avg2_row = Text("= 0", font_size=8, color=ORANGE).move_to(RIGHT * 1 + DOWN * 0.4)
        present2_row = Text("✗ NO", font_size=8, color=ORANGE).move_to(RIGHT * 1.7 + DOWN * 0.4)
        
        freq3_row = Text("3", font_size=8, color=PURPLE).move_to(RIGHT * 0.3 + DOWN * 0.7)
        avg3_row = Text("≠ 0", font_size=8, color=PURPLE).move_to(RIGHT * 1 + DOWN * 0.7)
        present3_row = Text("✓ YES", font_size=8, color=PURPLE).move_to(RIGHT * 1.7 + DOWN * 0.7)
        
        # Create table lines
        horizontal_line1 = Line(UP * 0.3, RIGHT * 2.15 + UP * 0.3, color=YELLOW, stroke_width=1)
        horizontal_line2 = Line(UP * 0.1, RIGHT * 2.15 + UP * 0.1, color=YELLOW, stroke_width=1)
        horizontal_line3 = Line(DOWN * 1.75, RIGHT * 2.15 + DOWN * 1.75, color=YELLOW, stroke_width=1)
        
        # Animate table creation
        self.play(
            Write(freq_header), Write(avg_header), Write(present_header),
            Create(horizontal_line1),
            Create(horizontal_line2)
        )
        
        self.play(
            Write(freq1_row), Write(avg1_row), Write(present1_row),
        )
        self.wait(0.5)
        
        self.play(
            Write(freq2_row), Write(avg2_row), Write(present2_row),
        )
        self.wait(0.5)
        
        self.play(
            Write(freq3_row), Write(avg3_row), Write(present3_row),
            Create(horizontal_line3)
        )
        self.wait(2)
        
        conclusion = Text("Fourier Transform detects which frequencies are present!", font_size=14, color=YELLOW).move_to(DOWN * 2.5)
        self.play(Write(conclusion))
        self.wait(2)
        
        # clean
        self.play(FadeOut(VGroup(
            signal_axes, signal, signal_label, main_freq_label,
            table_title, freq_header, avg_header, present_header,
            freq1_row, avg1_row, present1_row,
            freq2_row, avg2_row, present2_row,
            freq3_row, avg3_row, present3_row,
            horizontal_line1, horizontal_line2, horizontal_line3,
            conclusion
        )))

        # formula = MathTex(
        #     r"F(\omega) = \int_{-\infty}^{\infty} f(t)\, e^{-i\omega t}\, dt",
        #     font_size=48
        # ).shift(UP)

        # explanation = Text(
        #     "Slide a wave over the signal\nand measure similarity.",
        #     font_size=32
        # ).next_to(formula, DOWN)

        # self.play(Write(formula))
        # self.play(FadeIn(explanation))
        # self.wait()
        
class FourierSeriesMain2(Scene):
    def construct(self):
        title = Text("Fourier Series", font_size=20)
        title.move_to(UP)
        self.add(title)
        
        # Main Fourier Series equation
        fs_equation = MathTex(
            r"f(t) = a_0 + \sum_{n=1}^{\infty} \left(a_n \sin(n\omega_0 t) + b_n \cos(n\omega_0 t)\right)",
            font_size=14
        ).move_to(UP * 0.5)
        
        self.play(Write(fs_equation))
        self.wait(1)
        
        a_n_equation = MathTex(
            r"\boxed{a_n = \frac{2}{T} \int_{0}^{T} f(t)\sin(n\omega_0 t)\,dt}",
            font_size=10
        )
        
        # Sine coefficient explanation
        a_n_text1 = Text("If a_n ≠ 0 → a sine at frequency n is present.", font_size=8).next_to(a_n_equation, DOWN, buff=0.2)
        a_n_text2 = Text("If a_n = 0 → no sine component at that frequency.", font_size=8).next_to(a_n_text1, DOWN, buff=0.1)
        
        self.play(Write(a_n_equation))
        self.wait(0.5)
        self.play(Write(a_n_text1))
        self.play(Write(a_n_text2))
        self.wait(2)
        
        # Clear previous equations and texts
        self.play(
            FadeOut(a_n_equation),
            FadeOut(a_n_text1),
            FadeOut(a_n_text2),
            run_time=1
        )
        
        self.wait(1)
        
        # Cosine coefficient equation
        b_n_equation = MathTex(
            r"\boxed{b_n = \frac{2}{T} \int_{0}^{T} f(t)\cos(n\omega_0 t)\,dt}",
            font_size=10
        )
        
        # Cosine coefficient explanation
        b_n_text1 = Text("If b_n ≠ 0 → a cosine at frequency n is present.", font_size=8).next_to(b_n_equation, DOWN, buff=0.2)
        b_n_text2 = Text("If b_n = 0 → no cosine component at that frequency.", font_size=8).next_to(b_n_text1, DOWN, buff=0.1)
        
        self.play(Write(b_n_equation))
        self.wait(0.5)
        self.play(Write(b_n_text1))
        self.play(Write(b_n_text2))
        self.wait(1.5)
        
        a_group = VGroup(a_n_equation, a_n_text1, a_n_text2)
        
        b_group = VGroup(b_n_equation, b_n_text1, b_n_text2)
        
        a_group.move_to(LEFT * 4)
        self.add(a_group)
        
        self.play(
            b_group.animate.move_to(RIGHT + DOWN * 0.3).scale(0.7)
        )
        
        self.play(
            a_group.animate.move_to(LEFT + DOWN * 0.3).scale(0.7)
        )
        
        # highlight_box = SurroundingRectangle(
        #     VGroup(b_group, a_group),
        #     color=YELLOW, buff=0.2, stroke_width=2
        # )
        
        # two_calculation_text = Text("2 Calculations", font_size=10).next_to(highlight_box, DOWN, buff=0.2)
        # self.play(Create(highlight_box))
        # self.play(Write(two_calculation_text))
        self.wait(1)
        
        # clean the screen
        self.play(FadeOut(VGroup(
            title,
            fs_equation,
            a_group,
            b_group,
            # highlight_box,
            # two_calculation_text
        )))
        
        self.wait(1)
        
class FourierTransformMain(Scene):
    def construct(self):
        title = Text("Fourier Transform", font_size=20)
        title.move_to(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Fourier Transform equation
        ft_equation = MathTex(
            r"F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-2\pi i f t} \, dt",
            font_size=14
        ).move_to(UP * 0.5)
        
        self.play(Write(ft_equation))
        self.wait(1)
        
        # Explanation text
        explanation_title = Text("Why does this work?", font_size=16, color=YELLOW).move_to(DOWN * 0.3)
        self.play(Write(explanation_title))
        self.wait(0.5)
        
        self.play(FadeOut(explanation_title))
        
        # Euler's formula
        euler_formula = MathTex(
            r"e^{-2\pi i f t} = \cos(2\pi f t) - i \sin(2\pi f t)",
            font_size=10
        ).move_to(UP * 0.1)
        
        self.play(Write(euler_formula))
        self.wait(1)
        
        # Break it down
        breakdown_text = Text("This means we're testing BOTH:", font_size=10).move_to(DOWN * 0.2)
        self.play(Write(breakdown_text))
        self.wait(0.5)
        
        # Cosine component
        cosine_component = MathTex(
            r"\text{Cosine: } \int_{-\infty}^{\infty} f(t) \cos(2\pi f t) \, dt",
            font_size=10,
            color=BLUE
        ).move_to(DOWN * 0.5)
        
        # Sine component
        sine_component = MathTex(
            r"\text{Sine: } \int_{-\infty}^{\infty} f(t) \sin(2\pi f t) \, dt",
            font_size=10,
            color=RED
        ).move_to(DOWN * 0.8)
        
        self.play(Write(cosine_component))
        self.wait(0.5)
        self.play(Write(sine_component))
        self.wait(1)
        
        # Final explanation
        final_explanation = VGroup(
            Text("The complex exponential e^(-2πift) combines both", font_size=12),
            Text("cosine and sine tests in one elegant formula!", font_size=12, color=GREEN)
        ).arrange(DOWN, buff=0.1).move_to(DOWN * 2)
        
        self.play(Write(final_explanation))
        self.wait(2)
        
        

        # formula = MathTex(
        #     r"F(\omega) = \int_{-\infty}^{\infty} f(t)\, e^{-i\omega t}\, dt",
        #     font_size=48
        # ).shift(UP)

        # explanation = Text(
        #     "Slide a wave over the signal\nand measure similarity.",
        #     font_size=32
        # ).next_to(formula, DOWN)

        # self.play(Write(formula))
        # self.play(FadeIn(explanation))
        # self.wait()
        
# image processing
# audio processing
# communications
# (optional) vibration and machanical analysis

class FFTApplications(Scene):
    def construct(self):
        title = Text("Applications of Fourier Transform", font_size=20)
        title.move_to(ORIGIN)       # start above screen
        self.play(Write(title))
        
        self.play(title.animate.move_to(UP), run_time=1.5)
        
        audio_title = Text("Audio Processing", font_size=10)
        audio_image = ImageMobject("./images/audio.png").scale(0.15)
        image_title = Text("Image Processing", font_size=10)
        image_image = ImageMobject("./images/image.png").scale(0.25)
        vibration_title = Text("Vibration Analysis", font_size=10)
        vibration_image = ImageMobject("./images/vibration.png").scale(0.08)
        audio_title.move_to(ORIGIN + LEFT * 1.5 + UP * 0.35)
        audio_image.next_to(audio_title, DOWN)
        self.play(Write(audio_title), FadeIn(audio_image))
        self.wait()
        image_title.move_to(ORIGIN + UP * 0.35)
        image_image.next_to(image_title, DOWN)
        self.play(Write(image_title), FadeIn(image_image))
        self.wait()
        vibration_title.move_to(ORIGIN + RIGHT * 1.5 + UP * 0.35)
        vibration_image.next_to(vibration_title, DOWN)  
        self.play(Write(vibration_title), FadeIn(vibration_image))
        self.wait()
        
        self.play(FadeOut(Group(  # Changed from VGroup to Group
            title,
            audio_image,
            image_title, image_image,
            vibration_title, vibration_image
        )))
        
        self.play(audio_title.animate.move_to(UP).scale(2))
        self.wait(1)
        
        # Load and analyze school_song.wav
        
        
        try:
            # Load the audio file
            sample_rate, audio_data = wavfile.read("school_song.wav")
            
            # If stereo, convert to mono by taking the mean
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # Normalize the audio data
            audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Take a segment for analysis (first 4 seconds or full length if shorter)
            segment_length = min(3 * sample_rate, len(audio_data))
            audio_segment = audio_data[:segment_length]
            
            # Time axis for plotting
            time_axis = np.linspace(0, len(audio_segment) / sample_rate, len(audio_segment))
            
        except FileNotFoundError:
            # Create a synthetic audio signal if file not found
            sample_rate = 44100
            duration = 4  # 4 seconds
            time_axis = np.linspace(0, duration, sample_rate * duration)
            
            # Create a melody with C-D-E-F-G-A-B notes
            note_frequencies = {
                'C': 261.63, 'D': 293.66, 'E': 329.63, 'F': 349.23,
                'G': 392.00, 'A': 440.00, 'B': 493.88
            }
            
            audio_segment = np.zeros(len(time_axis))
            note_duration = duration / 7  # Each note plays for duration/7 seconds
            
            for i, (note, freq) in enumerate(note_frequencies.items()):
                start_idx = int(i * note_duration * sample_rate)
                end_idx = int((i + 1) * note_duration * sample_rate)
                if end_idx > len(audio_segment):
                    end_idx = len(audio_segment)
                
                t_note = time_axis[start_idx:end_idx] - time_axis[start_idx]
                audio_segment[start_idx:end_idx] = 0.5 * np.sin(2 * np.pi * freq * t_note)
        
        # Create time domain plot
        time_axes = Axes(
            x_range=[0, 4], y_range=[-1, 1],
            x_length=3, y_length=1.2,
            tips=False
        )
        
        time_label = Text("Audio Waveform", font_size=10).next_to(time_axes, UP, buff=0.1)
        time_x_label = Text("Time (s)", font_size=8).next_to(time_axes, DOWN, buff=0.1)
        time_y_label = Text("Amp", font_size=8).next_to(time_axes, LEFT, buff=0.1)
        
        # Sample the audio data for plotting (take every nth sample to reduce points)
        downsample_factor = max(1, len(audio_segment) // 1000)  # Max 1000 points for performance
        time_sampled = time_axis[::downsample_factor]
        audio_sampled = audio_segment[::downsample_factor]
        
        # Create the waveform plot
        waveform_points = [time_axes.c2p(t, amp) for t, amp in zip(time_sampled, audio_sampled) if t <= 4]
        waveform = VMobject()
        waveform.set_points_as_corners(waveform_points)
        waveform.set_color(BLUE)
        
        self.play(Create(time_axes), Write(time_label), Write(time_x_label), Write(time_y_label))
        
        # Add audio playback for 3 seconds (matching the graph duration)  
        self.add_sound("school_song.wav", time_offset=0, gain=1.0)
        
        # Create waveform with 3-second duration to match audio
        self.play(Create(waveform), run_time=3)
        self.wait(0.5)  # Short pause after audio ends
        
        # Perform FFT
        fft_data = fft(audio_segment)
        frequencies = fftfreq(len(audio_segment), 1/sample_rate)
        
        # Take only positive frequencies up to 1000 Hz (musical range)
        positive_freq_mask = (frequencies >= 0) & (frequencies <= 1000)
        freq_positive = frequencies[positive_freq_mask]
        magnitude_positive = np.abs(fft_data[positive_freq_mask])
        
        # Create frequency domain plot
        freq_axes = Axes(
            x_range=[0, 1000, 100], y_range=[0, np.max(magnitude_positive) * 1.1 if np.max(magnitude_positive) > 0 else 1, 100],
            x_length=3, y_length=1.2,
            tips=False
        )
        
        freq_label = Text("Frequency Spectrum", font_size=10).next_to(freq_axes, UP, buff=0.1)
        freq_x_label = Text("Frequency (Hz)", font_size=8).next_to(freq_axes, DOWN, buff=0.1)
        freq_y_label = Text("Mag", font_size=8).next_to(freq_axes, LEFT, buff=0.1)
        
        # Sample frequency data for plotting
        freq_downsample = max(1, len(freq_positive) // 500)
        freq_sampled = freq_positive[::freq_downsample]
        mag_sampled = magnitude_positive[::freq_downsample]
        
        # Normalize magnitude for plotting
        if np.max(mag_sampled) > 0:
            mag_normalized = mag_sampled / np.max(mag_sampled) * np.max(magnitude_positive) * 1.1
        else:
            mag_normalized = mag_sampled
        
        spectrum_points = [freq_axes.c2p(f, m) for f, m in zip(freq_sampled, mag_normalized)]
        spectrum = VMobject()
        spectrum.set_points_as_corners(spectrum_points)
        spectrum.set_color(ORANGE)  # Changed to ORANGE as requested
        
        # Transform the blue waveform into the orange frequency spectrum
        self.play(
            Transform(time_axes, freq_axes),
            Transform(time_label, freq_label), 
            Transform(time_x_label, freq_x_label),
            Transform(time_y_label, freq_y_label),
            Transform(waveform, spectrum),
            run_time=2
        )
        self.wait(1)
        
        # Identify and highlight musical notes (multiple octaves)
        musical_notes = {
            'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
            'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
            'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
            'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
            'C6': 1046.50, 'D6': 1174.66, 'E6': 1318.51, 'F6': 1396.91,
            'G6': 1567.98, 'A6': 1760.00, 'B6': 1975.53
        }
        
        note_markers = VGroup()
        detected_notes = []
        
        for note, target_freq in musical_notes.items():
            # Find peaks near the target frequency (±10 Hz tolerance)
            freq_mask = (freq_positive >= target_freq - 10) & (freq_positive <= target_freq + 10)
            if np.any(freq_mask):
                peak_magnitude = np.max(magnitude_positive[freq_mask])
                if peak_magnitude > np.max(magnitude_positive) * 0.1:  # Only significant peaks
                    detected_notes.append(note)
                    
                    # Create marker line
                    marker = Line(
                        freq_axes.c2p(target_freq, 0),
                        freq_axes.c2p(target_freq, peak_magnitude),
                        color=BLUE,
                        stroke_width=3
                    )
                    note_text = Text(note, font_size=8, color=BLUE, weight=BOLD).next_to(marker, UP, buff=0.05)
                    note_markers.add(marker, note_text)
        
        if len(note_markers) > 0:
            self.play(Create(note_markers))
            
            # Show detected notes summary
            detected_text = Text(f"Notes: {', '.join(detected_notes)}", 
                               font_size=10, color=BLUE, weight=BOLD).move_to(DOWN * 2.5)
            self.play(Write(detected_text))
            
            noise_threshold = np.max(magnitude_positive) * 0.15  # 15% threshold
            
           
            musical_mask = np.zeros_like(freq_positive, dtype=bool)
            for note, target_freq in musical_notes.items():
                freq_tolerance = 15  # Hz
                note_mask = (freq_positive >= target_freq - freq_tolerance) & (freq_positive <= target_freq + freq_tolerance)
                musical_mask |= note_mask
            
            # Filter spectrum: keep musical notes + high amplitude frequencies
            filtered_magnitude = magnitude_positive.copy()
            noise_mask = (magnitude_positive < noise_threshold) & ~musical_mask
            filtered_magnitude[noise_mask] = 0
            
            # Create filtered spectrum plot
            filtered_mag_sampled = filtered_magnitude[::freq_downsample]
            if np.max(filtered_mag_sampled) > 0:
                filtered_mag_normalized = filtered_mag_sampled / np.max(filtered_mag_sampled) * np.max(magnitude_positive) * 1.1
            else:
                filtered_mag_normalized = filtered_mag_sampled
                
            filtered_spectrum_points = [freq_axes.c2p(f, m) for f, m in zip(freq_sampled, filtered_mag_normalized)]
            filtered_spectrum = VMobject()
            filtered_spectrum.set_points_as_corners(filtered_spectrum_points)
            filtered_spectrum.set_color(GREEN)  # Green for cleaned spectrum
            
            # Add noise filtering label
            
            # Transform orange spectrum to green filtered spectrum
            # First remove the note markers and detected text
            self.play(FadeOut(note_markers), FadeOut(detected_text))
            
            # Transform spectrum and replace the label completely
            self.play(
                Transform(spectrum, filtered_spectrum),
                run_time=1.5
            )
            
            # Show filtering statistics
            total_freq_points = len(magnitude_positive)
            noise_points_removed = np.sum(noise_mask)
            noise_reduction_percent = (noise_points_removed / total_freq_points) * 100
            
            stats_text = Text(f"Noise Reduction: {noise_reduction_percent:.1f}% of frequencies removed", 
                            font_size=8, color=GREEN).move_to(DOWN * 3)
            self.play(Write(stats_text))
            self.wait(2)
            
        else:
            no_notes_text = Text("No clear notes detected", 
                                font_size=10, color=ORANGE).move_to(DOWN * 2.5)
            self.play(Write(no_notes_text))
            self.wait(2)
        
        # Fade out everything on screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

        # img = ImageMobject("example_image.png").scale(1.2)
        # img_fft = ImageMobject("example_image_fft.png").scale(1.2)
        # img_filtered = ImageMobject("example_image_filtered.png").scale(1.2)

        # group = VGroup(img, img_fft, img_filtered).arrange(RIGHT, buff=1)

        # self.play(FadeIn(img))
        # self.play(FadeIn(img_fft))
        # self.play(FadeIn(img_filtered))
        # self.wait()

        # labels = VGroup(
        #     Text("Original"),
        #     Text("FFT Spectrum"),
        #     Text("Filtered Image")
        # ).arrange(RIGHT, buff=1).next_to(group, DOWN)

        # self.play(FadeIn(labels))
        # self.wait()
<<<<<<< HEAD
        
class FFTApplications2(Scene):
=======

class FFTExplanation(Scene):
    def construct(self):
        title = Text("DFT vs FFT", font_size=48).to_edge(UP)
        self.play(Write(title))

        slow = MathTex("O(N^2)", font_size=60, color=RED).shift(LEFT*3)
        fast = MathTex("O(N \\log N)", font_size=60, color=GREEN).shift(RIGHT*3)

        arrow = Arrow(slow, fast)

        self.play(Write(slow))
        self.play(Create(arrow))
        self.play(Write(fast))
        self.wait()

        msg = Text("FFT enables Wi-Fi, JPEG, MP3, MRI, and more.", font_size=28).to_edge(DOWN)
        self.play(FadeIn(msg))
        self.wait()

class CircleFTVisualization(Scene):
>>>>>>> e9b2444 (Added CircleFTVisualization scene and updated FullPresentation)
    def construct(self):
        # Mr. Geddes' Photo - Fourier Transform Demonstration
        title = Text("Image Processing", font_size=16)
        title.move_to(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Display the original Mr. Geddes image
        geddes_image = ImageMobject("images/mrgeddes.png").scale(0.2)
        geddes_image.move_to(ORIGIN)

        highpass_image = ImageMobject("images/fft_output/highpass.png").scale(0.1)
        highpass_image.move_to(LEFT * 1.5 + DOWN * 0.1)
        
        lowpass_image = ImageMobject("images/fft_output/lowpass.png").scale(0.1)
        lowpass_image.move_to(RIGHT * 1.5+ UP * 0.3)
        
        notch_image = ImageMobject("images/fft_output/notch_removed_texture.png").scale(0.1)
        notch_image.move_to(RIGHT * 1.7 + DOWN * 0.5)

        self.play(FadeIn(geddes_image))
        self.wait(1)

        self.play(FadeIn(highpass_image))
        self.play(FadeIn(lowpass_image))
        self.play(FadeIn(notch_image))
        self.wait(2)
        
from manim import *

class FullPresentation(Scene):
    def construct(self):
<<<<<<< HEAD
        title = Text("Thank you for listening", font_size=16)
        title.move_to(ORIGIN)
        self.play(Write(title))
        self.wait(1)
=======
        for SceneClass in [
            PresentationIntro,
            SignalIntro,
            FourierSeriesScene,
            FourierTransformDefinition,
            CircleFTVisualization,
            FFTExplanation,
            FFTApplications,
            SpectrogramScene,
        ]:
            self.play(FadeOut(VGroup(*self.mobjects)))
            scene = SceneClass()
            scene.construct()
>>>>>>> e9b2444 (Added CircleFTVisualization scene and updated FullPresentation)
