#!/usr/bin/env python3

import argparse
import sys

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy

def fmt_time(time):
    #return time.isoformat().split("T")[1][:5]
    return time

def read_data(fname):
    with open(fname, 'r') as f:
        return f.read().split()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--output-file", required=True)
    parser.add_argument("--hours", type=int, default=12)
    parser.add_argument("--interval", help="secs between readings", default=30)
    args = parser.parse_args()

    no_datapoints = (args.hours*60*60) // args.interval
    #no_datapoints = 700
    data = read_data(args.data)
    data = [float(a) for a in data[-no_datapoints:]]

    now = datetime.now()
    t_interval = timedelta(seconds=args.interval)
    start_time = now - (t_interval * len(data))

    # matplotlib doesnt support generators
    times = [fmt_time(start_time + (t_interval*a)) for a in range(len(data))]

    x = numpy.array(times)
    y = numpy.array(data)

    fig, ax = plt.subplots()

    plt.plot(x, y)

    x_labels = ax.xaxis.get_ticklabels()
    for n, label in enumerate(x_labels[1:-1]):
        if n % 4 != 2:
            label.set_visible(False)

    plt.title("Temperature {}h".format(args.hours))
    plt.savefig(args.output_file)
