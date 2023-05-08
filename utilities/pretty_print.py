from lxml import etree
import os

class DirectoryOfFiles:
    def __init__(self, directory):
        self.directory = directory

    def pretty_print_directory(self):
        for file in os.listdir(self.directory):
            tree = etree.parse(os.path.join(self.directory, file))
            pretty_xml = etree.tostring(tree, pretty_print=True, encoding='unicode')
            with open(os.path.join(self.directory, file), 'w') as file:
                file.write(pretty_xml)


if __name__ == "__main__":
    x = DirectoryOfFiles('providers/bcpl/p17194coll17/MODS')
    x.pretty_print_directory()