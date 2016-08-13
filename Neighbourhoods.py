# Carl McCann   12508463    Recommender System  Week 3, 4 + extra

import numpy as np
import time
import sys
from operator import itemgetter

class Neighbourhoods:
    # Neighbourhoods
    def identical_rating_based_neighbourhood(self, user, user_data, n):
        # print('\nGenerating Identical Rating Based Neighbourhood')
        specified_user_dict = user_data.get(user)       # dictionary of items for the user to build a neighbourhood for
        identical_ratings_user_dict = {}
        for key in user_data:                           # loop to compare every user against the specified user
            identical_ratings = 0
            if key == user:                             # to stop the specified user being put in the neighbourhood
                continue
            else:
                current_user = user_data.get(key)       # dictionary of items for the current user to test against
                for item in current_user:               # loop to compare identical ratings between spec and curr user
                    spec_user_rating = specified_user_dict.get(item)
                    curr_user_rating = current_user.get(item)
                    # print('curr user:   ' + str(curr_user_rating))
                    # print('spec user:   ' + str(spec_user_rating))
                    #
                    if spec_user_rating is not None:    # if specified user has rated the particular item
                        if int(spec_user_rating[0]) == int(curr_user_rating[0]):    # if the spec and curr users rating
                            identical_ratings += 1                                  # matches, increment count
            identical_ratings_user_dict[key] = identical_ratings                    # add user: count to dict

        # list filled with lists in the form of [user, identical_ratings], sorted by descending value from the dict
        most_similar_users = sorted(identical_ratings_user_dict.items(), key=itemgetter(1), reverse=True)
        # print(most_similar_users)

        # # how to access a pair
        # print(most_similar_users[:n][1])
        # # how to access the user
        # print(most_similar_users[:n][1][0])

        # print('Identical Rating Based Neighbourhood Generated')
        if n == -1:
            return most_similar_users
        return most_similar_users[:n]   # returns the top n similar users,

    def cosine_distance_neighbourhood(self, user, user_data, n, min_corated):
        # print("\nGenerating Cosine Distance Based Neighbourhood")
        specified_user_dict = user_data.get(user)       # dictionary of items for the user to build a neighbourhood for
        user_distance_dict = {}
        for key in user_data:
            spec_user_list = []                         # lists will act as vectors for the cosine distance function
            curr_user_list = []
            if key == user:                             # to stop the specified user being put in the neighbourhood
                continue
            else:
                current_user = user_data.get(key)       # dictionary of items for the current user to test against
                for item in current_user:               # loop to compare identical ratings between spec and curr user
                    spec_user_rating = specified_user_dict.get(item) # getting ratings
                    curr_user_rating = current_user.get(item)
                    if spec_user_rating is not None:    # if specified user has rated the particular item
                        spec_user_list.append(float(spec_user_rating[0]))   # add to vectors
                        curr_user_list.append(float(curr_user_rating[0]))

            # print('a:   ' + str(spec_user_list))
            # print('b:   ' + str(curr_user_list))
            # print(self.cosine_distance(spec_user_list, curr_user_list))

            if len(spec_user_list) >= min_corated:       # stops users who have less the five corated items being included
                user_distance_dict[key] = self.cosine_distance(spec_user_list, curr_user_list)

        # print(user_distance_dict)
        most_similar_users = sorted(user_distance_dict.items(), key=itemgetter(1), reverse=True)

        # print(most_similar_users)
        # # how to access a pair
        # print(most_similar_users[:n][1])
        # # how to access the user
        # print(most_similar_users[:n][1][0])

        # print("Cosine Distance Based Neighbourhood Generated")
        with open('out/save_data/cosine_nhood_min_overlap_save_data.txt', 'w') as f:
            f.write(str(min_corated))

        if n == -1:
            return most_similar_users
        return most_similar_users[:n]

    def cosine_distance(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    #  (rating(user_i,item_k) - rating(user_j,item_k))sqrd /
    #   | corated(user_i,user_j) |
    def mean_squared_differences_neighbourhood(self, user, user_data, n, min_corated):
        # print('\nGenerating Mean Squared Differences Neighbourhood')

        specified_user_dict = user_data.get(user)
        user_distance_dict = {}
        for key in user_data:
            spec_user_list = []
            curr_user_list = []
            if key == user:
                continue
            else:
                current_user = user_data.get(key)
                for item in sorted(current_user, key=int):
                    spec_user_rating = specified_user_dict.get(item)
                    curr_user_rating = current_user.get(item)
                    if spec_user_rating is not None:
                        spec_user_list.append(float(spec_user_rating[0]))   # add to vectors
                        curr_user_list.append(float(curr_user_rating[0]))

            if len(spec_user_list) >= min_corated: # stops users who have less than min_corated corated items being included
                sim_score = 0.0
                for i in range(0, len(spec_user_list)):
                    # creates a total of all mean_squared_difference
                    sim_score += \
                        self.mean_squared_difference(int(spec_user_list[i]), int(curr_user_list[i]), len(spec_user_list))

                # gets the average mean_squared_difference
                user_distance_dict[key] = sim_score

                # print(user_distance_dict)

        # print(user_distance_dict)
        most_similar_users = sorted(user_distance_dict.items(), key=itemgetter(1))#, reverse=True)

        # # how to access a pair
        # print(most_similar_users[:n][1])
        # # how to access the user
        # print(most_similar_users[:n][1][0])

        # print('Mean Squared Differences Neighbourhood Generated')
        if n == -1:
            return most_similar_users
        return most_similar_users[:n]

    def mean_squared_difference(self, spec_user_rating, curr_user_rating, no_corated):
        return np.square(spec_user_rating - curr_user_rating) / no_corated

    def all_user_identical_rating_neighbourhoods(self, user_data):
        print('\nGenerating Identical Ratings based neighbourhoods For All Users')
        start_time = time.time()
        with open('out/neighbourhoods/neighbourhood_identical_ratings_based.csv', 'w') as f:
            for user in sorted(user_data, key=int):
                sys.stdout.write("\r" + str(round((int(user) / len(user_data)*100), 2)) + '%')
                sys.stdout.flush()
                # self.id_rat_neighbourhoods[user] = self.identical_rating_based_neighbourhood(user, user_data, -1)
                f.write(user)
                for sim_user in self.identical_rating_based_neighbourhood(user, user_data, -1):
                    f.write(',' + str(sim_user[0]) + ':' + str(sim_user[1]))
                f.write('\n')
            with open('out/neighbourhoods/neighbourhood_identical_ratings_based_run_time.csv', 'w') as f1:
                f1.write('run_time\n')
                f1.write(str(time.time() - start_time))
        print('\nIdentical Ratings based neighbourhoods run time:         ' + str(time.time() - start_time))
        print('Identical Ratings based Neighbourhoods For All Users Generated')
        pass
        return

    def all_user_cosine_distance_neighbourhoods(self, user_data, min_overlap):
        print('\nGenerating Cosine Distance based neighbourhood For All Users')
        start_time = time.time()
        with open('out/neighbourhoods/neighbourhood_cosine_distance_based.csv', 'w') as f:
            for user in sorted(user_data, key=int):
                sys.stdout.write("\r" + str(round((int(user) / len(user_data)*100), 2)) + '%')
                sys.stdout.flush()
                # self.cosine_neighbourhoods[user] = self.cosine_distance_neighbourhood(user, user_data, -1, 10)
                f.write(user)
                for sim_user in self.cosine_distance_neighbourhood(user, user_data, -1, min_overlap):
                    f.write(',' + str(sim_user[0]) + ':' + str(sim_user[1]))
                f.write('\n')

            with open('out/neighbourhoods/neighbourhood_cosine_distance_based_run_time_min_corated_' +
                              str(min_overlap) + '.csv', 'w') as f1:
                f1.write('min_overlap, run_time\n')
                f1.write(str(min_overlap) + ',' + str(time.time() - start_time))
        print('\nCosine Distance nased neighbourhoods run time:           ' + str(time.time() - start_time))
        print('Cosine Distance based Neighbourhoods For All Users Generated')

        # keeps track of neighbourhood min overlap 4 reopening the program, and neighbourhood size will always be known
        with open('out/save_data/cosine_nhood_min_overlap_save_data.txt', 'w') as f:
            f.write(str(min_overlap))
        return

    def all_user_mean_squared_difference_neighbourhoods(self, user_data, min_overlap):
        print('\nGenerating Mean Squared Difference based Neighbourhood For All Users')
        start_time = time.time()
        with open('out/neighbourhoods/neighbourhood_mean_squared_diff_based.csv', 'w') as f:
            for user in sorted(user_data, key=int):
                sys.stdout.write("\r" + str(round((int(user) / len(user_data)*100), 2)) + '%')
                sys.stdout.flush()
                # self.mean_squared_diff_neighbourhoods[user] = \
                #     self.mean_squared_differences_neighbourhood(user, user_data, -1, 10)
                f.write(user)
                for sim_user in self.mean_squared_differences_neighbourhood(user, user_data, -1, min_overlap):
                    f.write(',' + str(sim_user[0]) + ':' + str(sim_user[1]))
                f.write('\n')

            with open('out/neighbourhoods/neighbourhood_mean_squared_difference_based_run_time_min_corated_' +
                              str(min_overlap) + '.csv', 'w') as f1:
                f1.write('min_overlap, run_time\n')
                f1.write(str(min_overlap) + ',' + str(time.time() - start_time))
        print('\nMean Squared Difference Based Neighbourhood run time:   ' + str(time.time() - start_time))
        print('Mean Squared Difference based neighbourhoods For All Users Generated')

        # keeps track of neighbourhood min overlap 4 reopening the program, and neighbourhood size will always be known
        with open('out/save_data/msd_nhood_min_overlap_save_data.txt', 'w') as f:
            f.write(str(min_overlap))

        return

    # Week 5 Pearson Correlation Neighbourhood, done differently to the other neighbourhoods
    def all_user_pearson_correlation_neighbourhoods(self, user_data, min_overlap):
        print('\nGenerating Pearson Correlation based Neighbourhoods for all users')
        start_time = time.time()
        np.seterr(divide='ignore', invalid='ignore')
        users_mean_ratings = {}  # to be used in the pearson correlation coeffiecent formula
        correlation_dict = {}
        with open('out/general_statistics/user_stats.csv', 'r') as f:  # from week 1
            for line in f:
                line_split = line.split(',')
                users_mean_ratings[line_split[0]] = line_split[1]

        users_to_compare = user_data

        print('Pulling necessary data into dict')
        for user in sorted(user_data, key=int):  # for each user
            sys.stdout.write("\r" + str(round((int(user) / len(user_data) * 100), 2)) + '%')
            sys.stdout.flush()


            users_items = user_data.get(user)  # get their individual item ratings
            for comp_user in sorted(users_to_compare, key=int):  # loop through all users to compare each of them
                if user == comp_user:  # skip self comparison, would lead to p coeff of 1
                    continue
                else:
                    users_ratings_vector = []  # will be used as vectors along numpys methods for the formula
                    comp_users_ratings_vector = []

                    comp_users_items = users_to_compare.get(comp_user)  # current compared users items

                    for item in sorted(users_items, key=int):

                        corated_item = comp_users_items.get(item)

                        if corated_item is not None:  # if item is corated
                            users_ratings_vector.append(users_items.get(item)[0])
                            comp_users_ratings_vector.append(corated_item[0])

                    if len(users_ratings_vector) >= min_overlap:
                        # numerator = the sum of
                        numerator = 0
                        for i in range(0, len(users_ratings_vector)):
                            numerator += (
                                (float(users_ratings_vector[i]) - float(users_mean_ratings.get(user))) *
                                (float(comp_users_ratings_vector[i]) - (float(users_mean_ratings.get(comp_user))))
                            )

                        denominator_one = 0
                        denominator_two = 0
                        for i in range(0, len(users_ratings_vector)):
                            denominator_one += np.square(float(users_ratings_vector[i]) -
                                                         float(users_mean_ratings.get(user)))

                            denominator_two += np.square(float(comp_users_ratings_vector[i]) -
                                                         float(users_mean_ratings.get(comp_user)))

                        denominator_one = np.sqrt(denominator_one)
                        denominator_two = np.sqrt(denominator_two)
                        denominator = denominator_one * denominator_two

                        pearson_correlation_coefficient = np.divide(numerator, denominator)

                        if correlation_dict.get(user) is None:
                            correlation_dict[user] = {comp_user: pearson_correlation_coefficient}
                        else:
                            correlation_dict.get(user).update({comp_user: pearson_correlation_coefficient})
                        # f.write(',' + comp_user + ':' + str(pearson_correlation_coefficient))
                        # f.write(user + ',' + comp_user + ',' + str(pearson_correlation_coefficient) + '\n')

        with open('out/neighbourhoods/neighbourhood_pearson_correlation_based.csv', 'w') as f:
            print('\nsorting dict and writing to file:')
            i = 1
            for user_2 in sorted(correlation_dict, key=int):
                sys.stdout.write("\r" + str(round((i / len(correlation_dict) * 100), 2)) + '%')
                sys.stdout.flush()
                i += 1
                f.write(user_2)
                users_unsorted_neighbours = correlation_dict.get(user_2)

                sorted_for_best_correlation = sorted(users_unsorted_neighbours.items(), key=lambda x:x[1],
                                                     reverse=True)

                for neighbour in sorted_for_best_correlation:

                    # neighbour is a tuple of user_id,pearson_coefficient
                    f.write(',' + neighbour[0] + ':' + str(neighbour[1]))

                f.write('\n')

        run_time = time.time() - start_time
        with open('out/neighbourhoods/neighbourhood_pearson_correlation_based_run_time.csv', 'w') as f1:
            f1.write('min_overlap, run_time\n')
            f1.write(str(min_overlap) + ',' + str(run_time))

        with open('out/save_data/pearson_nhood_min_overlap_save_data.txt', 'w') as f:
            f.write(str(min_overlap))

        print('Pearson Correlation based neighbourhoods run time:\t\t' + str(run_time))
        print('\nPearson Correlation based Neighbourhoods Generated')
