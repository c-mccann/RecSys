To run the program run the file Recommender_System.py. Upon displaying graphs, closing these windows will resume
the running of the program. Instructions are provided in the terminal, and they should be easy to follow.

The program has been restructured to loop for easier navigation, with the option to quit, or explore other parts
of the system. Changes can be seen in readme_etc/CHANGES.txt in the project folder.

Extras:

*******   Week 1   *******
the method matrix_builder() in class Extras in Extras.py
is a discretionary function that outputs a user-item matrix, while also calculating ratings density metrics.
This mandatory part of the assignment is done in the general_statistics() function, in a different way, this just
highlights another approach, while building a visual representation of the data. The formatting seems to go haywire
in text editors other than PyCharm Comment it out if you wish.

*******   Week 2   *******
the method estimated_matrix_builder() in class Extras in  Extras.py
is an extra method that builds upon Week1's matrix_builder(), which instead of inserting '-' where no rating has been
made, it inserts a prediction based upon other users ratings of the item. The formatting seems to go haywire in text
editors other than PyCharm. It takes approx. 200 seconds to run. Comment it out if you wish.

*******   Week 3   *******
the methods identical_rating_based_neighbourhood(), cosine_distance_neighbourhood(), cosine_distance(),
all_user_identical_rating_neighbourhoods() and all_user_cosine_distance_neighbourhoods()
in class Neighbourhoods in Neighbourhoods.py
These extra methods generate two extra neighbourhoods, which i made for comparison. I don't generate predictions or
graphs from them. They are commented out in Recommender_System.py but you can run them if you wish.

*******   Week 4   *******
identical_ratings_neighbourhoods now outputs graphs of coverage and avg. prediction difference



