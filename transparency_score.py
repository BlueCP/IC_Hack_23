import csv

def transparency_score_for_brands():
    dict = {}
    with open('Fashion Transparency Index 2020 dataset_Final.csv', 'r') as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            if (i < 2 or len(row[0]) > 10):
                i += 1
                continue
            i += 1

            row_sum = 0
            for i in range(1, len(row)):
                try:
                    row_sum += float(row[i])
                except:
                    continue
            avg = row_sum / (len(row) - 1)

            dict[row[0]] = avg

    dict.pop('')

    return dict


    #sorted_dict = sorted(dict.items(), key=lambda x:x[1])

    #print(sorted_dict)

#print(transparency_score_for_brands())
