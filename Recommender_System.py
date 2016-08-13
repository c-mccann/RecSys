# Carl McCann   12508463    Recommender System  Week 4
# Takes the idea of the original Recommender_System.py file and makes it into a menu system

from General_Statistics import GeneralStatistics
from Data_Handler import DataHandler
from Simple_Prediction import SimplePrediction
from Neighbourhoods import Neighbourhoods
from Prediction import Prediction
from Extras import Extras
from Graphing import Graphing
from Correlation import Correlation

DH = DataHandler()              # handles the movielens data, processing it, and storing it
GS = GeneralStatistics()        # creates the general stats asked for in week 1 to understand the data
SP = SimplePrediction()         # week 2 doesnt use neighbourhoods, uses a simple overall average as baseline prediction
NS = Neighbourhoods()           # Week 3, 4 + extra, generates csvs of sim users based on different similarity metrics
P = Prediction()                # prediction (week 3 and 5), generates predictions, graphs their accuracy and coverge
                                # maybe graphing and coverage accuracy methods should have their own class
E = Extras()                    # extras methods i wrote such as building matrices etc.
G = Graphing()                  # highly specific code that'll break easily, just for graphing exactly what i tested
C = Correlation()               # houses code for pearson correlation, to be used in reznick's prediction formula

filename = 'res/MovieLens-100k-dataset.csv'

DH.csv_handler(filename)        # creates the two data structures i use

end_game = False                # keeps the menu looping until quit is explicitly stated
current_min_overlap= -1;        # min overlap can't be -1, set this way if the save_data doesn't exist
                                # it always should though to indicate what type of neighbourhoods we are working with

print('\nRecommender System')
print('\nThe User/Item data has been loaded into data structures')

while not end_game:             # starts the menu loop
    print('\nTo see statistics from week 1 please enter:                  1')
    print('To see simple predictions from week 2 please enter:          2')
    print('To use Mean Squared Difference predictions please enter:     3')
    print('To use Cosine Similarity predictions please enter:           4')
    print('To use the Resnick Prediction Method please enter:           5')
    print('To Generate New Neighbourhoods please enter:                 N')
    print('To see the experimental graphing class please enter:         G')
    print('To see extra features please enter:                          E')
    user_choice = input('To Quit the program please enter:                            Q\n')

    if user_choice.upper() == 'Q':              # QUIT
        end_game = True
        print('\nThanks for using the Recommender System, Goodbye.')

    elif user_choice.upper() == 'N':            # Neighbourhoods
        print('Please enter nothing to return to main menu: ')
        print('all is the safest thing to choose as it saves min corated data properly and aligns all')
        print('neighbourhoods better for testing')
        a = input('which Neighbourhood would you like to regenerate [identical/msd/cosine/pearson/all]: ')

        if a == 'all':

            a2 = input("What is your desired minimum overlap between neighbours: ")
            with open('out/minimum_overlap_save_data.txt', 'w') as f:
                f.write(a2)
            NS.all_user_identical_rating_neighbourhoods(DH.user_item_rating_dict)
            NS.all_user_mean_squared_difference_neighbourhoods(DH.user_item_rating_dict, int(a2))
            NS.all_user_cosine_distance_neighbourhoods(DH.user_item_rating_dict, int(a2))
            NS.all_user_pearson_correlation_neighbourhoods(DH.user_item_rating_dict, int(a2))

        if a == 'identical':
            NS.all_user_identical_rating_neighbourhoods(DH.user_item_rating_dict)
        if a == 'msd':
            a2 = input("What is your desired minimum overlap between neighbours: ")
            with open('out/minimum_overlap_save_data.txt', 'w') as f:
                f.write(a2)
            NS.all_user_mean_squared_difference_neighbourhoods(DH.user_item_rating_dict, int(a2))
        if a == 'cosine':
            a2 = input("What is your desired minimum overlap between neighbours: ")
            with open('out/minimum_overlap_save_data.txt', 'w') as f:
                f.write(a2)
            NS.all_user_cosine_distance_neighbourhoods(DH.user_item_rating_dict, int(a2))
        if a == 'pearson':
            a2 = input("What is your desired minimum overlap between neighbours: ")
            with open('out/minimum_overlap_save_data.txt', 'w') as f:
                f.write(a2)
            NS.all_user_pearson_correlation_neighbourhoods(DH.user_item_rating_dict, int(a2))

    elif user_choice == '1':                    # General Statistics
        print('Please enter nothing to return to main menu: ')
        print('\nTo see General statistics please enter:      G')
        print('To see user statistics please enter:         U')
        print('To see item statistics please enter:         I')
        a = input('To see rating statistics please enter:       R\n')

        if a.upper() == 'G':
            GS.general_statistics(DH.user_item_rating_dict, DH.item_user_rating_dict)
        if a.upper() == 'U':
            GS.user_stats(DH.user_item_rating_dict)
        if a.upper() == 'I':
            GS.item_stats(DH.item_user_rating_dict)
        if a.upper() == 'R':
            GS.rating_class_totals(DH.user_item_rating_dict)

    elif user_choice == '2':                    # Simple Prediction
        print('Please enter nothing to return to main menu: ')
        print('To See a specific user-item prediction please enter:                     S')
        print('To create a predictions csv and display its statistics please enter:     P')
        print('To run a series of L1O Tests please enter:                               L')
        a = input('To test the rmse method please enter:                                    R\n')

        if a.upper() == 'S':
            uid = input('please enter a user number: ')
            iid = input('please enter an item number: ')
            SP.mean_item_rating(uid, iid, DH.item_user_rating_dict, True)

        if a.upper() == 'P':
            SP.rmse_csv_maker(DH.user_item_rating_dict, DH.item_user_rating_dict)
            SP.rmse_calc()
            SP.coverage()

        if a.upper() == 'L':
            a2 = input('Please specify number of runs: ')
            SP.l1o_run_time(DH.user_item_rating_dict, DH.item_user_rating_dict, int(a2))

        if a.upper() == 'R':
            a1 = input('Please enter rating 1: ')
            a2 = input('Please enter rating 2: ')
            print(str(SP.rmse(float(a1), float(a2))))

    elif user_choice == '3':                    # Mean Squared Difference Neighbourhoods Prediction
        print('Please enter nothing to return to main menu: ')
        print('To See a specific user-item prediction please enter:                     S')
        a1 = input('To generate overall statistics please enter:                             O\n')

        if a1.upper() == 'S':
            user = input('Please input a user id: ')
            item = input('Please input an item id: ')
            n_size = input('What Neighbourhood size: ')
            P.user_item_prediction(user, item, 'msd', n_size, DH.user_item_rating_dict)

        if a1.upper() == 'O':
            print('What neighbourhood sizes would you like to use:')
            a1 = input('please enter in the format: int,int,int,...')
            n_sizes = a1.split(',')
            with open('out/save_data/msd_nhood_min_overlap_save_data.txt', 'r') as f:
                m_corated = int(f.readline())

            P.generate_graphing_data(DH.user_item_rating_dict, n_sizes, m_corated, 'msd')
            P.plot_differences(n_sizes, m_corated, 'msd')
            P.plot_coverage(n_sizes, m_corated, 'msd')

    elif user_choice == '4':                    # Cosine Similarity Neighbourhoods Prediction
        print('Please enter nothing to return to main menu: ')
        print('To See a specific user-item prediction please enter:                     S')
        a1 = input('To generate overall statistics please enter:                             O\n')

        if a1.upper() == 'S':
            user = input('Please input a user id: ')
            item = input('Please input an item id: ')
            n_size = input('What Neighbourhood size: ')
            P.user_item_prediction(user, item, 'cosine', n_size, DH.user_item_rating_dict)

        if a1.upper() == 'O':
            print('What neighbourhood sizes would you like to use:')
            a1 = input('please enter in the format: int,int,int,...')
            n_sizes = a1.split(',')
            with open('out/save_data/cosine_nhood_min_overlap_save_data.txt', 'r') as f:
                m_corated = int(f.readline())

            P.generate_graphing_data(DH.user_item_rating_dict, n_sizes, m_corated, 'cosine')
            P.plot_differences(n_sizes, m_corated, 'cosine')
            P.plot_coverage(n_sizes, m_corated, 'cosine')

    elif user_choice == '5':                    # Week 5 submission
        print('To generate user-user pearson correlations please enter:     P')
        a1 = input('To use the Resnick prediction method please enter:           R\n')
        if a1.upper() == 'P':
            C.pearson_correlation_file_output(DH.user_item_rating_dict)
        if a1.upper() == 'R':
            print('What neighbourhood sizes would you like to use:')
            n_sizes = input('please enter in the format: int,int,int,...')
            with open('out/save_data/pearson_nhood_min_overlap_save_data.txt', 'r') as f:
                m_corated = int(f.readline())
                print(m_corated)
            print('Only fully functional for pearson neighbourhood, other options may crash program')
            n_type = input('which neighbourhood type would you like to use? [msd/cos/id/pearson]: ')

            if n_type.upper() == 'PEARSON':
                print(m_corated)
                P.generate_resnick_graphing_data(DH.user_item_rating_dict, DH.item_user_rating_dict, n_sizes, m_corated)


    elif user_choice.upper() == 'G':            # Graphing for report file
        print('These methods were written solely to plot the three neighbourhoods from week 3, 4 and 5 with each other,')
        print('at the neighbourhood sizes i tested. The Code isn\'t very nice, but it works for this purpose alone')
        G = Graphing()
        G.plot_coverage([10,20,30,40,50,60,70,80,90,100], 5,'temp')
        G.plot_rmses([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 5, 'temp')
        G.plot_coverage([10,20,30,40,50,60,70,80,90,100], 10,'temp')
        G.plot_rmses([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 10, 'temp')
        G.plot_coverage([10,20,30,40,50,60,70,80,90,100], 20,'temp')
        G.plot_rmses([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 20, 'temp')



    elif user_choice.upper() == 'E':            # Extras
        print('Please enter nothing to return to main menu: ')
        print('The Identical Neighbourhood prediction does not work as of yet, as its measure of similarity')
        print('between users is a count of identical ratings, rather than a distance, or similarity measure')
        print('To use my own identical ratings neighbourhood to generate predictions please enter:             I')
        print('These methods output data that in some text editors appear unintelligible bar PyCharm')
        print('To print a user-item matrix please enter:                                                       M')
        a1 = input('To print the same matrix, with empty entries filled with simple predictions please enter:       E\n')

        if a1.upper() == 'I':
            print('Please enter nothing to return to main menu: ')
            print('To See a specific user-item prediction please enter:                     S')
            choice = input('To generate overall statistics please enter:                             O\n')

            if choice.upper() == 'S':
                user = input('Please input a user id: ')
                item = input('Please input an item id: ')
                P.user_item_prediction(user, item, 'identical', -1, DH.user_item_rating_dict)

            if choice.upper() == 'O':
                P.generate_graphing_data(DH.user_item_rating_dict, n_sizes, -1, 'identical')
                P.plot_differences(n_sizes, -1, 'identical')
                P.plot_coverage(n_sizes, -1, 'identical')

        if a1.upper() == 'M':
            E.matrix_builder(DH.user_item_rating_dict, DH.item_user_rating_dict)
        if a1.upper() == 'E':
            E.estimated_matrix_builder(DH.user_item_rating_dict, DH.item_user_rating_dict)


    else:
        print('Unrecognised input, please try again.\n')
