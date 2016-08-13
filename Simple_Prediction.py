# Carl McCann   12508463    Recommender System  Week 2

import numpy as np
import time
import sys
import warnings


class SimplePrediction:
    def __init__(self):
        pass

    # calculates a prediction for a given user-item pair, if result is nan a prediction cannot be made because the
    # user in question is the only person to have rated the item in question
    def mean_item_rating(self, uid, iid, items, print_to_term):
        # print('Creating Mean Item Ratings')
        ratings = []

        user_dict = items.get(iid)
        for user in sorted(user_dict, key=int):
            if user == uid:
                continue
            else:
                ratings.append(int(user_dict.get(user)[0]))

        # print('Mean Item Ratings Created')
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)

            if print_to_term:
                print('\nPrediction: ' + str(np.mean(ratings)))
                if items.get(iid).get(uid) is None:
                    print('\nNo actual rating exists')
                else:
                    print('Actual:     ' + str(items.get(iid).get(uid)[0]))
                    print('Difference: ' + str(self.rmse(int(items.get(iid).get(uid)[0]), np.mean(ratings))) + '\n')
            return np.mean(ratings)

    # RMSE formula
    # calculates how far away a prediction is from a rating
    def rmse(self, actual, prediction):
        return np.sqrt(np.power((actual - prediction), 2))

    # uses the rmse method to create statistics on every user-item pair, regarding actual rating, predictions, and rmse
    # format of output: user_id, item_id, actual rating, predicted rating, RMSE.
    def rmse_csv_maker(self, users, items):
        print('\nWriting RMSE csv')
        # formatting = '{0:0=3d}'

        # format of generated csv:  user, item, actual, prediction, rmse
        with open('out/prediction_simple_output/rmse.csv', 'w') as f:
            for user in sorted(users, key=int):                              # user by user now
                # print(str(round((int(user) / len(users)*100), 2)) + '%')
                sys.stdout.write("\r" + str(round((int(user) / len(users)*100), 2)) + '%')
                sys.stdout.flush()

                item_dict = users.get(user)
                # print(sorted(item_dict, key=int))
                for item in sorted(item_dict, key=int):

                    rating = item_dict.get(item)[0]
                    prediction = self.mean_item_rating(str(user), str(item), items, False)
                    f.write(user + ',' + str(item) + ',' + str(rating) + ',' +
                            str(prediction) + ',' + str(str(self.rmse(int(rating), prediction))) + '\n')

            print('\nRMSE csv created')

    # calculates an average rmse of all the user-item rmse's
    def rmse_calc(self):
        print('\nCalculating Overall RMSE Value')
        rmses = []
        count = 0
        with open('out/prediction_simple_output/rmse.csv', 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                rmses.append(float(line.split(',')[4]))
                count += 1

        with open('out/prediction_simple_output/overall_rmse_and_coverage.txt', 'w') as f:
            f.write('Overall RMSE Value:    ' + str(np.nanmean(rmses)) + '\n') # nanmean ignores nan values

        print('Overall RMSE Value:    ' + str(np.nanmean(rmses))) # nanmean ignores nan values
        print('Overall RMSE Value Calculated')
        return

    # calculates how many predictions can be made, rather than not made, e.g. you cannot predict for a user when he/she
    # is the only person to have rated the tem in question
    def coverage(self):
        print('\nCalculating Coverage')
        nan = 0
        non_nan = 0

        with open('out/prediction_simple_output/rmse.csv', 'r') as f:
            for line in f:
                line = line.rstrip('\n')

                if line.split(',')[3] == 'nan':
                    nan += 1
                else:
                    non_nan += 1
            with open('out/prediction_simple_output/overall_rmse_and_coverage.txt', 'a') as f1:
                f1.write('Coverage:              ' + str((non_nan / (nan + non_nan)) * 100) + '%')

        print('Coverage:              ' + str((non_nan / (nan + non_nan)) * 100) + '%')
        print('Coverage Calculated')
        return

    # runs the method rmse_csv_maker for as many runs specified to produce an average of its run time
    def l1o_run_time(self, users, items, runs):
        print("\nTesting L1O Run Time")
        run_times = []
        with open('out/prediction_simple_output/L1O_run_times.txt', 'w') as f:
            for i in range(1, runs + 1):
                start_time = time.time()
                self.rmse_csv_maker(users, items)
                run_time = time.time() - start_time
                f.write(str(i) + ':\t\t\t' + str(round(run_time, 2)) + 's\n')
                run_times.append(run_time)
                print('Run ' + str(i) + ' of ' + str(runs) + ' complete')

            print()
            for i in range(0, len(run_times)):
                print(str(i+1) + ':\t\t\t' + str(round(run_times[i], 2)) + 's')

            print('\nMean:\t\t' + str(round(np.mean(run_times), 2)) + 's')
            print('Median:\t\t' + str(round(np.median(sorted(run_times, key=float)), 2)) + 's')
            print('Min:\t\t' + str(round(np.min(run_times), 2)) + 's')
            print('Max:\t\t' + str(round(np.max(run_times), 2)) + 's')

            f.write('\nMean:\t\t' + str(round(np.mean(run_times), 2)) + 's\n')
            f.write('Median:\t\t' + str(round(np.median(sorted(run_times, key=float)), 2)) + 's\n')
            f.write('Min:\t\t' + str(round(np.min(run_times), 2)) + 's\n')
            f.write('Max:\t\t' + str(round(np.max(run_times), 2)) + 's\n')

        return
