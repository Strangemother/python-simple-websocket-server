"""Load config tools
"""
import yaml


def load(filename):
    """
    Load a yaml file and return a tuple for success, content
    """
    with open(filename, 'r') as stream:
        try:
            return True, yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            return False, exc
