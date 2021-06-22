import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import one_dot__with_visualization, one_dot_visualize_midpoint
from threading import Event
from model import Drum_with_podlozkda, Mishen
from tkinter import messagebox
from decimal import Decimal
import logging
import sys

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
    fig,
    ax1,
    ax2,
    rad_b,
    rpm_b,
    psi,
    rad_o,
    rpm_o,
    ksi,
    m_width,
    m_height,
    m_distance,
    k,
    nx,
    ny,
    time_step,
    time,
    frames,
    d_field,
    ct_field,
    enabled_sh,
    rad_sh,
    height_sh
):

    if not (0 <= rad_b <= 99):
        messagebox.showerror("Ошибка", "Введено недопустимое значение радиуса барабана. Допустимые значения:0-99")
        return
    elif not(0 <= rad_o <= 99):
        messagebox.showerror("Ошибка", "Введено недопустимое значение радиуса образца. Допустимые значения:0-99")
        return
    elif not(rad_o + rad_b < m_distance):
        messagebox.showerror("Ошибка", "Введено недопустимое значение радиуса барабана. Радиус образца и радиус барабана в сумме не должны превышать расстояние до мишени")
        return
    elif not(rad_o < rad_b):
        messagebox.showerror("Ошибка", "Введено недопустимое значение. Радиус образца должен быть меньше радиуса барабана")
        return
    elif not(0 < m_height <= 100):
        messagebox.showerror("Ошибка", "Введено недопустимое значение высоты мишени. Допустимые значения: (0,100]")
        return
    elif not(0 < m_width <= 100):
        messagebox.showerror("Ошибка", "Введено недопустимое значение ширины. Допустимые значения: (0,100]")
        return
    elif not(0 < m_distance <= 400):
        messagebox.showerror("Ошибка", "Введено недопустимое значение расстояния от центра барабана до мишени. Допустимые значения:(0,100]")
        return
    elif not(-360 <= psi <= 360):
        messagebox.showerror("Ошибка", "Введено недопустимое значение начального угла образца. Допустимое значение от -360 до 360")
        return
    elif not(-360 <= ksi <= 360):
        messagebox.showerror("Ошибка", "Введено недопустимое значение начального угла рассматриваемой точки. Допустимое значение от -360 до 360")
        return
    elif not(0 < nx <= 65536):
        messagebox.showerror("Ошибка", "Введено недопустимое значение количества узлов интегрирования. Допустимые значения:1-65536")
        return
    elif not(0 < ny <= 65536):
        messagebox.showerror("Ошибка", "Введено недопустимое значение количества узлов интегрирования. Допустимые значения:1-65536")
        return
    elif not(0 <= k <= 1):
        messagebox.showerror("Ошибка", "Введено недопустимое значение степени затенения. Допустимые значения:0-1")
        return
    elif not(time_step > 0):
        messagebox.showerror("Ошибка", "Введено недопустимое значение шага по времени. Допустимые значения: >0")
        return
    elif not(time > 0):
        messagebox.showerror("Ошибка", "Введено недопустимое значение времени моделирования. Допустимые значения: >0")
        return
    elif not(Decimal(f'{time}') % Decimal(f'{time_step}') == 0):
        messagebox.showerror("Ошибка", "Введено недопустимое значение шага по времени. Время работы установки должно быть кратно шагу.")
        return
    elif not(0 <= rpm_o <= 100):
        messagebox.showerror("Ошибка", "Введено недопустимое значение частоты вращения образца. Допустимые значения:0-100")
        return
    elif not(0 <= rpm_b <= 100):
        messagebox.showerror("Ошибка", "Введено недопустимое значение частоты вращения барабана. Допустимые значения:0-100")
        return

    if not (enabled_sh):
        rad_sh = 0
        height_sh = 0

    exit_flag.clear()
    print(time_step)
    disable_buttons_for_frames(frames)
    drum = Drum_with_podlozkda(rad=rad_b, rpm=rpm_b, holders_rad=rad_o, holders_rpm=rpm_o)
    mishen = Mishen(m_distance, -m_height / 2, m_height / 2, -m_width / 2, m_width / 2)
    drum.make_custom_holder(holder_angle=psi, point_angle=ksi)
    d_field.set(0)
    ct_field.set(0)
    one_dot_visualize_midpoint(
        fig,
        ax1,
        ax2,
        exit_flag,
        nx=nx,
        ny=ny,
        cond_enabled=True,
        drum_with_podlozkda=drum,
        mishen=mishen,
        k=k,
        time_step=time_step,
        seconds=time,
        d_field=d_field,
        ct_field=ct_field,
        height_sh=height_sh / 2,
        rad_sh=rad_sh
    )

def disable_shtuka(var, param1, param2):
    if var.get() is False:
        param1.configure(state='disable')
        param2.configure(state='disable')
    else:
        param1.configure(state='normal')
        param2.configure(state='normal')

def stop(frames):
    enable_buttons_for_frames(frames)
    exit_flag.set()


if __name__ == "__main__":
    # This defines the Python GUI backend to use for matplotlib
    matplotlib.use('TkAgg')

    # Initialize an instance of Tk
    root = tk.Tk()

    # Initialize matplotlib figure for graphing purposes
    # fig, (ax1, ax2) = plt.subplots(2)
    # ax1.set_title("")
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    ax1.title.set_text("Вид сверху")
    ax2.title.set_text("Вид на плоскость мишени c точки")
    # fig.tight_layout()
    # Special type of "canvas" to allow for matplotlib graphing
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()

    # Add the plot to the tkinter widget
    plot_widget.grid(row=0, column=1, sticky="nsew")

    # Create a tkinter button at the bottom of the window and link it with the updateGraph function
    root.title("Моделирование нанесения наноструктур в магнетроннах барабанного вида")
    root.geometry('{}x{}'.format(800, 890))
    root.minsize(width=800, height=890)
    # top_frame = tk.Frame(root, bg='cyan', width=450, height=50, pady=3)
    # center = tk.Frame(root, bg='gray2', width=50, height=40, padx=3, pady=3)
    # btm_frame = tk.Frame(root, bg='white', width=450, height=45, pady=3)
    # btm_frame2 = tk.Frame(root, bg='lavender', width=450, height=60, pady=3)

    paramsFrame = tk.Frame(root, bg="green")
    outputFrame = tk.Frame(root)
    # root.grid_rowconfigure(0, weight=1)
    # root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=0)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=0)
    root.grid_rowconfigure(1, weight=1)

    paramsFrame.grid(row=0, column=0, sticky="nsew")
    outputFrame.grid(row=0, column=2, sticky="nsew")
    labelframeBar = tk.LabelFrame(paramsFrame, text="Параметры барабана")
    labelframeObr = tk.LabelFrame(paramsFrame, text="Параметры образца")
    labelframeMish = tk.LabelFrame(paramsFrame, text="Параметры мишени")
    labelframeSred = tk.LabelFrame(paramsFrame, text="Параметры среды")
    labelframeMM = tk.LabelFrame(paramsFrame, text="Параметры моделирования")
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
    labelTextObrPsi.set("Начальный угол \nрассматриваемой точки")
    labelObrPsi = tk.Label(labelframeObr, textvariable=labelTextObrPsi, height=2)
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


    # Штука
    labelTextMishRadVnutr = tk.StringVar()
    labelTextMishRadVnutr.set("Радиус штуки")
    labelMishRadVnutr = tk.Label(labelframeMish, textvariable=labelTextMishRadVnutr, height=1)
    entryTextMishRadVnutr = tk.DoubleVar()
    entryTextMishRadVnutr.set(0)
    entryMishRadVnutr = tk.Entry(labelframeMish, text=entryTextMishRadVnutr)
    entryMishRadVnutr.configure(state="disabled")
    labelTextMishHeightVnutr = tk.StringVar()
    labelTextMishHeightVnutr.set("Высота штуки")
    labelMishHeightVnutr = tk.Label(labelframeMish, textvariable=labelTextMishHeightVnutr, height=1)
    entryTextMishHeightVnutr = tk.DoubleVar()
    entryTextMishHeightVnutr.set(0)
    entryMishHeightVnutr = tk.Entry(labelframeMish, text=entryTextMishHeightVnutr)
    entryMishHeightVnutr.configure(state="disabled")

    labelTextMishEnableVnutr = tk.BooleanVar()
    labelTextMishEnableVnutr.set(False)
    labelMishEnableVnutr = tk.Checkbutton(labelframeMish, text="Штука", variable=labelTextMishEnableVnutr, height=1, command=lambda: disable_shtuka(labelTextMishEnableVnutr, entryMishRadVnutr, entryMishHeightVnutr))
    labelMishEnableVnutr.pack(side="top", anchor="nw", expand=True)
    labelMishRadVnutr.pack(side="top", anchor="nw", expand=True)
    entryMishRadVnutr.pack(side="top", anchor="nw", expand=True)
    labelMishHeightVnutr.pack(side="top", anchor="nw", expand=True)
    entryMishHeightVnutr.pack(side="top", anchor="nw", expand=True)

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

    labelTextTime = tk.StringVar()
    labelTextTime.set("Время работы")
    labelTime = tk.Label(labelframeMM, textvariable=labelTextTime, height=1)
    labelTime.pack(side="top", anchor="nw", expand=True)

    entryTextTime = tk.IntVar()
    entryTextTime.set(1)
    entryTime = tk.Entry(labelframeMM, text=entryTextTime)
    entryTime.pack(side="top", anchor="nw", expand=True)

    ## OutputFrame
    entryLabelD = tk.StringVar()
    entryLabelD.set("Текущая толщина пленки: ")
    entryLabelDl = tk.Label(outputFrame, textvariable=entryLabelD, height=1)
    entryLabelDl.pack(side="top", anchor="nw")

    entryTextD = tk.StringVar()
    entryTextD.set(0)
    entryTextDl = tk.Label(outputFrame, textvariable=entryTextD, height=1)
    entryTextDl.pack(side="top", anchor="nw")

    entryLabelTTime = tk.StringVar()
    entryLabelTTime.set("Текущее время:")
    entryLabelTTimel = tk.Label(outputFrame, textvariable=entryLabelTTime, height=1)
    entryLabelTTimel.pack(side="top", anchor="nw")

    entryTextTTime = tk.StringVar()
    entryTextTTime.set(0)
    entryTextTTimel = tk.Label(outputFrame, textvariable=entryTextTTime, height=1)
    entryTextTTimel.pack(side="top", anchor="nw")

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
            entryTextTime.get(),
            framesToDisable,
            entryTextD,
            entryTextTTime,
            labelTextMishEnableVnutr.get(),
            entryTextMishRadVnutr.get(),
            entryTextMishHeightVnutr.get(),
        ),
    ).grid(row=0, column=0)
    tk.Button(frameSS, text="Стоп", command=lambda: stop(framesToDisable)).grid(row=0, column=1)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    root.mainloop()
