import logging
import os
import json


logger = logging.getLogger(__name__)

VIRTUALENV_DIR = '.env'
PROJECT_DESCRIPTOR_NAME = 'project.json'

DEPENDENCIES_KEY = 'dependencies'
DEPENDENCIES_DEV_KEY = 'development'
DEPENDENCIES_PROD_KEY = 'production'


class DependencyDescriptor(object):
    def __init__(self, descriptor):
        self.descriptor = descriptor

    def has_dev_dependency(self):
        return DEPENDENCIES_DEV_KEY in self.dependencies()

    def has_prod_dependency(self):
        return DEPENDENCIES_PROD_KEY in self.dependencies()

    def dependencies(self):
        return self.descriptor.get(DEPENDENCIES_KEY, {})

    def dev_dependencies(self):
        for dep_name, dep_version in self.dependencies().get(DEPENDENCIES_DEV_KEY, {}).items():
            yield dep_name, dep_version

    def prod_dependencies(self):
        for dep_name, dep_version in self.dependencies().get(DEPENDENCIES_PROD_KEY, {}).items():
            yield dep_name, dep_version


class Installer(object):
    def disable_env(self):
        logger.info('Disabling virtualenv at %s' % VIRTUALENV_DIR)
        os.system('source %s/bin/deactivate' % VIRTUALENV_DIR)

    def enable_env(self):
        logger.info('Enabling virtualenv at %s' % VIRTUALENV_DIR)
        os.system('source %s/bin/activate' % VIRTUALENV_DIR)

    def setup_env(self):
        logger.info('Setting up virtualenv at %s' % VIRTUALENV_DIR)
        os.system('virtualenv %s' % VIRTUALENV_DIR)

    def clean_env(self):
        logger.info('Cleaning virtualenv at %s' % VIRTUALENV_DIR)
        os.system('rm -r %s' % VIRTUALENV_DIR)

    def is_dependency_satisfied(self, name, version):
        import pkg_resources
        try:
            pkg_resources.require(['%s%s' % (name, version)])
        except pkg_resources.DistributionNotFound, pkg_resources.VersionConflict:
            logger.info('Dependency (%s%s) not installed' % (name, version))
            return False
        return True

    def install_dependency(self, name, version):
        if not self.is_dependency_satisfied(name, version):
            os.system('pip install %s%s' % (name, version))


class Workflow(object):
    def do(self):
        raise NotImplemented('Workflow not implemented')


class CleanWorkflow(Workflow):
    def do(self):
        installer = Installer()
        installer.disable_env()
        installer.clean_env()


class ProdDependencyWorkflow(Workflow):
    def __init__(self, args, descriptor):
        super(ProdDependencyWorkflow, self).__init__()
        self.args = args
        self.dep_descriptor = DependencyDescriptor(descriptor)
        self.installer = Installer()

    def _install_prod_dependencies(self):
        for dep_name, dep_version in self.dep_descriptor.dev_dependencies():
            logger.info('Processing dependency %s%s' % (dep_name, dep_version))
            self.installer.install_dependency(dep_name, dep_version)

    def do(self):
        self.installer.setup_env()
        self._install_prod_dependencies()
        self.installer.enable_env()


class DevDependencyWorkflow(ProdDependencyWorkflow):
    def __init__(self, args, descriptor):
        super(DevDependencyWorkflow, self).__init__(args, descriptor)

    def _install_dev_dependencies(self):
        for dep_name, dep_version in self.dep_descriptor.prod_dependencies():
            logger.info('Processing dependency %s%s' % (dep_name, dep_version))
            self.installer.install_dependency(dep_name, dep_version)

    def do(self):
        self.installer.setup_env()
        self._install_dev_dependencies()
        self._install_prod_dependencies()
        self.installer.enable_env()


def setup_project(args):
    descriptor = read_project_descriptor()
    logger.info('Executing %s workflow' % args.mode)
    if args.mode == 'clean':
        CleanWorkflow().do()
        return
    if args.mode == 'release':
        ProdDependencyWorkflow(args, descriptor).do()
        return
    if args.mode == 'develop':
        DevDependencyWorkflow(args, descriptor).do()
        return


def read_project_descriptor():
    descriptor = {}
    logger.info('Reading project descriptor file...')
    with open(PROJECT_DESCRIPTOR_NAME, 'r') as descriptor_stream:
        descriptor = json.loads(descriptor_stream.read())
    return descriptor
