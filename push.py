import os
import json
import logging
import requests
from environ import getEnviron
from pushFactory import pusher
####################################################
# Register an account and devices at Pushover.net!
# Created by Knox Hutchinson
# http://learn.gg/dataknox
# http://youtube.com/c/dataknox
###################################################

# Create logging, log key value if wanted
script_dir = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=f'{script_dir}\\filename.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def main():
    evars = getEnviron()
    logging.info(
        f"USER KEY is {evars['user_key']}, APP TOKEN is {evars['app_token']}")
    r = pusher(evars['user_key'], evars['app_token'])
    logging.info(f"post reply {r.text}")


if __name__ == "__main__":
    main()
