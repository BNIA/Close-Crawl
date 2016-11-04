from re import compile, IGNORECASE

file_name = "2015_Raw_Data_Court_FF.txt"

NAME_ADDR_PAT = compile(r'(?<=[^\W\d])(\s+(?=\d+))')

if __name__ == '__main__':

    dataset = {}

    dates = []
    case_nums = []
    titles = []
    addresses = []

    works = 0

    with open(file_name, 'r') as input_file:
        for i, j in enumerate(input_file):
            if i < 5:
                dates.append(j.split()[0])
                case_nums.append(j.split()[1])
                print NAME_ADDR_PAT.findall(j)
            dataset['date'] = dates
            dataset['case_nums'] = case_nums

    print dataset
