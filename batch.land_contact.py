#!/usr/bin/env python3
import sys
import os
import time

def main():
    sites = ['cvao','hateruma','ragged_point','mace_head','tudor_hill','minamitorishima','cape_grim']
    days_ = [ 3, 5, 7, 9]

    for site in sites:
        for days in days_:
            sed_cmd   = (f'sed -i "s/#SBATCH --job-name=.*/#SBATCH --job-name={days}{site}/" ./land_contact.py')
            os.system( sed_cmd )

            run_cmd=f'sbatch ./land_contact.py {site} {days}'
            run_cmd=f'sbatch ./land_contact.py {site} {days}'
            print( run_cmd )
            os.system( run_cmd )

            time.sleep(.5)

    
if __name__=="__main__":
    main()
