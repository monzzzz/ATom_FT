from manim import *
import numpy as np

class PresentationIntro(Scene):
    def construct(self):
        title = Text("Fourier Transforms", font_size=32, weight=BOLD)
        credits = Text("presented by Elmond, Claire, Irene, and Ella", font_size=10)

        title.move_to(UP * 4)       # start above screen
        credits.move_to(DOWN * 4) 
        
        title_target = ORIGIN + UP * 0.2
        credits_target = ORIGIN + DOWN * 0.2

        self.play(title.animate.move_to(title_target), run_time=1.5)
        self.play(credits.animate.move_to(credits_target), run_time=1.5)
        self.wait(1)
        # fade out
        self.play(FadeOut(title), FadeOut(credits))
        self.wait(1)

class SignalIntro(Scene):
    def construct(self):
        
        title = Text("Signals as Functions", font_size=24).to_edge(UP)

        axes = Axes(
            x_range=[0, 10],
            y_range=[-10, 10],
            tips=False
        ).to_edge(DOWN)

        t = np.linspace(0, 10, 600)
        sine_wave = np.sin(t)

        sine_graph = axes.plot(lambda x: np.sin(x), color=BLUE)

        label = Text("f(t) in time-domain", font_size=32).next_to(axes, UP)

        self.play(Write(title))
        self.play(Create(axes), FadeIn(label))
        self.play(Create(sine_graph), run_time=3)
        self.wait()

        # Explain frequency domain
        freq_title = Text("Frequency Domain", font_size=40)
        freq_graph = axes.plot(lambda x: np.sin(10*x), color=RED)

        self.play(Transform(title, freq_title),
                  Transform(sine_graph, freq_graph),
                  FadeOut(label))
        self.wait()


class FourierSeriesScene(Scene):
    def construct(self):
        title = Text("Fourier Series Decomposition", font_size=48).to_edge(UP)

        axes = Axes(
            x_range=[0, 2*np.pi],
            y_range=[-10, 10],
            tips=False
        )

        square_wave = axes.plot(
            lambda x: np.sign(np.sin(x)), color=YELLOW
        )

        series_terms = VGroup()
        partial_sum = lambda x, N: sum([
            (1/(2*k+1)) * np.sin((2*k+1)*x) for k in range(N)
        ])

        self.play(Write(title))
        self.play(Create(axes))
        self.wait()

        # show adding terms one by one
        for N, color in zip([1, 3, 5, 20], [BLUE, GREEN, ORANGE, RED]):
            graph = axes.plot(lambda x, N=N: partial_sum(x, N), color=color)
            term_text = Text(f"{N} sine waves", font_size=28).next_to(axes, DOWN)

            self.play(Create(graph), FadeIn(term_text))
            self.wait()
            self.play(FadeOut(graph), FadeOut(term_text))

        # Final square wave approximation
        final = axes.plot(lambda x: partial_sum(x, 50), color=RED)
        self.play(Create(final))
        self.play(FadeIn(square_wave))
        self.wait()

class FourierTransformDefinition(Scene):
    def construct(self):
        title = Text("Fourier Transform", font_size=48).to_edge(UP)
        self.play(Write(title))

        formula = MathTex(
            r"F(\omega) = \int_{-\infty}^{\infty} f(t)\, e^{-i\omega t}\, dt",
            font_size=48
        ).shift(UP)

        explanation = Text(
            "Slide a wave over the signal\nand measure similarity.",
            font_size=32
        ).next_to(formula, DOWN)

        self.play(Write(formula))
        self.play(FadeIn(explanation))
        self.wait()


class SpectrogramScene(Scene):
    def construct(self):
        title = Text("Spectrogram Visualization", font_size=48).to_edge(UP)
        self.play(Write(title))

        # Simulated changing-frequency signal
        axes = Axes(x_range=[0, 10], y_range=[-2, 2], tips=False)
        graph = axes.plot(lambda t: np.sin(2*t) + 0.5*np.sin(10*t), color=BLUE)

        self.play(Create(axes), Create(graph))

        window = Rectangle(color=YELLOW, width=1.0, height=4).move_to(axes.c2p(0,0))
        self.play(Create(window))

        # Animate sliding window
        self.play(window.animate.move_to(axes.c2p(8,0)), run_time=5, rate_func=linear)

        self.wait()
        
# image processing
# audio processing
# communications
# (optional) vibration and machanical analysis

class FFTApplications(Scene):
    def construct(self):
        title = Text("Applications of Fourier Transform", font_size=48).to_edge(UP)
        self.play(Write(title))

        img = ImageMobject("example_image.png").scale(1.2)
        img_fft = ImageMobject("example_image_fft.png").scale(1.2)
        img_filtered = ImageMobject("example_image_filtered.png").scale(1.2)

        group = VGroup(img, img_fft, img_filtered).arrange(RIGHT, buff=1)

        self.play(FadeIn(img))
        self.play(FadeIn(img_fft))
        self.play(FadeIn(img_filtered))
        self.wait()

        labels = VGroup(
            Text("Original"),
            Text("FFT Spectrum"),
            Text("Filtered Image")
        ).arrange(RIGHT, buff=1).next_to(group, DOWN)

        self.play(FadeIn(labels))
        self.wait()

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