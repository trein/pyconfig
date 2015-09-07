import logging
import json
import workflow


logger = logging.getLogger(__name__)

PROJECT_DESCRIPTOR_NAME = 'project.json'


def setup_project(args):
    descriptor = read_project_descriptor()
    logger.info('Executing %s workflow' % args.mode)
    if args.mode == 'clean':
        workflow.clean_workflow(args).do()
        return
    if args.mode == 'setup':
        workflow.setup_workflow(args, descriptor).do()
        return
    if args.mode == 'release':
        workflow.production_workflow(args, descriptor).do()
        return
    if args.mode == 'develop':
        workflow.development_workflow(args, descriptor).do()
        return


def read_project_descriptor():
    descriptor = {}
    logger.info('Reading project descriptor file...')
    with open(PROJECT_DESCRIPTOR_NAME, 'r') as descriptor_stream:
        descriptor = json.loads(descriptor_stream.read())
    return descriptor
