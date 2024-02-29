import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import json
import tkinter as tk

plot_path = r"D:\dev\github.com\AleX-PirS\stand\test_stand\scripts\ANALOG_script\plots"

MIP_SCALE_FACTOR = 83.3333

LINEAR_ENDS = {
    1: (-1, -1),
    2: (2, 31),
    3: (15, 37),
    4: (-1, -1),
}

signal_name = "CSA_LG"
names = {
    1: 'Signal',
    2: 'CSA',
    3: 'SHA',
    4: 'CMP',
}

BAN_INDEXES = (1, 4, 3)

def open_files():
    jsons = [pos_json for pos_json in os.listdir(plot_path) if pos_json.endswith('.json')]
    result = {"x": [], 1: [], 2: [], 3: [], 4: []}
    for file in jsons:
        with open(os.path.join(plot_path, file)) as json_file:
            data = json.load(json_file)

            result["x"] = list(np.array(data['x_value']) * MIP_SCALE_FACTOR)
            semi = {
                2: data['data']['2'],
                3: data['data']['3'],
                4: data['data']['4'],
            }

            for i in range(1, 5):
                if i in BAN_INDEXES:
                    continue
                if len(semi[i]) == 0:
                    continue
                result[i].append(semi[i])

    return result

def build_plots(data):
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
        
    result_figs = {}
    for key, value in list(data.items()):
        if key == "x":
            continue
        if len(value) == 0:
            continue
        
        fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(screen_width / 125, screen_height / 125))

        for plot_points in value:
            axs.plot(data["x"], plot_points)

        axs.set_title(f"{signal_name}_{names[key]}")
        axs.set_xlabel("MIPs")
        axs.set_ylabel("Amplitude, V")
        axs.grid(True, which='both')
        result_figs[key] = fig

    for idx, fig in list(result_figs.items()):
        fig.savefig(f'{signal_name}_plots_{names[idx]}.pdf', format='pdf')

    return result_figs

def build_mean_and_K(data):
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    result_figs = {}
    for key, value in list(data.items()):
        if key == "x":
            continue
        if len(value) == 0:
            continue
        
        fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(screen_width / 125, screen_height / 125))

        mean_points = []
        for i in range(len(value[0])):
            to_mean = []
            for j in range(len(value)):
                to_mean.append(value[j][i])
            mean_points.append(np.mean(to_mean, dtype=float))
        
        axs.plot(data["x"], mean_points)
        axs.set_xlabel("MIPs")
        axs.set_ylabel("Amplitude, V")
        axs.set_title(f"Mean {signal_name}_{names[key]}")
        axs.grid(True, which='both')

        
        if LINEAR_ENDS[key][0] == -1 or LINEAR_ENDS[key][1] == -1:
            return result_figs, 0, 0
        
        min_coordinate = -1
        max_coordinate = -1
        for i in range(len(data['x'])):
            if min_coordinate != -1 and max_coordinate != -1:
                break

            if min_coordinate == -1:
                if data['x'][i] >= LINEAR_ENDS[key][0]:
                    min_coordinate = i

            if max_coordinate == -1:
                if data['x'][i] >= LINEAR_ENDS[key][1]:
                    max_coordinate = i

        axs.plot(
            [data["x"][min_coordinate], data["x"][max_coordinate]],
            [mean_points[min_coordinate], mean_points[max_coordinate]],
            'ro',
        )

        a, b = np.polyfit(data["x"][min_coordinate:max_coordinate], mean_points[min_coordinate:max_coordinate], 1)

        axs.set_title(f"Mean {signal_name}_{names[key]}. ax+b, a={round(a, 5)}, b={round(b, 5)}\nStart coord={round(data['x'][min_coordinate], 2)}MIP\nStop coord={round(data['x'][max_coordinate], 2)}MIP")
        axs.plot(data["x"], a*np.array(data["x"])+b)

        result_figs[key] = fig

    for idx, fig in list(result_figs.items()):
        fig.savefig(f'{signal_name}_mean_{names[idx]}.pdf', format='pdf')
    
    return result_figs, a, b

def script():
    data = open_files()

    build_plots(data)
    build_mean_and_K(data)

    plt.show()

if __name__ == "__main__":
    script()

