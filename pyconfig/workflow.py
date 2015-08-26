import environment
import logging


logger = logging.getLogger(__name__)


class Workflow(object):
    def do(self):
        raise NotImplemented('Workflow not implemented')


class CleanWorkflow(Workflow):
    def do(self):
        installer = environment.Installer()
        installer.disable_env()
        installer.clean_env()


class ProdDependencyWorkflow(Workflow):
    def __init__(self, args, descriptor):
        super(ProdDependencyWorkflow, self).__init__()
        self.args = args
        self.project_descriptor = environment.DependencyDescriptor(descriptor)
        self.installer = environment.Installer()

    def _install_prod_dependencies(self):
        for dep_name, dep_version in self.project_descriptor.dev_dependencies():
            logger.info('Processing dependency %s%s' % (dep_name, dep_version))
            self.installer.install_dependency(dep_name, dep_version)

    def do(self):
        python_version = self.project_descriptor.python_version()
        self.installer.setup_env(python_version)
        self._install_prod_dependencies()
        self.installer.enable_env()


class DevDependencyWorkflow(ProdDependencyWorkflow):
    def __init__(self, args, descriptor):
        super(DevDependencyWorkflow, self).__init__(args, descriptor)

    def _install_dev_dependencies(self):
        for dep_name, dep_version in self.project_descriptor.prod_dependencies():
            logger.info('Processing dependency %s%s' % (dep_name, dep_version))
            self.installer.install_dependency(dep_name, dep_version)

    def do(self):
        python_version = self.project_descriptor.python_version()
        self.installer.setup_env(python_version)
        self._install_dev_dependencies()
        self._install_prod_dependencies()
        self.installer.enable_env()
