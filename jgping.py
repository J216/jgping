#! /usr/bin/python3
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess
import sys

graph_title="Ping Time for "+str(sys.argv[1])
graph_y_label='Time in MS'
ping_command="ping -c 1 "+str(sys.argv[1])+" | tail -n1 | cut -d '/' -f 5"

data_points=12800
# Create figure for plotting
fig = plt.figure(facecolor='gray')
fig.canvas.set_window_title(graph_title)
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
last_val = 0
# Run command as subprocess
def runSubp(command=''):
    p = subprocess.Popen("exec " +command, shell=True, stdout=subprocess.PIPE)
    p.wait()
    error_code = p.returncode
    out = str(p.communicate()[0])[2:-3].split('\\n')
    # print("\n".join(out))
    return out

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    global last_val
    # Read temperature (Celsius) from TMP102
    temp_c = runSubp(ping_command)[0]
    print(temp_c)
    # Add x and y to lists
    if temp_c != '':
        xs.append(dt.datetime.now())
        if "100% packet loss" in temp_c:
            ys.append(last_val)
        else:
            ys.append(float(temp_c))
            last_val = float(temp_c)
        # Limit x and y lists to 20 items
        xs = xs[-1*data_points:]
        ys = ys[-1*data_points:]
        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys, color='#852b2b')
        # Format plot
        ax.set_facecolor("black")
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title(graph_title)
        plt.ylabel(graph_y_label)
        fig.tight_layout()
# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()
