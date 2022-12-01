
import os
import GPUtil
import argparse
import collections

from logger import Logger
from config import Config

def run(config:Config):
    Logger.print_section_line()
    os.system('nvidia-smi')
    Logger.print_section_line()
    with Logger(config.save_path / 'run.log', 'a'):
        print('Everything works fine. Test config: ', config['key1'])
        print('Put your code here')

    

if __name__ == '__main__':
    args = argparse.ArgumentParser(description='project_template')
    args.add_argument('-cfg', '--config', default=None, type=str, help='config file path (default: None)')
    args.add_argument('-gpu', '--gpus', default='', type=str, help='indices of GPUs to enable (default: none)')
    args.add_argument('-ycf', '--overwrite_configurations', dest='overwrite_configurations', action='store_false', help='Overwrite Configurations, if config file in this directory already exists. (default: False)')
    CustomArgs = collections.namedtuple('CustomArgs', 'flags type target')
    options = [
        CustomArgs(['--op1', '--option1'], type=float, target='option1'),
        CustomArgs(['--op2', '--option2'], type=str, target='option2'),
        
        # Add more arguments here
    ]
    
    config = Config(args, options)
    
    if config['gpus'] != '' and len(GPUtil.getAvailable()) == 0:
        print(f'There is no GPU available.\n')
    else:
        run(config)