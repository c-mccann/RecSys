# Carl McCann   12508463    Recommender System  extra methods

import time
import sys
from Simple_Prediction import SimplePrediction

class Extras:
    def __init__(self):
        pass

    # extra function to create a user-item matrix
    def matrix_builder(self, users, items):
        print('Creating Matrix')
        formatting = '{0:0=3d}'
        overline_counter = 0
        rated = 0
        non_rated = 0

        with open('out/extras/ratings_matrix.txt', 'w') as f:
            f.write('\t\tItems -->\n\t')
            for item in sorted(items, key=int):                 # writing y values
                f.write("\t" + item)
                overline_counter += len(str('\t' + item))  # tab is 4 spaces, so \t + 3 gives proper size

            f.write('\n\t\t')
            for item in sorted(items, key=int):
                for i in range(0, len(item)):
                    f.write('‾')
                f.write('\t')

            f.write('\n\n')
            for user in sorted(users, key=int):                              # user by user now
                f.write(str(formatting.format(int(user))) + '|\t')                           # writing x value

                for j in range(1, len(items)+1):
                    spacing = '\t'
                    if j > 999:
                        spacing = '\t\t'
                    temp_dict = items.get(str(j))
                    temp_dict2 = temp_dict.get(user, None)
                    if temp_dict2 is not None:
                        f.write(temp_dict2[0] + spacing)
                        rated += 1
                    else:
                        f.write('-' + spacing)
                        non_rated += 1

                f.write('\n\n')

        with open('out/extras/ratings_density_metrics.txt', 'w') as f:
            f.write('Rated:                   ' + str(rated) + '\n')
            f.write('Non-Rated:               ' + str(non_rated) + '\n')
            f.write('Total Possible Ratings:  ' + str(rated + non_rated) + '\n')
            f.write('Ratio (Rated vs Non):    ' + str(rated/non_rated) + '\n')
            f.write('Density Metric:          ' + str(rated/(rated + non_rated)) + '\n')

        print('Matrix Created\n')
        return

    # extra method (expands upon the matrix builder from week 1) which creates a visual representation of the matrix of
    # user-item pairs, filled with actual ratings where possible and simple predictions where not
    def estimated_matrix_builder(self, users, items):
        print('\nCreating Estimated Matrix')
        formatting = '{0:0=3d}'
        overline_counter = 0
        SP = SimplePrediction()

        start_time = time.time()
        with open('out/extras/estimated_ratings_matrix.txt', 'w') as f:
            f.write('\t\tItems -->\n\t')
            for item in sorted(items, key=int):                 # writing y values
                f.write("\t" + item)
                overline_counter += len(str('\t' + item))  # tab is 4 spaces, so \t + 3 gives proper size

            f.write('\n\t\t')
            for item in sorted(items, key=int):
                for i in range(0, len(item)):
                    f.write('‾')
                f.write('\t')

            f.write('\n\n')
            for user in sorted(users, key=int):                              # user by user now
                f.write(str(formatting.format(int(user))) + '|\t')                           # writing x value
                sys.stdout.write("\r" + str(round((int(user) / len(users)*100), 2)) + '%')
                sys.stdout.flush()
                for j in range(1, len(items)+1):
                    spacing = '\t'
                    if j > 999:
                        spacing = '\t\t'
                    temp_dict = items.get(str(j))
                    temp_dict2 = temp_dict.get(user, None)
                    if temp_dict2 is not None:
                        f.write(temp_dict2[0] + spacing)
                    else:
                        x = SP.mean_item_rating(str(user), str(j), items, False)
                        f.write(str(round(x, 1)) + spacing)

                f.write('\n\n')
            run_time = time.time() - start_time

        with open('out/extras/est_rat_matrix_time.txt', 'w') as f:
            f.write('Estimated Ratings Matrix Creation Time:\t' + str(round(run_time, 2)) + 's\n')

        print('\nEstimated Matrix Created')
