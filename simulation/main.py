
from server_experiment import *

def main():
    exp = server_experiment()

    # Fig. 4a)
    exp.run_off_on(p=0.75, c=1)

    # Fig. 4b)
    exp.run_temp_exp_obl()

    # Fig. 4c)
    exp.run_temp_for_c_obl(12)

    # Fig. 5a)
    exp.run_fb_exp_diff_c()

    # Fig. 5b)
    exp.run_fb_exp_for_c(c=12)


if __name__ == '__main__':
    main()


    
