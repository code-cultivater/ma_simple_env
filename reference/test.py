import time
import tkinter  as tk


windows=tk.Tk()
windows.title("simple__ma_env")
n=2
lines=5
space=100
poses=[(0,0),(4,4)]
colors=["red",'yellow']
windows.geometry("500x500")
canvas = tk.Canvas(windows, bg='white', height=500, width=500)
for i in range(lines+1):
    canvas.create_line(0,0+i*space,500,0+i*space)
    canvas.create_line(0+i*space, 0,0+i*space, 500)
ovals=[]
for i in range(n):
    ovals.append(canvas.create_oval(poses[i][1]*space,poses[i][0]*space,poses[i][1]*space+space,poses[i][0]*space+space,fill=colors[i]))

canvas.pack()
def new_pos_paint(new_poses):
    for i in range(n):
        global  poses
        canvas.move(ovals[i],(new_poses[i][1]-poses[i][1])*space,(new_poses[i][0]-poses[i][0])*space)
        poses[i]=new_poses[i]
new_poses=[[(1,1),[3,3]],[(2,2),[2,2]]]
for i in range(2):
    windows.update()
    time.sleep(1)
    new_pos_paint(new_poses[i])
windows.update()
windows.mainloop()