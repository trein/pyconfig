import os
import logging


logger = logging.getLogger(__name__)


PYTHON_BIN_LOCATION = '/usr/bin/python%s'

class InstallException(Exception):
    pass


class Installer(object):
    _SUCCESS = 0

    # def disable_env(self):
    #     logger.info('Disabling virtualenv at %s' % VIRTUALENV_DIR)
    #     os.system('deactivate')

    # def enable_env(self):
    #     logger.info('Enabling virtualenv at %s' % VIRTUALENV_DIR)
    #     os.system('source %s/bin/activate' % VIRTUALENV_DIR)

    def setup_env(self, python_version, virtualenv_dir):
        logger.info('Setting up virtualenv at %s' % virtualenv_dir)
        if os.path.exists(virtualenv_dir):
            logger.info('Virtualenv is already setup')
        else:
            python_binary = PYTHON_BIN_LOCATION % python_version
            os.system('virtualenv -p %s %s' % (python_binary, virtualenv_dir))

    def clean_env(self, virtualenv_dir):
        logger.info('Cleaning virtualenv at %s' % virtualenv_dir)
        os.system('rm -r %s' % virtualenv_dir)

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
            dep_id = '%s%s' % (name, version)
            logger.info('Installing dependency (%s)' % dep_id)
            # os.system('%s/bin/pip install %s' % (VIRTUALENV_DIR, dep_id))
            exit_code = os.system('pip install %s' % dep_id)
            if exit_code != self._SUCCESS:
                raise InstallException('Dependency (%s) could not be installed' % dep_id)


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
