import os
import logging


logger = logging.getLogger(__name__)


VIRTUALENV_DIR = '.env'
PYTHON_BIN_LOCATION = '/usr/bin/python%s'


class Installer(object):
    # def disable_env(self):
    #     logger.info('Disabling virtualenv at %s' % VIRTUALENV_DIR)
    #     os.system('deactivate')

    # def enable_env(self):
    #     logger.info('Enabling virtualenv at %s' % VIRTUALENV_DIR)
    #     os.system('source %s/bin/activate' % VIRTUALENV_DIR)

    def setup_env(self, python_version):
        logger.info('Setting up virtualenv at %s' % VIRTUALENV_DIR)
        python_binary = PYTHON_BIN_LOCATION % python_version
        os.system('virtualenv -p %s %s' % (python_binary, VIRTUALENV_DIR))

    def clean_env(self):
        logger.info('Cleaning virtualenv at %s' % VIRTUALENV_DIR)
        os.system('rm -r %s' % VIRTUALENV_DIR)

    # def is_dependency_satisfied(self, name, version):
    #     import pkg_resources
    #     try:
    #         pkg_resources.require(['%s%s' % (name, version)])
    #     except pkg_resources.DistributionNotFound, pkg_resources.VersionConflict:
    #         logger.info('Dependency (%s%s) not installed' % (name, version))
    #         return False
    #     return True

    def install_dependency(self, name, version):
        # if not self.is_dependency_satisfied(name, version):
        logger.info('Installing dependency (%s%s)' % (name, version))
        os.system('%s/bin/pip install %s%s' % (VIRTUALENV_DIR, name, version))


DEPENDENCIES_KEY = 'dependencies'
DEPENDENCIES_DEV_KEY = 'development'
DEPENDENCIES_PROD_KEY = 'production'


class DependencyDescriptor(object):
    def __init__(self, descriptor):
        self.descriptor = descriptor

    def python_version(self):
        return self.descriptor.get('python_version')

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
