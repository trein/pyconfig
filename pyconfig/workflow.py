import environment
import logging


logger = logging.getLogger(__name__)


def clean_workflow(args):
    return CleanWorkflow(args)


def setup_workflow(args, descriptor):
    return SetupWorkflow(args, descriptor)


def production_workflow(args, descriptor):
    return CompositeWorkflow()\
            .add(setup_workflow(args, descriptor))\
            .add(ProdDependencyWorkflow(args, descriptor))


def development_workflow(args, descriptor):
    return production_workflow(args, descriptor)\
            .add(DevDependencyWorkflow(args, descriptor))


class Workflow(object):
    def do(self):
        raise NotImplemented('Workflow not implemented')


class CompositeWorkflow(Workflow):
    def __init__(self):
        self.flows = []

    def add(self, w):
        self.flows.append(w)
        return self

    def do(self):
        for w in self.flows:
            w.do()


class CleanWorkflow(Workflow):
    def __init__(self, args):
        self.args = args

    def do(self):
        installer = environment.Installer()
        installer.clean_env(self.args.env_dir)


class SetupWorkflow(Workflow):
    def __init__(self, args, descriptor):
        self.project_descriptor = environment.DependencyDescriptor(descriptor)
        self.installer = environment.Installer()
        self.args = args

    def do(self):
        python_version = self.project_descriptor.python_version()
        self.installer.setup_env(python_version, self.args.env_dir)


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
        self._install_prod_dependencies()


class DevDependencyWorkflow(Workflow):
    def __init__(self, args, descriptor):
        super(DevDependencyWorkflow, self).__init__()
        self.args = args
        self.project_descriptor = environment.DependencyDescriptor(descriptor)
        self.installer = environment.Installer()

    def _install_dev_dependencies(self):
        for dep_name, dep_version in self.project_descriptor.prod_dependencies():
            logger.info('Processing dependency %s%s' % (dep_name, dep_version))
            self.installer.install_dependency(dep_name, dep_version)

    def do(self):
        self._install_dev_dependencies()
