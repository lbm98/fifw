from pathlib import Path
import matplotlib.pyplot as plt

def main():
    for x in Path('.').glob('*.data'):
        plot(x)

def plot(x):
    with x.open() as fh:
        data = fh.readlines()
        data = [int(dp) for dp in data]

        fig, ax = plt.subplots()
        ax.plot(range(len(data)), data)
        fig.savefig(x.stem)
        plt.close()

if __name__ == '__main__':
    main()