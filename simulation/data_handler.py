import json
import random

def get_temp_processed():
    filename = "temp-seq/temp_small.json"
    #filename = "temp-seq/temp_file_processed.json"     # uncomment to run big experiment
    with open(filename) as f_in:
        file = json.load(f_in)
    logger = open("used_seq_data" + ".txt", "a")
    for temp_p in file:
        print("P: " + str(temp_p))
        logger.write("P: " + str(temp_p)+"\n")
        for sample in file[temp_p]:
            distinct_items = set()
            for r in file[temp_p][sample]:
                distinct_items.add(file[temp_p][sample][r])
            print("Sample " + str(sample) + ", size: " + str(len(file[temp_p][sample]))+ ", n_items = " + str(len(distinct_items)))
            logger.write("Sample " + str(sample) + ", size: " + str(len(file[temp_p][sample]))+
                         ", n_items = " + str(len(distinct_items)) + "\n")
    return file

def get_fb_data():
    filename = "real-seq/fb_single/fb_clusterB_timestamp_srcip_dstip.csv_single.json"       # smaller test-datasest
    with open(filename) as f_in:
        file = json.load(f_in)
    return file

def get_temp_original():
    filename = "temp-seq/temp_small.json"
    #filename = "q2_seq.json"       # omitted from repository because of its size
    with open(filename) as f_in:
        file = json.load(f_in)
    return file

def count_nodes(set):
    """returns counter: the set of distinct nodes (hosts) in the sequence"""
    counter = dict()
    for item in set:
        if item in counter:
            counter[item] += 1
        else:
            counter[item] = 0
    return counter
    
def sorted_nodes_occur(x):
    counter = dict()
    for item in x:
        if item in counter:
            counter[item] += 1
        else:
            counter[item] = 1
    list_of_tuples = sorted(counter.items(), key=lambda x: x[1])
    return list_of_tuples
    
def pre_process_temp_seq():
    """
    Make sure there are enough hosts (hard-coded number below) in sequence
    """
    dataset = get_temp_original()
    n_hosts = 131       # changed to 65535 for big experiment (original file is omitted)
    new_dataset = {}
    logger = open("preprocess_seq" + ".txt", "a")
    for temp_p in dataset:
        new_dataset[temp_p] = {}
        print("Temp p: " + str(temp_p))
        logger.write("Temp p: " + str(temp_p) + "\n")
        for sample in dataset[temp_p]:
            distinct_items = set()
            for r in dataset[temp_p][sample]:
                distinct_items.add(r)
            new_dataset[temp_p][sample] = {}
            if len(distinct_items) == n_hosts:  # nothing to do
                for i in range(0, len(dataset[temp_p][sample])):
                    new_dataset[temp_p][sample][i] = dataset[temp_p][sample][i]
            else:
                print("analyzing sample: " + str(sample))
                logger.write("analyzing sample: " + str(sample) + "\n")
                appearing_items = set()
                double_appearing_items = set()
                curr_item = dataset[temp_p][sample][0]
                for i in range(0, len(dataset[temp_p][sample]) - 1):  # stop at second-last request
                    if curr_item in appearing_items:  # this means that it appears in 2 subsequences
                        double_appearing_items.add(curr_item)
                    if curr_item != dataset[temp_p][sample][i + 1]:  # add to candidates once we switch to another item
                        appearing_items.add(curr_item)
                    curr_item = dataset[temp_p][sample][i + 1]
                print("Found " + str(len(double_appearing_items)) + " items that appear in 2 subsequences")
                logger.write(
                    "Found " + str(len(double_appearing_items)) + " items that appear in 2 subsequences" + "\n")

                # now create new sequence based on the missing items
                missing_items = n_hosts - len(distinct_items)
                logger.write("Replacing " + str(missing_items) + " items" + "\n")
                random_sample = set()
                while missing_items:
                    tentative = random.randint(0, n_hosts)
                    if tentative not in distinct_items and \
                            tentative not in random_sample:  # get a random sample of items not in sequence
                        random_sample.add(tentative)
                        missing_items -= 1
                logger.write("Picked " + str(len(random_sample)) + " random items" + "\n")
                already_replaced_items = set()  # keep track of what items have been replaced already
                i = 0
                while i < len(dataset[temp_p][sample]):
                    if random_sample and dataset[temp_p][sample][i] in double_appearing_items \
                            and dataset[temp_p][sample][i] not in already_replaced_items:
                        curr_req = dataset[temp_p][sample][i]
                        already_replaced_items.add(curr_req)
                        replacement = random_sample.pop()
                        new_dataset[temp_p][sample][i] = replacement
                        while dataset[temp_p][sample][i + 1] == curr_req:
                            i += 1
                            new_dataset[temp_p][sample][i] = replacement
                        logger.write("Replaced " + str(curr_req) + " with " + str(replacement) + "\n")
                    else:
                        new_dataset[temp_p][sample][i] = dataset[temp_p][sample][i]
                    i += 1
                test = set()
                for r in new_dataset[temp_p][sample]:
                    test.add(new_dataset[temp_p][sample][r])
                logger.write("Test, sample" + str(sample) + " now has " + str(len(test)) + " items and " +
                             str(len(new_dataset[temp_p][sample])) + " requests \n")
    with open("temp_file_processed.json", "w") as handle:
        json.dump(new_dataset, handle)
    logger.close()