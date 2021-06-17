from tkinter import *

root = Tk()
root.title('Model Definition')
root.geometry('{}x{}'.format(460, 350))

# create all of the main containers
top_frame = Frame(root, bg='cyan', width=450, height=50, pady=3)
center = Frame(root, bg='gray2', width=50, height=40, padx=3, pady=3)
btm_frame = Frame(root, bg='white', width=450, height=45, pady=3)
btm_frame2 = Frame(root, bg='lavender', width=450, height=60, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=3, sticky="ew")
btm_frame2.grid(row=4, sticky="ew")

root.mainloop()
