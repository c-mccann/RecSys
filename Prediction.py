# Carl McCann   12508463    Recommender System  Week 3,4

import numpy as np
import os.path
import time
import sys
import math
import matplotlib.pyplot as plt

class Prediction:
    def __init__(self):
        pass
    # writes predictions to file
    def prediction_file_writer(self, user_data, n_size, neighbourhood_choice):
        print('\nCreating MSD prediction and Difference Values')
        max_diff = np.square(5 - 1)
        avg = 0.0
        output_location = ''
        lines = []

        # edit for week 4
        if neighbourhood_choice == 'cosine':
            with open('out/neighbourhoods/neighbourhood_cosine_distance_based.csv', 'r') as f: # pulls neighbourhoods into list
                lines = f.readlines()
                output_location = 'out/prediction_advanced_output/cosine/cosine_prediction_values.csv'

        elif neighbourhood_choice == 'msd':
            with open('out/neighbourhoods/neighbourhood_mean_squared_diff_based.csv', 'r') as f: # pulls neighbourhoods into list
                lines = f.readlines()
                output_location = 'out/prediction_advanced_output/msd/msd_prediction_values.csv'

        elif neighbourhood_choice == 'identical':
            with open('out/neighbourhoods/neighbourhood_identical_ratings_based.csv', 'r') as f: # pulls neighbourhoods into list
                lines = f.readlines()
                output_location = 'out/prediction_advanced_output/identical/id_prediction_values.csv'



        # wij = 1 - (sim(user_i, user_j) / MaxDiff)     # where MaxDiff == 16 based on 1-5 rating scale system
        # prediction = (sum of (wij * (rating(user_j, item_k)))) / sum of ( wij )

        with open(output_location, 'w') as f:
            for user in sorted(user_data, key=int):                             # for each user
                # pprint.pprint(lines)
                # pprint.pprint(lines[:10])
                # print('Testing')
                # print(user)
                # print(len(lines))
                # print(lines[int(user) -1])

                spec_user_neighbourhood_info = lines[int(user) - 1].split(',')  # get the specific user neighbourhood
                # print(lines[int(user) - 1].split(','))

                spec_user_data = user_data.get(user)                            # get the users item info
                sys.stdout.write("\r" + str(round((int(user) / len(user_data)*100), 2)) + '%')
                sys.stdout.flush()
                for item in sorted(spec_user_data, key=int):                    # for each item, of the current user
                    spec_user_rating = spec_user_data.get(item)[0]              # get the rating

                    ws = []                                         # bottom part of the prediction formula b4 summation
                    ws_by_curr_user_rating = []                     # top part of the prediction formula b4 summation
                    for i in range(1, n_size+1):                         # for the first n neighbours
                        if i == len(spec_user_neighbourhood_info):  # break if neighbourhood smaller than n
                            break
                        neighbour = spec_user_neighbourhood_info[i].split(':')[0]   # gets the neighbour
                        difference = spec_user_neighbourhood_info[i].split(':')[1]  # and the difference value
                        # input(ws)
                        # print(item)
                        # input(user_data.get(neighbour).get(item))
                        if user_data.get(neighbour).get(item) is not None: # if the neighbour has rated the current item
                            ws.append(1 - (float(difference) / max_diff))  # following lines from prediction formula
                            w_by_rating = (1 - (float(difference) / max_diff)) * int(user_data.get(neighbour).get(item)[0])
                            ws_by_curr_user_rating.append(w_by_rating)

                    # print(ws_by_curr_user_rating)
                    # print(np.sum(ws_by_curr_user_rating))
                    # print(ws)
                    # print(np.sum(ws))
                    # print()

                    if ws:                                          # if there are values to generate a prediction
                        numerator = np.sum(ws_by_curr_user_rating)  # can be empty if neighbours haven't rated the item
                        denominator = np.sum(ws)                    # <- summation part of prediction formula
                        # input()
                        # print(ws_by_curr_user_rating)
                        # print(len(ws_by_curr_user_rating))
                        # print(numerator)
                        # print(ws)
                        # print(len(ws))
                        # print(denominator)
                        # print(type(spec_user_rating))
                        # print('User:         \t' + str(user))
                        # print('Item:         \t' + item)
                        # print('actual rating:\t' + str((spec_user_rating)))
                        # print('prediction:   \t' + str(numerator / denominator))
                        # print('difference:   \t' + str(np.abs(float(spec_user_rating) - float(numerator / denominator))))

                        avg += np.abs(float(spec_user_rating) - float(numerator / denominator))
                        rating_prediction_difference = np.abs(float(spec_user_rating) - float(numerator / denominator))

                        if not np.isnan(rating_prediction_difference):
                            if not np.isinf(rating_prediction_difference):
                                # writes to csv in format: user_id,item_id,rating, prediction,difference
                                f.write(user + ',' + item + ',' + spec_user_rating + ',' +
                                        str(numerator / denominator) + ',' +
                                        str(rating_prediction_difference) + '\n')

                # print(str(avg / len(spec_user_data)))
                # print(avg)

        print('\nMSD prediction and Difference Values Created')
        return

    # gets the average mean squared difference for all predictions
    def overall_msd_value_calc(self, n_type):
        print('\nCalculating Overall MSD Difference Value')

        if n_type == 'msd':
            output_location = 'out/prediction_advanced_output/msd/msd'

        if n_type == 'cosine':
            output_location = 'out/prediction_advanced_output/cosine/cosine'

        if n_type == 'identical':
            output_location = 'out/prediction_advanced_output/identical/id'

        with open(output_location + '_prediction_values.csv', 'r') as f:
            sd = []
            for line in f:
                sd.append(float(line.split(',')[4]))

        print('Overall MSD Difference Value Calculated')
        if n_type == 'identical':
            print('Overall MSD difference mean:\t' + str(np.nanmean(sd)))
            return np.nanmean(sd)

        print('Overall MSD difference mean:\t' + str(np.mean(sd)))
        return np.mean(sd)

    # produces the coverage achieved by predictions, varies due to neighbourhood size/ minimum overlap
    def msd_prediction_coverage(self, n_type):
        print('\nCalculating MSD Prediction Coverage')

        if n_type == 'msd':
            output_location = 'out/prediction_advanced_output/msd/msd'

        if n_type == 'cosine':
            output_location = 'out/prediction_advanced_output/cosine/cosine'

        if n_type == 'identical':
            output_location = 'out/prediction_advanced_output/identical/id'

        # although not msd_prediction this method is badly named and will work with the prediction values
        # from pearson resnick

        with open(output_location + '_prediction_values.csv', 'r') as f:
            lines = f.readlines()

        with open('res/MovieLens-100k-dataset.csv', 'r') as f:
            lines_2 = f.readlines()

        print('Coverage:\t\t\t\t\t\t' + str(round((len(lines)/len(lines_2))*100, 2)) + '%')
        print('MSD Prediction Coverage Calculated')
        return round((len(lines)/len(lines_2))*100, 2)

    # generates a csv in the format: neighbourhood_size,average_prediction_difference,coverage, run_time
    def generate_graphing_data(self, user_data, n_sizes, min_corated, n_type):
        print('\nGenerating Graph Data')
        x = []
        coverages = []
        differences = []
        output_location = ''
        colours = ['r', 'g', 'b', 'm', 'c', 'y']

        if n_type == 'msd':
            output_location = 'out/prediction_advanced_output/msd/'

        if n_type == 'cosine':
            output_location = 'out/prediction_advanced_output/cosine/'

        if n_type == 'identical':
            output_location = 'out/prediction_advanced_output/identical/'

        if n_type == 'pearson':
            output_location = 'out/prediction_advanced_output/resnick/resnick/'

        for i in range(1, len(n_sizes) + 1):
            x.append(i)

            # outputs neighbourhood size specific csvs in the format:
            # n_size, overall_diff_between_ratings_and_predictions, coverage, run_time
        if os.path.isfile(output_location + 'graph_data_min_corated_' + str(min_corated) + '.csv'):
            a = input('Do you want to rewrite graph_data file[Y/n]: ')

            # cant check if the write data exists yet, therefore commented out
            # if a == 'y' or a == 'Y':
            with open(output_location + 'graph_data_min_corated_' + str(min_corated) + '.csv', 'w') as f:
                for n in n_sizes:
                    start_time = time.time()
                    self.prediction_file_writer(user_data, int(n), n_type)

                    f.write(str(n) + ',' + str(self.overall_msd_value_calc(n_type)) + ',' +
                        str(self.msd_prediction_coverage(n_type)) + ',' + str(time.time()-start_time) + '\n')
        else:
            with open(output_location + 'graph_data_min_corated_' + str(min_corated) + '.csv', 'w') as f:
                for n in n_sizes:
                    start_time = time.time()
                    self.prediction_file_writer(user_data, int(n), n_type)
                    f.write(str(n) + ',' + str(self.overall_msd_value_calc(n_type)) + ',' +
                        stroverall_resnick_rmse_calc()(self.msd_prediction_coverage(n_type)) + ',' + str(time.time()-start_time) + '\n')
        print('\nGraph Data Generated')
        return

    # plots coverage from graphing data
    def plot_coverage(self, n_sizes, min_corated, n_type):
        print('\nPlotting Coverages')
        x = []
        coverages = []
        output_location = ''
        colours = ['r', 'g', 'b', 'm', 'c', 'y']

        if n_type == 'msd':
            output_location = 'out/prediction_advanced_output/msd/'

        if n_type == 'cosine':
            output_location = 'out/prediction_advanced_output/cosine/'

        if n_type == 'identical':
            output_location = 'out/prediction_advanced_output/identical/'

        for i in range(1, len(n_sizes) + 1):
            x.append(i)

        with open(output_location + 'graph_data_min_corated_' + str(min_corated) + '.csv', 'r') as f:
            for line in f:
                coverages.append(float(line.split(',')[2]))

        fig = plt.figure()
        ax = plt.subplot(111)
        plt.title('Coverage Bar Chart with Minimum Neighbourhood Overlap: ' + str(min_corated))
        ax.set_ylabel('Coverage %')
        ax.set_xlabel('Neighbourhood Size')
        width = 0.8

        # tick_label_fix = [0]
        tick_label_fix = []
        tick_label_fix.extend(map(int,n_sizes))
        ax.set_xticks(x)
        ax.set_xticklabels(tick_label_fix)
        plt.xticks(list(plt.xticks()[0]) + tick_label_fix)
        # cursor = Cursor(ax, useblit=True, color='k', linewidth=2 )
        for i in range(0, len(n_sizes)):
            ax.bar(x[i], coverages[i], color=colours[i % (len(colours))], align='center')

        plt.savefig(output_location + 'coverage_bar_chart_min_corated_' + str(min_corated) + '.png', bbox_inches='tight')
        plt.draw()
        plt.show()
        print('Coverages Plotted')
        return

    # plots avg. differences from graphing data
    def plot_differences(self, n_sizes, min_corated, n_type):
        print('\nPlotting Differences')
        x = []
        differences = []

        colours = ['r', 'g', 'b', 'm', 'c', 'y']

        if n_type == 'msd':
            output_location = 'out/prediction_advanced_output/msd/'

        if n_type == 'cosine':
            output_location = 'out/prediction_advanced_output/cosine/'

        if n_type == 'identical':
            output_location = 'out/prediction_advanced_output/identical/'

        for i in range(1, len(n_sizes) + 1):
            x.append(i)

        with open(output_location + 'graph_data_min_corated_' + str(min_corated) + '.csv', 'r') as f:
            for line in f:
                differences.append(float(line.split(',')[1]))

        fig = plt.figure()
        ax = plt.subplot(111)
        plt.title('Avg. RMSE with Minimum Neighbourhood Overlap: ' + str(min_corated))
        ax.set_ylabel('Avg. RMSE')
        ax.set_xlabel('Neighbourhood Size')
        width = 0.8

        # tick_label_fix = [0]
        tick_label_fix = []
        tick_label_fix.extend(map(int,n_sizes))
        ax.set_xticks(x)
        ax.set_xticklabels(tick_label_fix)
        plt.xticks(list(plt.xticks()[0]) + tick_label_fix)
        # cursor = Cursor(ax, useblit=True, color='k', linewidth=2 )
        for i in range(0, len(n_sizes)):
            ax.bar(x[i], differences[i], color=colours[i % (len(colours))], align='center')

        plt.savefig(output_location + 'avg_prediction_diff_bar_chart_min_corated_' + str(min_corated)
                    + '.png', bbox_inches='tight')
        plt.draw()
        plt.show()
        print('Differences Plotted')
        return

    # extra method to return a user-item prediction to terminal for the menu system
    def user_item_prediction(self, uid, iid, n_type, n_size, users):
        if n_type == 'cosine':
            file = 'out/prediction_advanced_output/cosine/cosine_prediction_values.csv'
            with open('out/save_data/cosine_nhood_min_overlap_save_data.txt', 'r') as f:
                print('Current minimum Overlap in neighbourhood: ' + f.readline())
        if n_type == 'msd':
            file = 'out/prediction_advanced_output/msd/msd_prediction_values.csv'
            with open('out/save_data/msd_nhood_min_overlap_save_data.txt', 'r') as f:
                print('Current minimum Overlap in neighbourhood: ' + f.readline())

        if n_type == 'identical':
            file = 'out/prediction_advanced_output/identical/id_prediction_values.csv'



        print('Generating a new prediction file will take into account the neighbourhood size you provide.')
        print('If you choose not to do this, a prediction from the last time a file was generated will be used,')
        print('where you do not know the specific neighbourhood size. This does not matter for the identical')
        print('neighbourhood. This could be saved in save data in future. Generation may take a bit of time.')
        a = input('Would you like to create a new prediction file [Y/n]: ')
        if a.upper() == 'Y':
            self.prediction_file_writer(users, int(n_size), n_type)

        with open(file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith(uid + ',' + iid + ','):
                pred_list = line.split(',')
                print('\nActual:      ' + pred_list[2])
                print('Prediction:  ' + pred_list[3])
                print('RMSE:        ' + pred_list[4])

    # Week 5 Prediction Method Resnick's prediction Formula

# Resnick’s Prediction Formula

# Resnick’s Prediction Formula is a popular approach that assumes a
# correlation-based similarity function (-1 < sim < 1).

# Efectively the target user’s, target item is assigned a rating that is an
# adjusted form of the target user’s average rating.

# The adjustment is based on the degree to which neighbours rate the target
# item above or below their own average ratings, weighted by the correlation
# between the neighbour and the target user.

            # rating_bar = mean rating
    #         sim must be pearson's correlation coefficient

    # prediction(user_i,item_k) =
    # rating_bar(user_i) +
    # ( Σ (user_j ∈ neighbourhood(user_i)(rating(user_j,item_k) - rating_bar(user_j)) · sim(user_i,user_j) /
    # Σ (user_j ∈ neighbourhood(user_i)|sim(user_i,user_j| )

    # sim(user_i,user_j) = ... in notes in preview

    def resnick_prediction_file_writer(self, users, items, n_type, n_size):
        np.seterr(divide='ignore', invalid='ignore')

        with open('out/minimum_overlap_save_data.txt', 'r') as f:   # for saving output data with correct title
            min_overlap = int(f.readline().rstrip('\n'))

        # this block of code allows the use of different neighbourhoods, while keeping the pearson coefficient
        # here as an extra feature, will only be testing the pearson neighbourhoods
        neighbourhood_file = 'out/neighbourhoods/neighbourhood_'    # setting up the neighbourhood for the formula
        if n_type == 'MSD':
            n_type = 'msd'
            neighbourhood_file += 'mean_squared_diff_based.csv'
        if n_type == 'COS':
            n_type = 'cosine'
            neighbourhood_file += 'cosine_distance_based.csv'
        if n_type == 'ID':
            n_type = 'identical'
            neighbourhood_file += 'identical_rating_based.csv'
        if n_type.upper() == 'PEARSON':
            n_type = 'pearson'
            neighbourhood_file += 'pearson_correlation_based.csv'

        with open(neighbourhood_file, 'r') as f:
            neighbourhood_data = f.readlines()



        users_mean_ratings = {}  # to be used in the resnick prediction formula
        with open('out/general_statistics/user_stats.csv', 'r') as f:  # from week 1
            for line in f:
                line_split = line.rstrip('\n').split(',')
                users_mean_ratings[line_split[0]] = line_split[1]

        # this block of code could be may be unnecessary as these values can be pulled from the neighbourhood file
        # however for use with non-pearson neighbourhoods this is necessary, so i left it in
        pearson_correlation_values = {} # to be used in the resnick prediction formula later on
        with open('out/correlation/users_pearson_correlation.csv', 'r') as f:
            for line in f:
                line_split = line.rstrip('\n').split(',')
                if pearson_correlation_values.get(line_split[0]) is None:
                    pearson_correlation_values[line_split[0]] = {line_split[1]: float(line_split[2])}
                else:
                    pearson_correlation_values.get(line_split[0]).update({line_split[1]: float(line_split[2])})

        print('\nNeighbourhood, Mean Ratings, and Pearson Correlation Values loaded from files')

        # creates prediction files in for specific neighbourhoods

        with open('out/prediction_advanced_output/resnick/pearson/prediction_values.csv', 'w') as f:
            i = 0   # user as index for neighbourhood_data at higher min overlap was causing out of bounds errors
            for user in sorted(users, key=int): # for each user
                sys.stdout.write("\r" + str(round((i / len(users) * 100), 2)) + '%')
                sys.stdout.flush()
                user_mean_rating = users_mean_ratings.get(user) # average user rating

                # get neighbourhood, for specified user, split it, and slice list to specified n_size
                # entry in user_neighbourhood = [neighbour:similarity_metric], will need to be split later

                if not user == neighbourhood_data[i].rstrip('\n').split(',')[0]:
                    continue

                user_neighbourhood = neighbourhood_data[i].rstrip('\n').split(',')[1:int(n_size)+1]

                users_items = users.get(user)
                for item in sorted(items, key=int):
                    users_that_have_rated_item = items.get(item)
                    numerator = 0.0
                    denominator = 0.0
                    for neighbour in user_neighbourhood:
                        neighbour_data = neighbour.split(':')  # [0] = neighbour, [1] = sim metric
                        comp_user_mean_rating = float(users_mean_ratings.get(neighbour_data[0]))
                        comp_user_items = users.get(neighbour_data[0])

                        # corated = comp_user_items.get(item)
                        # if corated is not None:

                        corated_item = users_that_have_rated_item.get(neighbour_data[0])
                        if corated_item is not None: ### PROBLEM WITH FORMULA CALCULATION ###
                            neighbour_rating = float(corated_item[0])
                            lhs = neighbour_rating - comp_user_mean_rating  # r(user_j,item_k) - r_bar(user_j)
                            sim = pearson_correlation_values.get(user).get(neighbour_data[0]) # sim(user_i,user_j)
                            if sim is None:
                                continue
                            numerator += np.dot(lhs, sim) # add dot product to numerator (summation)
                            denominator += np.abs(sim) # add abs value of sim to denominator (summation)

                    # checking nan with numpy's nan wasn't working as intended
                    if not math.isnan(np.divide(numerator, denominator)):
                            prediction = float(user_mean_rating) + np.divide(numerator, denominator)
                            if not math.isnan(prediction):
                                actual_rating = users_items.get(item)
                                if actual_rating is not None:
                                    f.write(user + ',' + item + ',' + actual_rating[0] + ',' +
                                            str(prediction) + ',' + str(np.abs(float(actual_rating[0]) -
                                                                               prediction)) + '\n')

                                # commented out as this wrote predictions with no rmse to be averaged
                                # else:
                                #     f.write(user + ',' + item + ',' + '-1' + ',' +
                                #             str(prediction) + ',' + '-1' + '\n')
                                    # format:   user,
                                    #           item,
                                    #           actual rating if it exists, -1 if it doesnt
                                    #           prediction
                                    #           rmse only if actual rating exists, -1 if it doesn't
                i += 1
        return

    def overall_resnick_rmse_calc(self):
        rmses = []

        with open('out/prediction_advanced_output/resnick/pearson/prediction_values.csv', 'r') as f:
            for line in f:
                line_split = line.rstrip('\n').split(',')
                rmses.append(float(line_split[4]))
        print("\nAverage RMSE:\t\t\t\t\t" + str(np.divide(np.sum(rmses), len(rmses))))
        return np.divide(np.sum(rmses), len(rmses))

    def overall_resnick_coverage_calc(self):
        with open('out/prediction_advanced_output/resnick/pearson/prediction_values.csv', 'r') as f:
            lines = f.readlines()

        with open('res/MovieLens-100k-dataset.csv', 'r') as f:
            lines_2 = f.readlines()

        print('Coverage:\t\t\t\t\t\t' + str(round((len(lines) / len(lines_2)) * 100, 2)) + '%')
        print('Resnick Prediction Coverage Calculated')
        return round((len(lines) / len(lines_2)) * 100, 2)


    def generate_resnick_graphing_data(self, user_data, item_data, n_sizes, min_corated):
        print('\nGenerating Resnick Graph Data')
        n_sizes = n_sizes.split(',')
        x = []
        coverages = []
        differences = []
        output_location = ''
        colours = ['r', 'g', 'b', 'm', 'c', 'y']

        output_location = 'out/prediction_advanced_output/resnick/pearson/'

        for i in range(1, len(n_sizes) + 1):
            x.append(i)

            # format:
            # n_size, overall_rmse, coverage, run_time
        if os.path.isfile(output_location + 'graph_data_min_corated_' + str(min_corated) + '.csv'):
            a = input('Do you want to rewrite graph_data file[Y/n]: ')

            # cant check if the write data exists yet, therefore commented out
            # if a == 'y' or a == 'Y':
            with open(output_location + 'graph_data_min_corated_' + str(min_corated) + '.csv', 'w') as f:
                for n in n_sizes:
                    start_time = time.time()
                    self.resnick_prediction_file_writer(user_data, item_data, 'pearson', n)

                    print(n_sizes)
                    print('n_size ' + str(n))
                    f.write(str(n) + ',' + str(self.overall_resnick_rmse_calc()) + ',' +
                            str(self.overall_resnick_coverage_calc()) + ',' + str(time.time() - start_time) + '\n')
        else:
            with open(output_location + 'graph_data_min_corated_' + str(min_corated) + '.csv', 'w') as f:
                for n in n_sizes:
                    start_time = time.time()
                    self.resnick_prediction_file_writer(user_data, item_data, 'pearson', n)
                    f.write(str(n) + ',' + str(self.overall_resnick_rmse_calc()) + ',' +
                            str(self.overall_resnick_coverage_calc()) + ',' + str(time.time() - start_time) + '\n')
        print('\nResnick Graph Data Generated')

        return