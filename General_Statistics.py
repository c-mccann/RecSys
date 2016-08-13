# Carl McCann   12508463    Recommender System  Week 1

import numpy as np


class GeneralStatistics:

    # calculates some general statistics requested in the specification
    def general_statistics(self, users, items):
        np = 0;
        print('Creating General Statistics')
        ratings = 0
        for user in users:
            movies = users.get(user)
            for movie in movies:
                ratings += 1

        print('Total number of users:              ' + str(len(users)))
        print('Total number of items:              ' + str(len(items)))
        print('Total number of ratings:            ' + str(ratings))
        density_metric = (ratings/(len(users)*len(items))) * 100
        print('Density Metric:                     ' + str("%.3g" % density_metric) + '%')

        a = input('\nWould you like to write this to a file [Y/n]: ')
        if a.upper() == 'Y':
            with open('out/general_statistics/general_statistics.txt', 'w') as f:
                f.write('Total number of users:              ' + str(len(users)) + '\n')
                f.write('Total number of items:              ' + str(len(items)) + '\n')
                f.write('Total number of ratings:            ' + str(ratings) + '\n')

                f.write('Density Metric:                     ' + str("%.3g" % density_metric) + '%\n')
                print('General Statistics File Created\n')

        return

    # generates statistics over all users and each individual user
    def user_stats(self, users):
        print("Creating User Statistics")
        all_user_ratings = []

        print('\nuser, mean, median, standard deviation, min, max\n')
        with open('out/general_statistics/user_stats.csv', 'w') as f:
            for user in sorted(users, key=int):
                ratings_list = []
                items = users.get(user)

                for item in items:
                    rat_time_list = items.get(item)
                    ratings_list.append(int(rat_time_list[0]))
                    all_user_ratings.append(int(rat_time_list[0]))

                print(user+ ', ' + str(np.mean(ratings_list)) + ', ' + str(np.median(sorted(ratings_list))) + ', ' +
                        str(np.std(ratings_list)) + ', ' + str(np.min(ratings_list)) + ', ' +
                        str(np.max(ratings_list)))

                f.write(user + ',' + str(np.mean(ratings_list)) + ',' + str(np.median(sorted(ratings_list))) + ',' +
                        str(np.std(ratings_list)) + ',' + str(np.min(ratings_list)) + ',' +
                        str(np.max(ratings_list)) + '\n')

        print('\nMean for all users:                 ' + str(np.mean(all_user_ratings)))
        print('Median for all users:               ' + str(np.median(sorted(all_user_ratings))))
        print('Standard Deviation for all users:   ' + str(np.std(all_user_ratings)))
        print('Min for all users:                  ' + str(np.min(all_user_ratings)))
        print('Max for all users:                  ' + str(np.max(all_user_ratings)))

        with open('out/general_statistics/general_statistics.txt', 'a') as f:
            f.write('\nMean for all users:                 ' + str(np.mean(all_user_ratings)) + '\n')
            f.write('Median for all users:               ' + str(np.median(sorted(all_user_ratings))) + '\n')
            f.write('Standard Deviation for all users:   ' + str(np.std(all_user_ratings)) + '\n')
            f.write('Min for all users:                  ' + str(np.min(all_user_ratings))+ '\n')
            f.write('Max for all users:                  ' + str(np.max(all_user_ratings)) + '\n')

        print("\nUser Statistics Created\n")
        return

    # generates statistics over all items and each individual item
    def item_stats(self, items):
        print("Creating Item Statistics")
        all_item_ratings = []

        print('\nitem, mean, median, standard deviation, min, max\n')

        with open('out/general_statistics/item_stats.csv', 'w') as f:
            for item in sorted(items, key=int):
                ratings_list = []
                users = items.get(item)

                for user in users:
                    rat_time_list = users.get(user)
                    ratings_list.append(int(rat_time_list[0]))
                    all_item_ratings.append(int(rat_time_list[0]))

                print(item + ', ' + str(np.mean(ratings_list)) + ', ' + str(np.median(sorted(ratings_list))) + ', ' +
                        str(np.std(ratings_list)) + ', ' + str(np.min(ratings_list)) + ', ' +
                        str(np.max(ratings_list)))

                f.write(item + ',' + str(np.mean(ratings_list)) + ',' + str(np.median(sorted(ratings_list))) + ',' +
                        str(np.std(ratings_list)) + ',' + str(np.min(ratings_list)) + ',' +
                        str(np.max(ratings_list)) + '\n')

        print('\nMean for all items:                 ' + str(np.mean(all_item_ratings)))
        print('Median for all items:               ' + str(np.median(sorted(all_item_ratings))))
        print('Standard Deviation for all items:   ' + str(np.std(all_item_ratings)))
        print('Min for all items:                  ' + str(np.min(all_item_ratings)))
        print('Max for all items:                  ' + str(np.max(all_item_ratings)))

        with open('out/general_statistics/general_statistics.txt', 'a') as f:
            f.write('\nMean for all items:                 ' + str(np.mean(all_item_ratings)) + '\n')
            f.write('Median for all items:               ' + str(np.median(sorted(all_item_ratings))) + '\n')
            f.write('Standard Deviation for all items:   ' + str(np.std(all_item_ratings)) + '\n')
            f.write('Min for all items:                  ' + str(np.min(all_item_ratings)) + '\n')
            f.write('Max for all items:                  ' + str(np.max(all_item_ratings)) + '\n')

        print("Item Statistics Created\n")
        return

    # calculates the amount of ratings each rating class received
    def rating_class_totals(self, users):
        print('Creating Rating Totals')
        ratings = [0, 0, 0, 0, 0]
        for user in users:
            items = users.get(user)
            for item in items:
                rating = int(items.get(item)[0])
                if rating == 1:
                    ratings[0] += 1
                elif rating == 2:
                    ratings[1] += 1
                elif rating == 3:
                    ratings[2] += 1
                elif rating == 4:
                    ratings[3] += 1
                elif rating == 5:
                    ratings[4] += 1

        with open('out/general_statistics/general_statistics.txt', 'a') as f:
            f.write('\n')
            for i in range(0, 5):
                print('Total number of ratings of class ' + str(i+1) + ": " + str(ratings[i]))
                f.write('Total number of ratings of class ' + str(i+1) + ": " + str(ratings[i]) + '\n')
        print('Rating Totals Created\n')
        return