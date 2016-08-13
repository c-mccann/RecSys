# Carl McCann   12508463    Recommender System  Week 5

import numpy as np
import sys


class Correlation:


    def __init__(self):
        pass

    def pearson_correlation_file_output(self, users):
        np.seterr(divide='ignore', invalid='ignore')
        users_mean_ratings = {}                      # to be used in the pearson correlation coeffiecent formula
        with open('out/general_statistics/user_stats.csv', 'r') as f:       # from week 1
            for line in f:
                line_split = line.split(',')
                users_mean_ratings[line_split[0]] = line_split[1]

        with open('out/correlation/users_pearson_correlation.csv', 'w') as f:

            users_to_compare = users

            for user in sorted(users, key=int):             # for each user
                sys.stdout.write("\r" + str(round((int(user) / len(users) * 100), 2)) + '%')
                sys.stdout.flush()

                users_items = users.get(user)              # get their individual item ratings
                for comp_user in sorted(users_to_compare, key=int): # loop through all users to compare each of them
                    if user == comp_user:                           # skip self comparison, would lead to p coeff of 1
                        continue
                    else:
                        users_ratings_vector = []  # will be used as vectors along numpys methods for the formula
                        comp_users_ratings_vector = []

                        comp_users_items = users_to_compare.get(comp_user) # current compared users items

                        for item in sorted(users_items, key=int):

                            corated_item = comp_users_items.get(item)
                            if corated_item is not None:                       # if item is corated
                                users_ratings_vector.append(users_items.get(item)[0])
                                comp_users_ratings_vector.append(corated_item[0])


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
                        f.write(user + ',' + comp_user + ',' + str(pearson_correlation_coefficient) + '\n')




