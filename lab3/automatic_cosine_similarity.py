import os
import argparse
#Importation of the modified TF-IDF calculator.
import TFIDFMod as TFIDF


#Obtains the paths of all the files located inside the selected folders.
def generate_files_list(path):
    """
    Generates a list of all the files inside a path
    :param path:
    :return:
    """
    if path[-1] == '/':
        path = path[:-1]

    lfiles = []

    for lf in os.walk(path):
        if lf[2]:
            for f in lf[2]:
                lfiles.append(lf[0] + '/' + f)
    return lfiles

#Computes the  average cosine similarity between a file and all the files from
# a selected folder.

def mean_file_group(file,group,index):
    aux_mean = 0
    for f in group:
        aux_mean += TFIDF.obtain_value(index,file,f)
    return aux_mean/len(group)

#Computes the  average cosine similarity between the files from
# a selected folder.

def mean_inner_group_similarity(lfiles,index):
    mean = 0
    i = 0
    while i < len(lfiles) - 1:
        mean += mean_file_group(lfiles[i],lfiles[i+1:],index)*len(lfiles[i+1:])
        i+=1
    return mean/((len(lfiles)*(len(lfiles) - 1))/2)

"""
Computes the average cosine similarity between the files from one folder and
the files from antoher folder. The comparision is performed selecting a file
 orm one folder and comparing its average similarity to the other folder.
"""
def mean_between_groups(folder1,folder2,index):
    mean = 0
    for f in folder1:
        mean += mean_file_group(f,folder2,index)
    return mean/len(folder1)

def main():

    print("Welcome to the Automic Cosine Similarity Calculator!","\n")

    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index to search')
    parser.add_argument('--folders', default=None, required=True, nargs=2, help='Paths of the folders to compare')
    parser.add_argument('--num_files', default=None, required=True, help='Number of files from the folders to compare')

    args = parser.parse_args()

    index = args.index

    folder1 = args.folders[0]
    folder2 = args.folders[1]

    n = int(args.num_files)

    lf1 = generate_files_list(folder1)
    lf2 = generate_files_list(folder2)

    print("Computing similarity group 1...","\n")
    m1 = mean_inner_group_similarity(lf1[:n],index)
    print("Mean inner group similiarity folder 1:",m1,"\n")
    print("Computing similarity group 2...","\n")
    m2 = mean_inner_group_similarity(lf2[:n],index)
    print("Mean inner group similiarity folder 2:",m2,"\n")
    print("Computiig similarity between groups...","\n")
    m1_2 = mean_between_groups(lf1[:n],lf2[:n],index)
    print("Mean between groups:",m1_2)

main()
