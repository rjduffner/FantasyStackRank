import os
import yaml
import yql


# YQL query to get current nhl game key
# select * from fantasysports.games where use_login=1 and game_key in ('nhl')
GAME_KEY = 341

# League ID found on league page
#
LEAGUE_ID = 13222

# Create league key from game key and league id
#
LEAGUE_KEY = '%s.l.%s' % (GAME_KEY, LEAGUE_ID)

# Team Key
#
# To get stats
# select * from fantasysports.teams.stats where team_key='341.l.13222.t.10'
#
# To get stat_ids
# select * from fantasysports.leagues.settings where league_key='341.l.13222'
TEAM_NUMBER = '10'
TEAM_KEY = '%s.t.%s' % (LEAGUE_KEY, TEAM_NUMBER)



class FantasyApi(object):
    def __init__(self, key_configuration_file=None):

        if key_configuration_file is None:
            self.key_configuration_file = os.path.join(
                os.getenv('API_KEYS'), 'yahoo.yaml')
        else:
            self.key_configuration_file = key_configuration_file

        self.configuration = self._load_yaml_configuration()

        self.y3 = yql.ThreeLegged(
            self.configuration.get('consumer_key'),
            self.configuration.get('consumer_secret'))

    def _load_yaml_configuration(self):
        with open(self.key_configuration_file) as f:
            keys = yaml.safe_load(f)
        return keys

    def _save_yaml_configuration(self):
        with open(self.key_configuration_file, 'w') as f:
           f.write(yaml.dump(self.configuration, default_flow_style=False))

    def get_access_token_manually(self):
        y3 = yql.ThreeLegged(self.configuration.get('consumer_key'),
                             self.configuration.get('consumer_secret'))
        request_token, auth_url = y3.get_token_and_auth_url()
    
        print auth_url
        verifier = raw_input('Please enter the PIN shown: ')

        access_token = y3.get_access_token(request_token, verifier)
        return access_token

    def get_access_token(self):
        try:
            token = yql.YahooToken.from_string(self.configuration['access_token'])
        except KeyError:
            token = self.get_access_token_manually()
            self.configuration['access_token'] = token.to_string()


        return token

    def make_call(self, query):
        # Get access token from file or manually
        access_token = self.get_access_token()

        # Check token for timeout
        access_token = self.y3.check_token(access_token)

        # Run Query
        response = self.y3.execute(query, token=access_token)
        
        # Save configuration
        self._save_yaml_configuration()
        
        # Return results
        return response


#
# This will allow for the extended use of the access token (auto refresh)
#
# However, if no token exists, you will still have to
# make the first token manually.
#
#
query = "select * from fantasysports.leagues.standings where league_key='%s'" % LEAGUE_KEY

fapi = FantasyApi()
response = fapi.make_call(query)
print response.raw
