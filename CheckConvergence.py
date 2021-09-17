
#after run kernel
#after run the perfect optimization

# read the kernel profit return
# read the perfect optimization return
# compare their result
class CheckConvergence():
    def __init__(self):
        self.list_numerical = None
        self.list_perfect = None
        self.list_accuracy = None

    def main(self):
        self.read_two_profit(doc_1, doc_2)
        self.compare_profit()
        self.csv_return()


    def read_two_profit(self, doc_1, doc_2):
        '''
        :param doc_1: csv, numerical_profit
        :param doc_2: csv, perfect_profit
        :return: two lists
        '''
        #这里的读取还需要改进
        file = open("sample.csv", "r")
        csv_reader = csv.reader(file)
        lists_from_csv = []
        for row in csv_reader:
            lists_from_csv. append(row)

        self.list_numerical = list[1]
        self.list_perfect = list[2]


    def compare_profit(self):
        '''
        :param numerical_profit: profit from the algorithm
        :param perfect_profit: perfect perfect optimization return
        :return: list:  accuracy
        '''
        len = len(self.list_numerical)
        curr_sum_numerical = 0
        curr_sum_perfect = 0
        ret = []

        for i in range(len):
            curr_sum_numerical += self.list_numerical[i]
            curr_sum_perfect += self.list_perfect[i]
            curr_precise = abs(curr_sum_perfect - curr_sum_numerical)/ curr_sum_perfect
            ret.append(curr_precise)

        self.list_accuracy = ret


    def csv_return(self):
        '''
        :return: csv, have added the list of accuracy
        '''
        dict = {'numerical_profit': self.list_numerical, 'perfect_profit': self.list_perfect, 'accuracy': self.list_accuracy}
        df = pd.DataFrame(dict)
        df.to_csv('test.csv')

