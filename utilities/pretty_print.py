from lxml import etree
import os

class DirectoryOfFiles:
    def __init__(self, directory):
        self.directory = directory
        self.sets = self.get_sets()

    def pretty_print_directory(self):
        for set in self.sets:
            for file in os.listdir(f'{self.directory}/{set}/MODS'):
                tree = etree.parse(os.path.join(f'{self.directory}/{set}/MODS', file))
                pretty_xml = etree.tostring(tree, pretty_print=True, encoding='unicode')
                with open(os.path.join(f'{self.directory}/{set}/MODS', file), 'w') as file:
                    file.write(pretty_xml)

    def get_sets(self):
        return [file for file in os.listdir(self.directory)]


if __name__ == "__main__":
    x = DirectoryOfFiles('providers/utk/')
    x.pretty_print_directory()