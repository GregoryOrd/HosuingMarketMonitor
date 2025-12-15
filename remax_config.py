import yaml

class ConfigData:
    def __init__(
        self, 
        streetsToAvoid, 
        citiesToAvoid, 
        min_price, 
        max_price,
        remax_url,
        gad_source,
        gad_campaignid,
        gbraid,
        gclid
    ):
        self.streetsToAvoid = streetsToAvoid
        self.citiesToAvoid = citiesToAvoid
        self.min_price = min_price
        self.max_price = max_price
        self.remax_url = remax_url
        self.gad_source = gad_source,
        self.gad_campaignid = gad_campaignid,
        self.gbraid = gbraid,
        self.gclid = gclid,

    @staticmethod
    def fromConfigFile(file_path):
        try:
            with open(file_path, 'r') as file:
                config_data = yaml.safe_load(file)


            return ConfigData(
                config_data['streetsToAvoid'],
                config_data['citiesToAvoid'],
                config_data['min_price'],
                config_data['max_price'],
                config_data['remax_url'],
                config_data['gad_source'],
                config_data['gad_campaignid'],
                config_data['gbraid'],
                config_data['gclid']
            )

        except FileNotFoundError:
            print(f"Error: The config file '{file_path}' was not found.")
            return None
        except yaml.YAMLError as e:
            print(f"Error in YAML config file: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
