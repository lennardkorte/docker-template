
import os
import sys

from pathlib import Path
from functools import reduce
from operator import getitem
from typing import Any
from argparse import ArgumentParser

from utils import Utils

NAME_CONFIG_FILE_STANDARD = 'config_std.json'
NAME_CONFIG_FILE_COPY = 'config_std.json'

class Config(dict):
    ''' The "Config" object acts like a "dict", is initialized and represents the actual
    and final configuration of the application before the start.
    It reads the arguments and configuration files to determine the configuration.
    '''
    
    def __init__(self, args:ArgumentParser, options:list):
        ''' Initialized the config object with the right configuration.
        - First adds the configurations from the standard configuration file.
        - Secondly overwrites all given configurations with the config file provided in an argument.
        - Third: Overwrites configuration with all arguments given as argument.
        Arguments:
            self: The "Config" object itself.
            args: Standard arguments like config-file directory which are essential for running the program.
            options: Custom arguments to add and evaluate.
        Return:
            The class constructor returns a "Config" object.
        '''
        
        # Reads all given arguments and adds them to the args variable.
        for opt in options:
            args.add_argument(*opt.flags, default=None, type=opt.type)
        if not isinstance(args, tuple):
            args = args.parse_args()
        
        # Reads the standard configuration file to create the dict foundation.
        config = Utils.read_json('./cfgs/' + NAME_CONFIG_FILE_STANDARD)
        # Adds / overwrites the given config to the new config.
        if args.config is not None:
            config.update(Utils.read_json(args.config))
            
        # Given arguments overwrite all other configs.
        config.update({
            'overwrite_configurations': args.overwrite_configurations,
            'gpus':args.gpus
            })

        # Adds random other arguments to the config file.
        modification = {opt.target : getattr(args, self._get_opt_name(opt.flags)) for opt in options}
        self.config = self._update_config(config, modification)
        
        # Create main directory to store the results.
        self.save_path = Path('./data/working/')
        os.makedirs(self.save_path, exist_ok=True)

        # Checks if copy of the same config as a file is already existing or not. If not, creates new one.
        # Warns user with a dialogue when config changed, in case a program tries to continue.
        config_file_copy_path = self.save_path / NAME_CONFIG_FILE_COPY
        if os.path.isfile(config_file_copy_path) and not Utils.read_json(config_file_copy_path) == config:
            if config['overwrite_configurations']:
                print('This model has been trained with a different config before. Sure that you want to run this with a changed configuration file? Run with different name is recommended.')
                print('"yes" or "no" ?')
                while(True):
                    choice = input().lower()
                    if choice in 'yes':
                        break
                    elif choice in 'no':
                        print('canceled')
                        exit()
                    else:
                        sys.stdout.write("Please respond with 'yes' or 'no'")

        else:
            Utils.write_json(self.config, config_file_copy_path)

    def __getitem__(self, key:str):
        ''' Makes the object accessable like a normal dict.
        Arguments:
            self: The "Config" object itself.
            key: The key to access in the config dict.
        Return:
            The value belonging to the given key in the dict.
        '''
        
        # Return right dict value accessed by key.
        return self.config[key]
    
    def __contains__(self, key:str):
        ''' Makes the object behave like a dict in an is-in expression.
        Arguments:
            self: The "Config" object itself.
            key: The key to check availability on in the config dict.
        Return:
            The function returns True or False depending if the key exists in dict or not.
        '''
        
        # Checks if key is in config.
        return key in self.config
    
    def __setitem__(self, name:str, value:Any):
        ''' Makes the object behave like a dict when adding new keys to it.
        Arguments:
            self: The "Config" object itself.
            name: The name of the new key.
            value: Object or type assigned / belonging to the key in the config dict.
        Return:
            This Method has nothing to return.
        '''
        
        # Adds a new key with value to the config dict.
        self.config[name] = value

    @classmethod
    def _update_config(cls, config:dict, modification:dict) -> dict:
        ''' Updates the configurations according to the CLI options given.
        Arguments:
            cls: The "Config" class itself.
            config: The current configuration.
            modification: CLI Options to add to configurations.
        Return:
            This Method returns the updated configuration.
        '''
        
        # Checks if modifications are given.
        if modification is None:
            return config

        # Add all cli options to dictionary.
        for key, value in modification.items():
            if value is not None:
                cls._set_by_path(config, key, value)
        return config

    @staticmethod
    def _get_opt_name(flags:list) -> list:
        ''' Removes the double dashes from the given argument parameters.
        Arguments:
            flags: Strings to remoce the dashes from and convert to keys.
        Return:
            List of Keys without dashes.
        '''
        
        # Remove dashes from list of strings.
        for flag in flags:
            if flag.startswith('--'):
                return flag.replace('--', '')
        return flags[0].replace('--', '')

    @classmethod
    def _set_by_path(cls, tree:dict, keys:list, value:Any) -> None:
        ''' Removes the two dashes from the given argument parameters.
        Arguments:
            cls: The "Config" class itself.
            tree: The current configuration dict.
            keys: Key of dict where to add the value to.
            value: Any value that was given as CLI option.
        Return:
            This method has nothing to return.
        '''
        
        # Create list of keys and assign value to that dict element.
        keys = keys.split(';')
        cls._get_by_path(tree, keys[:-1])[keys[-1]] = value

    @staticmethod
    def _get_by_path(tree:dict, keys:list) -> Any:
        ''' Gets a value in the dict by a specified path and returns it.
        
        Arguments:
            tree: Dictionary where the keys and values are in.
            keys: List of key / path to look under.
        Return:
            This method has nothing to return.
        '''
        
        # Gets value in dict by path.
        return reduce(getitem, keys, tree)