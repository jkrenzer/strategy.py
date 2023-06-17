from strategy import logging


from configargparse import ArgParser, YAMLConfigFileParser
from unittest import TestLoader
from . import load_tests
import sys

tests = TestLoader().loadTestsFromModule(sys.modules[__name__])

rootParser = ArgParser(
    prog='test',
    default_config_files=['./.config_test.yml'],
    config_file_parser_class=YAMLConfigFileParser,
    args_for_writing_out_config_file=['-w', '--write-config']
)

rootParser.add('-c', '--config', required=False,  # type: ignore
               is_config_file=True, help='config file path')
rootParser.add('--log-level', default='debug', help="set loglevel",  # type: ignore
               choices=logging.log_levels)
rootParser.add('-v','--verbose', help='be verbose', action='count', default=0)  # type: ignore
rootParser.add('-t','--tap', help='output results in TAP protocol', action='store_true')  # type: ignore

if __name__ == '__main__':
    #    logging.basicConfig(level=logging.DEBUG)

    options = rootParser.parse_args()

    # Set loglevel
    logging.basicConfig(level=logging.log_levels[options.log_level.lower()])

    if options.tap:
        from pycotap import TAPTestRunner
        TAPTestRunner().run(tests)
    else:
        from unittest import TextTestRunner
        TextTestRunner(verbosity=options.verbose).run(tests)
