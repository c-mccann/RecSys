# Carl McCann   12508463    Recommender System  Week 1

class DataHandler:
    def __init__(self):
        self.user_item_rating_dict = {}
        self.item_user_rating_dict = {}
        # in the initial submission the data structures were returned and saved in Recommender_System.py, now they are
        # instance variables of the class DataHandler


    # deals with the movielens data, and breaks it up into data structures (in the form
    # {outer_key: {inner_key: [data1, data2]}} ) to be used later on in the project
    def csv_handler(self, file_name):
        print('Creating Data Structures')
        with open(file_name, 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                data_list = line.split(",")

                if self.user_item_rating_dict.get(data_list[0]) is None:
                    self.user_item_rating_dict[data_list[0]] = {data_list[1]: [data_list[2], data_list[3]]}
                else:
                    self.user_item_rating_dict[data_list[0]].update({data_list[1]: [data_list[2], data_list[3]]})

                if self.item_user_rating_dict.get(data_list[1]) is None:
                    self.item_user_rating_dict[data_list[1]] = {data_list[0]: [data_list[2], data_list[3]]}
                else:
                    self.item_user_rating_dict[data_list[1]].update({data_list[0]: [data_list[2], data_list[3]]})

        print('Data Structures Created\n')
        return