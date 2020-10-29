import os
# from dotenv import load_dotenv
# load_dotenv()


def getEnviron():
    # get Pushover USER key and API Token from environment variables
    # Make sure to create an application and get user key from Pushover Dashboard
    evars = {}
    user_key = os.environ.get('PUSHOVERKEY')
    app_token = os.environ.get('APPKEY')
    evars['user_key'] = user_key
    evars['app_token'] = app_token
    print(evars)
    return evars
