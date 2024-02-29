import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import json
import tkinter as tk

ads_neg_path = r"D:\dev\github.com\AleX-PirS\stand\test_stand\scripts\ADC_script\ADC_NEG"
ads_pos_path = r"D:\dev\github.com\AleX-PirS\stand\test_stand\scripts\ADC_script\ADC_POS"


def open_files(json_path, json_list, pol, scale, offset):
    result = []
    for file in json_list:
        with open(os.path.join(json_path, file)) as json_file:
            data = json.load(json_file)

            json_data = data['data'][str(offset)]
            amplitude = 1.8-offset+(pol*(np.array(json_data[0]) / scale))
            adc_code = np.array(json_data[1])

            result.append((amplitude, adc_code))
    return result


def get_normalized_data(ads_neg_path, ads_pos_path):
    neg_json_files = [pos_json for pos_json in os.listdir(
        ads_neg_path) if pos_json.endswith('.json')]
    pos_json_files = [pos_json for pos_json in os.listdir(
        ads_pos_path) if pos_json.endswith('.json')]
    
    neg_points = open_files(ads_neg_path, neg_json_files, -1, 5.55555, 0.9)
    pos_points = open_files(ads_pos_path, pos_json_files, 1, 5.55555, 0.9)

    points = []
    for i in range(len(neg_points)):
        ampls = np.append(neg_points[i][0], pos_points[i][0])
        vals = np.append(neg_points[i][1], pos_points[i][1])
        points.append((ampls, vals))

    plot_all(points)
    i_s, dnl = measure_dnl(points)
    plt.legend(loc='upper left')
    measure_inl(i_s, dnl)
    plt.legend(loc='upper left')
    a, b = plot_mean_data(points)
    plt.show()


def plot_mean_data(points):
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(
        screen_width / 125, screen_height / 125))

    mean_points = []
    for i in range(len(points[0][1])):
        to_mean = []
        for j in range(len(points)):
            to_mean.append(points[j][1][i])
        mean_points.append(np.mean(to_mean, dtype=int))

    a, b = np.polyfit(points[0][0], mean_points, 1)

    axs.plot(points[0][0], mean_points)
    axs.set_title(f"ADC mean. ax+b, a={a}, b={b}")
    axs.set_xlabel("Amplitude, V")
    axs.set_ylabel("ADC code")
    axs.grid(True, which='both')

    axs.plot(points[0][0], a*points[0][0]+b)

    fig.savefig('plot_mean_data.pdf', format='pdf')
    fig.savefig('plot_mean_data.png', format='png')

    return a, b


def plot_all(points):
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(
        screen_width / 125, screen_height / 125))

    for data in points:
        axs.plot(data[0], data[1])
        axs.set_title("ADC statistic")
        axs.set_xlabel("Amplitude, V")
        axs.set_ylabel("ADC code")
        axs.grid(True, which='both')

    fig.savefig('plot_all.pdf', format='pdf')
    fig.savefig('plot_all.png', format='png')


def measure_dnl(points):
    start_val = 280
    end_val = 750
    start_val = 10
    end_val = 993
    n_dict = {}
    for point_list in points:
        for val in point_list[1]:
            n_dict[val] = n_dict.get(val, 0) + 1
    
    items = [n_dict[val] for val in list(n_dict.keys()) if val >= start_val and val <= end_val]

    mean = sum(items) / len(items)

    dnl = []    
    for i in range(start_val, end_val):
        try:
            dnl.append((n_dict[i]/mean) - 1)
        except:
            dnl.append(0)

    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(
        screen_width / 125, screen_height / 125))

    max_dnl = round(max(dnl), 3)
    min_dnl = round(min(dnl), 3)
    min_dnl_abs = round(min(abs(i) for i in dnl if abs(i) > 0), 3)

    axs.bar(range(start_val, end_val), dnl, width=2)
    axs.plot([start_val, end_val], [max_dnl, max_dnl],
             color='r', label=f'Max val:{max_dnl}')
    axs.plot([start_val, end_val], [min_dnl, min_dnl],
             color='g', label=f'Min val:{min_dnl}')
    axs.set_title(
        f"DNL. max_value={max_dnl}. min_value={min_dnl}. min_dnl_abs:{min_dnl_abs}")
    axs.set_xlabel("code i")
    axs.set_ylabel("DNL")
    axs.grid(True, which='both')

    fig.savefig('measure_dnl.pdf', format='pdf')
    fig.savefig('measure_dnl.png', format='png')

    return (range(start_val, end_val), dnl)


def measure_inl(i_s, dnl):
    inl = []
    for idx, i_point in enumerate(i_s):
        inl.append(sum(dnl[:idx]))

    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(
        screen_width / 125, screen_height / 125))

    max_inl = round(max(inl), 3)
    min_inl = round(min(inl), 3)
    min_inl_abs = min(abs(i) for i in inl if abs(i) > 0)

    axs.bar(i_s, inl, width=2)
    axs.plot([i_s[0], i_s[-1]], [max_inl, max_inl],
             color='r', label=f"Max val:{max_inl}")
    axs.plot([i_s[0], i_s[-1]], [min_inl, min_inl],
             color='g', label=f"Min val:{min_inl}")
    axs.set_title(
        f"INL. max_value={max_inl}. min_value={min_inl}. min_dnl_abs:{min_inl_abs}")
    axs.set_xlabel("code i")
    axs.set_ylabel("INL")
    axs.grid(True, which='both')

    fig.savefig('measure_inl.pdf', format='pdf')
    fig.savefig('measure_inl.png', format='png')


if __name__ == "__main__":
    print(get_normalized_data(ads_neg_path, ads_pos_path))
