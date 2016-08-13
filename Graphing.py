# Carl McCann   12508463    Recommender System  4

import matplotlib.pyplot as plt

class Graphing:
    def __init__(self):
        pass

    # plots the 2 neighbourhoods specified in the spec to a coverage graph together
    def plot_coverage(self, n_sizes, min_corated, n_type):
        print('\nPlotting Coverages')
        x = []
        coverages = [] # msd
        coverages_2 = [] # cosine
        coverages_3 = [] # pearson
        output_location = 'out/graphing/coverages_'
        colours = ['r', 'g', 'b', 'm', 'c', 'y']

        # if n_type == 'msd':
        #     output_location = 'out/prediction_advanced_output/msd/'
        #
        # if n_type == 'cosine':
        #     output_location = 'out/prediction_advanced_output/cosine/'
        #
        # if n_type == 'identical':
        #     output_location = 'out/prediction_advanced_output/identical/'

        for i in range(1, len(n_sizes) + 1):
            x.append(i)

        with open('out/prediction_advanced_output/msd/' + 'graph_data_min_corated_' + str(min_corated) + '.csv', 'r') as f:
            for line in f:
                coverages.append(float(line.split(',')[2]))

        with open('out/prediction_advanced_output/cosine/' + 'graph_data_min_corated_' + str(min_corated) + '.csv', 'r') as f:
            for line in f:
                coverages_2.append(float(line.split(',')[2]))
        with open('out/prediction_advanced_output/resnick/pearson/' + 'graph_data_min_corated_' + str(min_corated) + '.csv',
                  'r') as f:
            for line in f:
                coverages_3.append(float(line.split(',')[2]))
        # fig = plt.figure()
        # ax = plt.subplot(111)
        fig, ax = plt.subplots()

        plt.title('Coverage Bar Chart with Minimum Neighbourhood Overlap: ' + str(min_corated))
        ax.set_ylabel('Coverage %')
        ax.set_xlabel('Neighbourhood Size')
        width = 0.8

        # tick_label_fix = [0]
        tick_label_fix = []
        tick_label_fix.extend(map(int, n_sizes))
        ax.set_xticks(x)
        ax.set_xticklabels(tick_label_fix)

        plt.xticks(list(plt.xticks()[0]) + tick_label_fix)
        # cursor = Cursor(ax, useblit=True, color='k', linewidth=2 )

        rects1 = ax.bar(x, coverages, color='b', align='center')
        rects3 = ax.bar(x, coverages_3, color='g', align='center')
        rects2 = ax.bar(x, coverages_2, color='r', align='center')

        plt.plot([0] + coverages, color='b')
        plt.plot([0] + coverages_2, color='r')
        plt.plot([0] + coverages_3, color='g')
        ax.legend((rects1[0], rects2[0], rects3[0]), ('MSD', 'Cosine','Pearson/Resnick'), loc=0)

        plt.savefig(output_location + 'min_corated_' + str(min_corated) + '.png', bbox_inches='tight')
        plt.draw()
        plt.show()
        plt.close()
        print('Coverages Plotted')
        return

    # plots the 2 neighbourhoods specified in the spec to an rmse graph together
    def plot_rmses(self, n_sizes, min_corated, n_type):
        print('\nPlotting Differences')
        x = []
        differences = []
        differences_2 = []
        differences_3 = []

        output_location = 'out/graphing/rmse_'

        colours = ['r', 'g', 'b', 'm', 'c', 'y']

        # if n_type == 'msd':
        #     output_location = 'out/prediction_advanced_output/msd/'
        #
        # if n_type == 'cosine':
        #     output_location = 'out/prediction_advanced_output/cosine/'
        #
        # if n_type == 'identical':
        #     output_location = 'out/prediction_advanced_output/identical/'

        for i in range(1, len(n_sizes) + 1):
            x.append(i)

        with open('out/prediction_advanced_output/msd/' + 'graph_data_min_corated_' + str(min_corated) + '.csv', 'r') as f:
            for line in f:
                differences.append(float(line.split(',')[1]))

        with open('out/prediction_advanced_output/cosine/' + 'graph_data_min_corated_' + str(min_corated) + '.csv', 'r') as f:
            for line in f:
                differences_2.append(float(line.split(',')[1]))

        with open('out/prediction_advanced_output/resnick/pearson/' + 'graph_data_min_corated_' + str(min_corated) + '.csv',
                  'r') as f:
            for line in f:
                differences_3.append(float(line.split(',')[1]))

        fig = plt.figure()
        ax = plt.subplot(111)
        plt.title('Avg. RMSE with Minimum Neighbourhood Overlap: ' + str(min_corated))
        ax.set_ylabel('Avg. RMSE')
        ax.set_xlabel('Neighbourhood Size')
        width = 0.8

        # tick_label_fix = [0]
        tick_label_fix = []
        tick_label_fix.extend(map(int, n_sizes))
        ax.set_xticks(x)
        ax.set_xticklabels(tick_label_fix)
        plt.xticks(list(plt.xticks()[0]) + tick_label_fix)
        # cursor = Cursor(ax, useblit=True, color='k', linewidth=2 )


        rects2 = ax.bar(x, differences_2, color='r', align='center')
        rects1 = ax.bar(x, differences, color='b', align='center')
        rects3 = ax.bar(x, differences_3, color='g', align='center')

        plt.plot([0] + differences_2, color='r')
        plt.plot([0] + differences, color='b')
        plt.plot([0] + differences_3, color = 'g')

        ax.legend((rects1[0], rects2[0], rects3[0]), ('MSD', 'Cosine', 'Pearson/Resnick'), loc=0)

        plt.savefig(output_location + 'min_corated_' + str(min_corated) + '.png', bbox_inches='tight')
        plt.draw()
        plt.show()
        plt.close()
        print('Differences Plotted')
        return