from repox.repox import Repox
import yaml
import xmltodict
import json


class Manifest:
    def __init__(self, repox_instance, provider_id, good_sets=[]):
        self.repox = repox_instance
        self.provider_id = provider_id
        self.datasets = repox_instance.get_list_of_sets_from_provider(provider_id)
        self.good_sets = good_sets
        self.dataset_info = { provider_id: self.parse_sets() }

    def parse_sets(self):
        return [DataSet(dataset, self.repox).build() for dataset in self.datasets if dataset in self.good_sets]

    def write_manifest(self):
        with open(f'manifests/{self.provider_id}.json', 'w') as file:
            pretty_json = json.dumps(self.dataset_info, indent=4)
            file.write(pretty_json)


class DataSet:
    def __init__(self, dataset_id, repox_instance):
        self.repox = repox_instance
        self.dataset_id = dataset_id
        self.details = self.repox.get_dataset_details(dataset_id)
        self.last_ingest = self.repox.get_last_ingest_date_of_set(dataset_id)
        self.log = self.repox.get_log_of_last_harvest(dataset_id)

    def build(self):
        return {
            'dataset_id': self.dataset_id,
            'last_ingest': self.last_ingest,
            'details': self.get_important_details(),
            'log': self.get_important_log_info(),
        }

    def get_important_details(self):
        return {
            'acquisition_method': self.details['dataSource']['dataSetType'],
            'schema': self.details['dataSource']['schema'],
            'namespace': self.details['dataSource']['namespace'],
            'description': self.details['dataSource']['description'],
            'metadata_format': self.details['dataSource']['metadataFormat'],
            'oai_endpoint_url': self.details['dataSource'].get('oaiSourceURL', None),
            'original_oai_set_name': self.details['dataSource'].get('oaiSet', None),
        }

    def get_important_log_info(self):
        x = xmltodict.parse(self.log)
        return {
            'status': x['report']['status'],
            'start_time': x['report']['startTime'],
            'end_time': x['report']['endTime'],
            'duration': x['report']['duration'],
            'records': x['report']['records'],
            'deleted_records': x['report']['deleted'],
        }


if __name__ == '__main__':
    r = Repox('https://dpla.lib.utk.edu', 'user', 'pass')
    good_sets = []
    with open('sets.yml', 'r') as file:
        # Read the contents of the YAML file
        yaml_data = yaml.safe_load(file)
        for k, v in yaml_data.items():
            for dataset in v:
                good_sets.append(dataset)
    providers = r.get_list_of_providers('TNDPLAr0')
    for provider in providers:
        m = Manifest(r, provider, good_sets)
        m.parse_sets()
        m.write_manifest()
