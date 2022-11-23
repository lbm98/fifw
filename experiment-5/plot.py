import matplotlib.pyplot as plt


def main():
    with open('sta0.data', 'r') as fh:
        lines = fh.readlines()

        times = []
        dbms = []
        for data in lines:
            time, dbm = data.split(" ")
            dbm = dbm.strip()
            times.append(float(time))
            dbms.append(int(dbm))

        fig, ax = plt.subplots()
        ax.scatter(times, dbms)
        fig.savefig('sta0')
        plt.close()


if __name__ == '__main__':
    main()