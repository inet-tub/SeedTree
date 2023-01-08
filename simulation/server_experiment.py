
from pushdown.randomPush import *
from data_handler import get_temp_processed, get_fb_data
from pushdown.static_offline import static_offline

class server_experiment():
    def __init__(self):
        pass
    
    def run_fb_exp_diff_c(self):
        """ Run experiment on temporal data
        for different values of c and all the temporal params p
        f = 0.5 set as default ( in method set_c(c) ) """
        dataset = get_fb_data()
        c_params = [2, 4, 6, 8, 10, 12, 14, 16]
        logger2 = open("results/f-0.5-results_detail_fb+obl.txt", "a")
        for c in c_params:
            logger2.write("\nRunning for c = " + str(c) + "\n")
            for data in dataset:
                n_simulations = 0
                logger2.write(f"\nRunning for {data}")
                for sample in dataset[data]:
                    for trace in dataset[data][sample]:
                        distinct_items = set()
                        n_simulations += 1
                        sum_cost_algo = 0
                        for i in range(0,len(dataset[data][sample][trace])): #in dataset[data][sample][trace]:
                            #print(dataset[data][sample][trace])
                            distinct_items.add(dataset[data][sample][trace][i])

                        print(distinct_items)
                        on_tree = CompleteTree()
                        obl_tree = CompleteTree()
                        for t in [on_tree, obl_tree]:
                            t.set_c(c)
                            t.initialize_servers(len(distinct_items))

                        # set full initial occupation for obl
                        obl_tree.initial_occupation = c

                        print("inserting in on tree")
                        # insert for on_tree
                        dist_items_list = list(distinct_items)
                        random.shuffle(dist_items_list)
                        for item in dist_items_list:
                            on_tree.insert(item)

                        print("inserting in obl tree")
                        # insert in obl_tree and opt_tree
                        random.shuffle(dist_items_list)
                        for item in dist_items_list:  # different order as above
                            obl_tree.insert(item)

                        if c == 1:
                            algo = randomPush(on_tree, single_capacity = True)
                        else:
                            algo = randomPush(on_tree)
                        acc_obl = static_offline(obl_tree)
                        #print_tree(ct1.root)
                        for i in range(0,len(dataset[data][sample][trace])):#for r in dataset[data][sample][trace]:
                            algo.access(dataset[data][sample][trace][i])
                            acc_obl.access(dataset[data][sample][trace][i])
                        print("Total items: " + str(len(distinct_items)))
                        print("Total requests: " + str(algo.n_accesses))
                        print("ALGO: Access cost: " + str(algo.access_cost))
                        print("ALGO: Moving cost: " + str(algo.moves))
                        print("ALGO: Reconfig cost: " + str(algo.reconfig))
                        print("OBL: Access cost: " + str(acc_obl.access_cost))
                        logger2.write("Total items: " + str(len(distinct_items))+ "\n")
                        logger2.write("Total requests: " + str(algo.n_accesses)+ "\n")
                        logger2.write("ALGO: Reconfig cost: " + str(algo.moves + algo.reconfig) + "\n")
                        sum_cost_algo += (algo.access_cost + algo.moves + algo.reconfig)
                        logger2.write("ALGO: Total cost: " + str(sum_cost_algo) + "\n")
                        logger2.write("ALGO: Access cost: " + str(algo.access_cost) + "\n")
                        logger2.write("OBL: Access cost: " + str(acc_obl.access_cost) + "\n")
                        print("")
        logger2.close()
 
    def run_fb_exp_for_c(self, c):
        """
        run experiment on temporal data for different values of f (initial_occupancy)
        """
        if c == 12:
            f_params = [10, 9, 8, 6, 4, 3, 2]
        else:
            raise Exception("Missing definition of f-params for this 'c'")
        dataset = get_fb_data()
        logger2 = open("results/c_"+str(c)+"-results_detail_fb+obl.txt", "a")
        for f in f_params:
            logger2.write("\nRunning for f = " + str(f/c) + "\n")
            for data in dataset:
                n_simulations = 0
                for sample in dataset[data]:
                    for trace in dataset[data][sample]:
                        distinct_items = set()
                        n_simulations += 1
                        sum_cost_algo = 0
                        #print(len(dataset[data][sample][trace]))
                        for i in range(0,len(dataset[data][sample][trace])): #in dataset[data][sample][trace]:
                            distinct_items.add(dataset[data][sample][trace][i])
                        #logger.write((", n_items" + str(sample) + ": " + str(len(distinct_items))))
                        on_tree = CompleteTree()
                        obl_tree = CompleteTree()
                        on_tree.set_c_set_f(c=c, f=f)
                        for t in [on_tree, obl_tree]:
                            t.set_c(c)
                            t.initialize_servers(len(distinct_items))
                            # set full initial occupation for obl
                        obl_tree.initial_occupation = c

                        print("inserting in on tree")
                        # insert for on_tree
                        dist_items_list = list(distinct_items)
                        random.shuffle(dist_items_list)
                        for item in dist_items_list:
                            on_tree.insert(item)

                        print("inserting in obl tree")
                        # insert in obl_tree and opt_tree
                        random.shuffle(dist_items_list)
                        for item in dist_items_list:  # different order as above
                            obl_tree.insert(item)
                        if c == 1:
                            algo = randomPush(on_tree, single_capacity=True)
                        else:
                            algo = randomPush(on_tree)
                        acc_obl = static_offline(obl_tree)
                        for i in range(0,len(dataset[data][sample][trace])):#for r in dataset[data][sample][trace]:
                            algo.access(dataset[data][sample][trace][i])
                            acc_obl.access(dataset[data][sample][trace][i])

                        print("Total items: " + str(len(distinct_items)))
                        print("Total requests: " + str(algo.n_accesses))
                        print("Access cost: " + str(algo.access_cost))
                        print("Moving cost: " + str(algo.moves))
                        print("Reconfig cost: " + str(algo.reconfig))
                        logger2.write("Total items: " + str(len(distinct_items))+ "\n")
                        logger2.write("Total requests: " + str(algo.n_accesses)+ "\n")
                        logger2.write("ALGO: Reconfig cost: " + str(algo.moves + algo.reconfig) + "\n")
                        sum_cost_algo += (algo.access_cost + algo.moves + algo.reconfig)
                        logger2.write("Total cost: " + str(sum_cost_algo) + "\n")
                        logger2.write("ALGO: Access cost: " + str(algo.access_cost)+ "\n")
                        logger2.write("OBL: Access cost: " + str(acc_obl.access_cost) + "\n")
                        print("")
        #logger.close()
        logger2.close()
    
    def run_off_on(self, p, c):
        dataset = get_temp_processed()
        logger = open("results/results_tmp_on_off_p" + str(p) + "_c" + str(c) + ".txt", "a")
        logger2 = open("results/results_detail_tmp_on_off_p" + str(p) + "_c" + str(c) + ".txt", "a")
        for temp_p in dataset:
            if temp_p == str(p):
                logger.write("Repeating probability p = " + str(p) + "\n")
                logger2.write("Repeating probability p = " + str(p) + "\n")
                n_simulations = 0
                sum_cost_algo = 0
                sum_acc_cost_algo = 0
                sum_cost_opt = 0
                sum_cost_obl = 0
                for sample in dataset[temp_p]:
                    logger2.write("Sample = " + str(sample) + "\n")
                    n_simulations += 1
                    distinct_items = set()
                    for r in dataset[temp_p][sample]:
                        distinct_items.add(dataset[temp_p][sample][r])
                    on_tree = CompleteTree()
                    opt_tree = CompleteTree()
                    obl_tree = CompleteTree()
                    for t in [on_tree, opt_tree, obl_tree]:
                        t.set_c(c)
                        t.initialize_servers(len(distinct_items))

                    # set full initial occupation for opt and obl
                    opt_tree.initial_occupation = c
                    obl_tree.initial_occupation = c

                    # insert for on_tree
                    dist_items_list = list(distinct_items)
                    random.shuffle(dist_items_list)
                    for item in dist_items_list:
                        on_tree.insert(item)

                    # insert in obl_tree and opt_tree
                    random.shuffle(dist_items_list)
                    for item in dist_items_list:     # different order as above
                        obl_tree.insert(item)
                    opt_tree.fill_for_optimal(sequence=dataset[temp_p][sample])
                    if c == 1:
                        algo = randomPush(on_tree, single_capacity=True)
                    else:
                        algo = randomPush(on_tree)
                    acc_obl = static_offline(obl_tree)
                    acc_opt = static_offline(opt_tree)

                    # access the sequence
                    for r in dataset[str(p)][sample]:
                        algo.access(dataset[str(p)][sample][r])
                        acc_obl.access(dataset[str(p)][sample][r])
                        acc_opt.access(dataset[str(p)][sample][r])

                    sum_cost_algo += algo.access_cost + algo.moves + algo.reconfig
                    sum_acc_cost_algo += algo.access_cost
                    sum_cost_obl += acc_obl.access_cost
                    sum_cost_opt += acc_opt.access_cost

                    logger2.write("OBL: total cost: " + str(acc_obl.access_cost) + "\n")
                    logger2.write("OPT: total cost: " + str(acc_opt.access_cost) + "\n")
                    logger2.write("\n")
                logger.write("ALGO: Average total cost over " + str(n_simulations) + " simulations: "
                             + str(sum_cost_algo / n_simulations)[:10] + "\n")
                logger.write("ALGO: Average access cost over " + str(n_simulations) + " simulations: "
                             + str(sum_acc_cost_algo / n_simulations)[:10] + "\n")
                logger.write("OBL: Average total cost over " + str(n_simulations) + " simulations: "
                             + str(sum_cost_obl / n_simulations)[:10] + "\n")
                logger.write("OPT: Average total cost over " + str(n_simulations) + " simulations: "
                             + str(sum_cost_opt / n_simulations)[:10] + "\n")
                logger.write("\n")
        logger.close()
        logger2.close()

    def run_temp_exp_obl(self):
        """ Run experiment on temporal data
        for different values of c and all the temporal params p
        f = 0.5 set as default ( in method set_c(c) )
        For algo and oblivious-structure """
        dataset = get_temp_processed()
        c_params = [2, 4, 6, 8, 10, 12, 14, 16]

        logger = open("results/f-0.5-results_temp_obl" + ".txt", "a")
        logger2 = open("results/f-0.5-results_detail_obl.txt", "a")
        for c in c_params:
            logger.write("\nRunning for c = " + str(c) + "\n")
            logger2.write("\nRunning for c = " + str(c) + "\n")
            for p in dataset:
                sum_algo_total_cost = 0
                sum_algo_access_cost = 0
                sum_obl_cost = 0
                n_simulations = 0
                logger.write("Repeating probability p = " + str(p) + ". ")
                logger2.write("Repeating probability p = " + str(p) + ". ")
                for sample in dataset[p]:
                    distinct_items = set()
                    n_simulations += 1
                    for i in range(0,len(dataset[p][sample])):
                        distinct_items.add(dataset[p][sample][i])
                    logger.write((", n_items" + str(sample) + ": " + str(len(distinct_items))))
                    on_tree = CompleteTree()
                    obl_tree = CompleteTree()
                    for t in [on_tree, obl_tree]:
                        t.set_c(c)
                        t.initialize_servers(len(distinct_items))
                    # set full initial occupation for obl
                    obl_tree.initial_occupation = c

                    # insert for on_tree
                    dist_items_list = list(distinct_items)
                    random.shuffle(dist_items_list)
                    for item in dist_items_list:
                        on_tree.insert(item)

                    # insert in obl_tree
                    random.shuffle(dist_items_list)
                    for item in dist_items_list:  # different order as above
                        obl_tree.insert(item)
                    if c == 1:
                         algo = randomPush(on_tree, single_capacity = True)
                    else:
                        algo = randomPush(on_tree)
                    acc_obl = static_offline(obl_tree)
                    for i in range(0, len(dataset[p][sample])):  # for r in dataset[data][sample][trace]:
                        #print("Acessing " + str(dataset[p][sample][i]) + "index = " + str(i))
                        algo.access(dataset[p][sample][i])
                        acc_obl.access(dataset[p][sample][i])

                    print("Total items: " + str(len(distinct_items)))
                    print("Total requests: " + str(algo.n_accesses))
                    print("Access cost: " + str(algo.access_cost))
                    print("Moving cost: " + str(algo.moves))
                    print("Reconfig cost: " + str(algo.reconfig))
                    logger2.write("Total items: " + str(len(distinct_items))+ "\n")
                    logger2.write("Total requests: " + str(algo.n_accesses)+ "\n")
                    logger2.write("ALGO: Access cost: " + str(algo.access_cost)+ "\n")
                    logger2.write("ALGO: Reconfig cost: " + str(algo.moves + algo.reconfig) + "\n")
                    logger2.write("OBL: Access cost: " + str(acc_obl.access_cost)+ "\n")
                    sum_algo_total_cost += (algo.access_cost + algo.moves + algo.reconfig)
                    sum_algo_access_cost += algo.access_cost
                    sum_obl_cost += acc_obl.access_cost

                    print("")
                logger.write("\n")
                logger.write("ALGO: Average total cost over " + str(n_simulations) + " simulations: "
                             + str(sum_algo_total_cost / n_simulations)[:10] + "\n")
                logger.write("ALGO: Average access cost over " + str(n_simulations) + " simulations: "
                             + str(sum_algo_access_cost / n_simulations)[:10] + "\n")
                logger.write("OBL: Average access cost over " + str(n_simulations) + " simulations: "
                             + str(sum_obl_cost / n_simulations)[:10] + "\n")
        logger.close()
        logger2.close()

    def run_temp_for_c_obl(self, c):
        """
        run experiment on temporal data for different values of f (initial_occupancy)
        for algo and oblivious-structure
        """
        if c == 12:
            f_params = [10, 9, 8, 6, 4, 3, 2]
        else:
            raise Exception("Missing definition of f-params for this 'c'")
        dataset = get_temp_processed()
        logger = open("results/results_temp_c_" + str(c) + "_obl.txt", "a")
        logger2 = open("results/results_detailc_" + str(c) + "_obl.txt", "a")
        logger.write("\nExperiment for c = " + str(c) + "\n")
        logger2.write("\nExperiment for c = " + str(c) + "\n")
        for f in f_params:
            logger.write("\nRunning for f = " + str(f/c) + "\n")
            logger2.write("\nRunning for f = " + str(f/c) + "\n")
            for p in dataset:
                sum_algo_total_cost = 0
                sum_algo_access_cost = 0
                sum_obl_cost = 0
                n_simulations = 0
                logger.write("Repeating probability p = " + str(p) + ". ")
                logger2.write("Repeating probability p = " + str(p) + ". ")
                for sample in dataset[p]:
                    distinct_items = set()
                    n_simulations += 1
                    for i in range(0,len(dataset[p][sample])):
                        distinct_items.add(dataset[p][sample][i])
                    logger.write((", n_items" + str(sample) + ": " + str(len(distinct_items))))
                    on_tree = CompleteTree()
                    obl_tree = CompleteTree()
                    on_tree.set_c_set_f(c=c, f=f)
                    for t in [on_tree, obl_tree]:
                        t.set_c(c)
                        t.initialize_servers(len(distinct_items))
                        # set full initial occupation for obl
                    obl_tree.initial_occupation = c

                    # insert for on_tree
                    dist_items_list = list(distinct_items)
                    random.shuffle(dist_items_list)
                    for item in dist_items_list:
                        on_tree.insert(item)

                    # insert in obl_tree
                    random.shuffle(dist_items_list)
                    for item in dist_items_list:  # different order as above
                        obl_tree.insert(item)
                    if c == 1:
                        algo = randomPush(on_tree, single_capacity=True)
                    else:
                        algo = randomPush(on_tree)
                    acc_obl = static_offline(obl_tree)
                    for i in range(0, len(dataset[p][sample])):  # for r in dataset[data][sample][trace]:
                        algo.access(dataset[p][sample][i])
                        acc_obl.access(dataset[p][sample][i])
                    print("Total items: " + str(len(distinct_items)))
                    print("Total requests: " + str(algo.n_accesses))
                    print("Access cost: " + str(algo.access_cost))
                    print("Moving cost: " + str(algo.moves))
                    print("Reconfig cost: " + str(algo.reconfig))
                    logger2.write("Total items: " + str(len(distinct_items)) + "\n")
                    logger2.write("Total requests: " + str(algo.n_accesses) + "\n")
                    logger2.write("ALGO: Access cost: " + str(algo.access_cost) + "\n")
                    logger2.write("ALGO: Reconfig cost: " + str(algo.moves + algo.reconfig) + "\n")
                    logger2.write("OBL: Access cost: " + str(acc_obl.access_cost) + "\n")
                    sum_algo_total_cost += (algo.access_cost + algo.moves + algo.reconfig)
                    sum_algo_access_cost += algo.access_cost
                    sum_obl_cost += acc_obl.access_cost

                    print("")
                logger.write("\n")
                logger.write("ALGO: Average total cost over " + str(n_simulations) + " simulations: "
                             + str(sum_algo_total_cost / n_simulations)[:10] + "\n")
                logger.write("ALGO: Average access cost over " + str(n_simulations) + " simulations: "
                             + str(sum_algo_access_cost / n_simulations)[:10] + "\n")
                logger.write("OBL: Average access cost over " + str(n_simulations) + " simulations: "
                             + str(sum_obl_cost / n_simulations)[:10] + "\n")
        logger.close()
        logger2.close()


    def run_temp_for_c(self, c):
        """
        run experiment on temporal data for different values of f (initial_occupancy)
        """
        if c == 12:
            f_params = [10, 9, 8, 6, 4, 3, 2]
        else:
            raise Exception("Missing definition of f-params for this 'c'")
        dataset = get_temp_processed()
        logger = open("results/results_temp_c" + str(c) + ".txt", "a")
        logger2 = open("results/results_detail" + str(c) + ".txt", "a")
        logger.write("\nExperiment for c = " + str(c) + "\n")
        logger2.write("\nExperiment for c = " + str(c) + "\n")
        for f in f_params:
            logger.write("\nRunning for f = " + str(f/c) + "\n")
            logger2.write("\nRunning for f = " + str(f/c) + "\n")
            for p in dataset:
                sum_total_cost = 0
                n_simulations = 0
                logger.write("Repeating probability p = " + str(p) + ". ")
                logger2.write("Repeating probability p = " + str(p) + ". ")
                for sample in dataset[p]:
                    distinct_items = set()
                    n_simulations += 1
                    for r in dataset[p][sample]:
                        distinct_items.add(dataset[p][sample][r])
                    logger.write((", n_items" + str(sample) + ": " + str(len(distinct_items))))
                    ct1 = CompleteTree()
                    ct1.set_c_set_f(c=c, f=f)
                    ct1.initialize_servers(len(distinct_items))
                    for item in distinct_items:
                        ct1.insert(item)
                    algo = randomPush(ct1)
                    #print_tree(ct1.root)
                    for r in dataset[str(p)][sample]:
                        algo.access(dataset[p][sample][r])
                    print("Total items: " + str(len(distinct_items)))
                    print("Total requests: " + str(algo.n_accesses))
                    print("Access cost: " + str(algo.access_cost))
                    print("Moving cost: " + str(algo.moves))
                    logger2.write("Total items: " + str(len(distinct_items)) + "\n")
                    logger2.write("Total requests: " + str(algo.n_accesses) + "\n")
                    logger2.write("Access cost: " + str(algo.access_cost) + "\n")
                    logger2.write("Moving cost: " + str(algo.moves) + "\n")
                    logger2.write("Reconfig cost: " + str(algo.reconfig) + "\n")
                    sum_total_cost += (algo.access_cost + algo.moves + algo.reconfig)

                    print("")
                logger.write("\n")
                logger.write("Average total cost over " + str(n_simulations) + " simulations: "
                             + str(sum_total_cost / n_simulations)[:10] + "\n")
        logger.close()
        logger2.close()