from pprint import pprint
import matplotlib.pyplot as plt

import iwlist



def main():
    wot = iwlist.scan('wlp6s0')
    ssids = iwlist.parse(wot)

    pprint(ssids)

    channels = list(map(lambda s: int(s['channel']) , ssids))
    signal_levels = list(map(lambda s: int(s['signal_level_dBm']) , ssids))
    labels = list(map(lambda s: s['essid'] , ssids))

    # x, y = ([8, 1, 2, 5, 8, 8, 9, 13, 13, 52, 52, 52], [-46, -84, -48, -60, -47, -47, -64, -69, -37, -45, -45, -45])

    for x, y, label in zip(channels, signal_levels, labels):
        plt.plot([x-1.5, x-1, x+1, x+1.5], [-100, y, y, -100], label=label)

    plt.xlabel('x label')
    plt.ylabel('y label')

    plt.title("Simple Plot")

    plt.legend()

    plt.show()    

if __name__ == '__main__':
    main()