import matplotlib.pyplot as plt


def main():
    with open('sta1.data', 'r') as fh:
        data = fh.readlines()
        data = [int(x) for x in data]

        fig, ax = plt.subplots()
        ax.plot(range(len(data)), data)
        fig.savefig('sta1')
        plt.close()


if __name__ == '__main__':
    main()