import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import one_dot__with_visualization, one_dot_visualize_midpoint
from threading import Event
from model import Drum_with_podlozkda, Mishen


global exit_flag
exit_flag = Event()


def disable_buttons_for_frame(frame: tk.Frame):
    for child in frame.winfo_children():
        child.configure(state='disable')


def disable_buttons_for_frames(frames):
    for frame in frames:
        disable_buttons_for_frame(frame)


def enable_buttons_for_frame(frame: tk.Frame):
    for child in frame.winfo_children():
        child.configure(state='normal')


def enable_buttons_for_frames(frames):
    for frame in frames:
        enable_buttons_for_frame(frame)


def start(
    fig, ax1, ax2, rad_b, rpm_b, psi, rad_o, rpm_o, ksi, m_width, m_height, m_distance, k, nx, ny, time_step, time
)
    # print(fig, ax1, ax2, rad_b, rpm_b, psi, rad_o, rpm_o, ksi, m_width, m_height, m_distance, k, nx, ny, time_step, time)
    exit_flag.clear()
    # exit()
    drum = Drum_with_podlozkda(rad=rad_b, rpm=rpm_b, holders_rad=rad_o, holders_rpm=rpm_o)
    mishen = Mishen(m_distance, -m_height / 2, m_height / 2, -m_width / 2, m_width / 2)
    drum.make_custom_holder(holder_angle=psi, point_angle=ksi)
    one_dot_visualize_midpoint(
        fig, ax1, ax2, exit_flag, nx=nx, ny=ny, cond_enabled=True, drum_with_podlozkda=drum, mishen=mishen, k=k, time_step=time_step,
    )

def stop():
    exit_flag.set()


if __name__ == "__main__":
    # This defines the Python GUI backend to use for matplotlib
    matplotlib.use('TkAgg')

    # Initialize an instance of Tk
    root = tk.Tk()
    graphFrame = tk.Frame(root, bg="blue")

    # Initialize matplotlib figure for graphing purposes
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.set_title("")

    # Special type of "canvas" to allow for matplotlib graphing
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()

    # Add the plot to the tkinter widget
    plot_widget.grid(row=0, column=1, sticky="nsew")
    # Create a tkinter button at the bottom of the window and link it with the updateGraph function
    root.title("Моделирование нанесения наноструктур в магнетроннах барабанного вида")
    root.geometry('{}x{}'.format(460, 710))
    root.minsize(width=460, height=600)
    # top_frame = tk.Frame(root, bg='cyan', width=450, height=50, pady=3)
    # center = tk.Frame(root, bg='gray2', width=50, height=40, padx=3, pady=3)
    # btm_frame = tk.Frame(root, bg='white', width=450, height=45, pady=3)
    # btm_frame2 = tk.Frame(root, bg='lavender', width=450, height=60, pady=3)

    paramsFrame = tk.Frame(root, bg="green")
    # root.grid_rowconfigure(0, weight=1)
    # root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=0)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(1, weight=1)

    paramsFrame.grid(row=0, column=0, sticky="nsew")
    # graphFrame.grid(row=0, column=1, sticky="nsew")
    labelframeBar = tk.LabelFrame(paramsFrame, text="Параметры барабана")
    labelframeObr = tk.LabelFrame(paramsFrame, text="Параметры образца")
    labelframeMish = tk.LabelFrame(paramsFrame, text="Параметры мишени")
    labelframeSred = tk.LabelFrame(paramsFrame, text="Параметры среды")
    labelframeMM = tk.LabelFrame(paramsFrame, text="Параметры мат. модели")
    frameSS = tk.Frame(paramsFrame)

    labelframeBar.pack(fill=tk.BOTH, expand=True)
    labelframeObr.pack(fill=tk.BOTH, expand=True)
    labelframeMish.pack(fill=tk.BOTH, expand=True)
    labelframeSred.pack(fill=tk.BOTH, expand=True)
    labelframeMM.pack(fill=tk.BOTH, expand=True)
    frameSS.pack(fill=tk.BOTH, expand=True)
    framesToDisable = [labelframeBar, labelframeMish, labelframeMM, labelframeObr, labelframeSred]

    # inside labelframeBar
    labelTextBarRad = tk.StringVar()
    labelTextBarRad.set("Радиус")
    labelBarRad = tk.Label(labelframeBar, textvariable=labelTextBarRad, height=1)
    labelBarRad.pack(side="top", anchor="nw", expand=True)

    entryTextBarRad = tk.DoubleVar()
    entryTextBarRad.set(10.0)
    entryBarRad = tk.Entry(labelframeBar, text=entryTextBarRad)
    entryBarRad.pack(side="top", anchor="nw", expand=True)

    labelTextBarRpm = tk.StringVar()
    labelTextBarRpm.set("Частота вращения")
    labelBarRpm = tk.Label(labelframeBar, textvariable=labelTextBarRpm, height=1)
    labelBarRpm.pack(side="top", anchor="nw", expand=True)

    entryTextBarRpm = tk.DoubleVar()
    entryTextBarRpm.set(1.0)
    entryBarRpm = tk.Entry(labelframeBar, text=entryTextBarRpm)
    entryBarRpm.pack(side="top", anchor="nw", expand=True)

    labelTextBarPsi = tk.StringVar()
    labelTextBarPsi.set("Начальный угол образца")
    labelBarPsi = tk.Label(labelframeBar, textvariable=labelTextBarPsi, height=1)
    labelBarPsi.pack(side="top", anchor="nw", expand=True)

    entryTextBarPsi = tk.DoubleVar()
    entryTextBarPsi.set(0)
    entryBarPsi = tk.Entry(labelframeBar, text=entryTextBarPsi)
    entryBarPsi.pack(side="top", anchor="nw", expand=True)

    # inside labelframeObr
    labelTextObrRad = tk.StringVar()
    labelTextObrRad.set("Радиус")
    labelObrRad = tk.Label(labelframeObr, textvariable=labelTextObrRad, height=1)
    labelObrRad.pack(side="top", anchor="nw", expand=True)

    entryTextObrRad = tk.DoubleVar()
    entryTextObrRad.set(1.0)
    entryObrRad = tk.Entry(labelframeObr, text=entryTextObrRad)
    entryObrRad.pack(side="top", anchor="nw", expand=True)

    labelTextObrRpm = tk.StringVar()
    labelTextObrRpm.set("Частота вращения")
    entryObrRpm = tk.Label(labelframeObr, textvariable=labelTextObrRpm, height=1)
    entryObrRpm.pack(side="top", anchor="nw", expand=True)

    entryTextObrRpm = tk.DoubleVar()
    entryTextObrRpm.set(1.0)
    entryObrRpm = tk.Entry(labelframeObr, text=entryTextObrRpm)
    entryObrRpm.pack(side="top", anchor="nw", expand=True)

    labelTextObrPsi = tk.StringVar()
    labelTextObrPsi.set("Начальный угол образца")
    labelObrPsi = tk.Label(labelframeObr, textvariable=labelTextObrPsi, height=1)
    labelObrPsi.pack(side="top", anchor="nw", expand=True)

    entryTextObrPsi = tk.DoubleVar()
    entryTextObrPsi.set(0)
    entryObrPsi = tk.Entry(labelframeObr, text=entryTextObrPsi)
    entryObrPsi.pack(side="top", anchor="nw", expand=True)

    # inside labelframeMish
    labelTextMishDist = tk.StringVar()
    labelTextMishDist.set("Расстояние от центра барабана")
    labelMishDist = tk.Label(labelframeMish, textvariable=labelTextMishDist, height=1)
    labelMishDist.pack(side="top", anchor="nw", expand=True)

    entryTextMishDist = tk.DoubleVar()
    entryTextMishDist.set(30.0)
    entryMishDist = tk.Entry(labelframeMish, text=entryTextMishDist)
    entryMishDist.pack(side="top", anchor="nw", expand=True)

    labelTextMishWidth = tk.StringVar()
    labelTextMishWidth.set("Ширина")
    labelMishWidth = tk.Label(labelframeMish, textvariable=labelTextMishWidth, height=1)
    labelMishWidth.pack(side="top", anchor="nw", expand=True)

    entryTextMishWidth = tk.DoubleVar()
    entryTextMishWidth.set(11.5)
    entryMishWidth = tk.Entry(labelframeMish, text=entryTextMishWidth)
    entryMishWidth.pack(side="top", anchor="nw", expand=True)

    labelTextMishHeight = tk.StringVar()
    labelTextMishHeight.set("Высота")
    labelMishHeight = tk.Label(labelframeMish, textvariable=labelTextMishHeight, height=1)
    labelMishHeight.pack(side="top", anchor="nw", expand=True)

    entryTextMishHeight = tk.DoubleVar()
    entryTextMishHeight.set(25.5)
    entryMishHeight = tk.Entry(labelframeMish, text=entryTextMishHeight)
    entryMishHeight.pack(side="top", anchor="nw", expand=True)

    # inside labelframeSred
    labelTextSredK = tk.StringVar()
    labelTextSredK.set("Коэффициент затенения")
    labelSredK = tk.Label(labelframeSred, textvariable=labelTextSredK, height=1)
    labelSredK.pack(side="top", anchor="nw", expand=True)

    entryTextSredK = tk.DoubleVar()
    entryTextSredK.set(0)
    entrySredK = tk.Entry(labelframeSred, text=entryTextSredK)
    entrySredK.pack(side="top", anchor="nw", expand=True)

    # inside labelframeMM
    labelTextMMDT = tk.StringVar()
    labelTextMMDT.set("dt")
    labelMMDT = tk.Label(labelframeMM, textvariable=labelTextMMDT, height=1)
    labelMMDT.pack(side="top", anchor="nw", expand=True)

    entryTextMMDT = tk.DoubleVar()
    entryTextMMDT.set(0.15)
    entryMMDT = tk.Entry(labelframeMM, text=entryTextMMDT)
    entryMMDT.pack(side="top", anchor="nw", expand=True)

    labelTextMMHX = tk.StringVar()
    labelTextMMHX.set("nx")
    labelMMHX = tk.Label(labelframeMM, textvariable=labelTextMMHX, height=1)
    labelMMHX.pack(side="top", anchor="nw", expand=True)

    entryTextMMHX = tk.IntVar()
    entryTextMMHX.set(100)
    entryMMHX = tk.Entry(labelframeMM, text=entryTextMMHX)
    entryMMHX.pack(side="top", anchor="nw", expand=True)

    labelTextMMHY = tk.StringVar()
    labelTextMMHY.set("ny")
    labelMMHY = tk.Label(labelframeMM, textvariable=labelTextMMHY, height=1)
    labelMMHY.pack(side="top", anchor="nw", expand=True)

    entryTextMMHY = tk.IntVar()
    entryTextMMHY.set(100)
    entryMMHY = tk.Entry(labelframeMM, text=entryTextMMHY)
    entryMMHY.pack(side="top", anchor="nw", expand=True)

    tk.Button(
        frameSS,
        text="Старт",
        command=lambda: start(
            fig,
            ax1,
            ax2,
            entryTextBarRad.get(),
            entryTextBarRpm.get(),
            entryTextBarPsi.get(),
            entryTextObrRad.get(),
            entryTextObrRpm.get(),
            entryTextObrPsi.get(),
            entryTextMishWidth.get(),
            entryTextMishHeight.get(),
            entryTextMishDist.get(),
            entryTextSredK.get(),
            entryTextMMHX.get(),
            entryTextMMHY.get(),
            entryTextMMDT.get(),
            1
        ),
    ).grid(row=0, column=0)
    tk.Button(frameSS, text="Стоп", command=lambda: stop()).grid(row=0, column=1)

    root.mainloop()
