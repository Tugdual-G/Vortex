#!/usr/bin/env python3
import multiprocessing as mp
import time

import matplotlib.pyplot as plt
import numpy as np


class Plot_process:
    def __init__(self):
        """This is executed by the subprocess"""
        self.data = []
        self.cmap = "viridis"
        self.IMG_DIR = "images_output/"

    def terminate(self):
        plt.close("all")
        quit()

    def call_back(self):
        while self.pipe.poll():
            recieve = self.pipe.recv()
            if recieve is None:
                self.terminate()
                return False
            else:
                self.im.set_array(recieve)
        self.fig.canvas.draw()
        return True

    def __call__(self, pipe, period):
        # print("starting plotter...")

        self.pipe = pipe
        if self.pipe.poll(100):
            recieve = self.pipe.recv()
            self.fig, self.ax = plt.subplots()
            plt.axis("off")
            plt.tight_layout(pad=0)
            self.im = plt.imshow(recieve, self.cmap)
        else:
            print("pas de tread plot lance")
        # the interval is in millisecond
        timer = self.fig.canvas.new_timer(interval=period * 1000)
        timer.add_callback(self.call_back)
        timer.start()

        # print("...done")
        plt.show()


class Plot_sender:
    def __init__(self, period):
        """Send plotting data to a subprocess."""
        self.period = period
        self.plot_pipe, plotter_pipe = mp.Pipe()
        self.plotter = Plot_process()
        self.plot_process = mp.Process(
            target=self.plotter,
            args=(
                plotter_pipe,
                self.period,
            ),
            daemon=True,
        )
        self.plot_process.start()

    def plot_send(self, data, finished=False):
        send = self.plot_pipe.send
        if finished:
            send(None)
        else:
            send(data)


if __name__ == "__main__":
    np.random.seed(2522224)
    pl = Plot_sender()
    data = np.random.rand(100, 100)
    for ii in range(1000):
        pl.plot_send(data * (ii % 2))
        time.sleep(0.1)
    pl.plot_send(data, finished=True)
