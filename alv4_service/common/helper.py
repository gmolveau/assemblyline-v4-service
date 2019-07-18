import os

import yaml

from assemblyline.common.classification import Classification, InvalidDefinition
from assemblyline.common.dict_utils import recursive_update


def get_classification() -> Classification:
    classification_yml = '/etc/assemblyline/classification.yml'

    classification_definition = {}

    '''default_file = os.path.join(os.path.dirname(__file__), 'classification.yml')
    if os.path.exists(default_file):
        with open(default_file) as default_fh:
            default_yml_data = yaml.safe_load(default_fh.read())
            if default_yml_data:
                classification_definition.update(default_yml_data)'''

    # while True:
        # Load modifiers from the yaml config
    if os.path.exists(classification_yml):
        with open(classification_yml) as yml_fh:
            yml_data = yaml.safe_load(yml_fh.read())
            if yml_data:
                classification_definition = recursive_update(classification_definition, yml_data)
                    # break
        # else:
        #     time.sleep(5)


    if not classification_definition:
        raise InvalidDefinition("Could not find any classification definition to load.")

    return Classification(classification_definition)