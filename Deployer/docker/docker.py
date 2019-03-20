import os
from Deployer.utils import TaskTracker


class DockerCommands:
    def __init__(self, source, repo, tag, username):
        """
        A collection of properties and methods that return docker command strings.

        Provides access to underlying Docker commands that are executed.  Use cases
        include debugging, logging and copying and pasting commands to terminal
        in order to save time typing repeated commands.

        :param source: Docker files source path
        :param repo: Docker repo name
        :param tag: Docker repo tag
        :param username: Docker username
        """
        self.source = source
        self.repo = repo
        self.tag = tag
        self.username = username

    @property
    def docker_image(self):
        """Concatenate DockerHub user name and environment name to create docker image tag."""
        return '{user}/{repo}:{tag}'.format(user=self.username, repo=self.repo, tag=self.tag)

    @property
    def build(self):
        """Returns a Docker 'build' command string."""
        return 'docker build -t {0}'.format('{tag} {source}'.format(tag=self.docker_image, source=self.source))

    @property
    def run(self):
        """Returns a Docker 'run' command string."""
        return 'docker run -i -t -p 5000:5000 {0}'.format(self.docker_image)

    @property
    def push(self):
        """Returns a Docker 'push' command string."""
        return 'docker push {0}'.format(self.docker_image)


class Docker(TaskTracker):
    def __init__(self, source, repo, tag, username):
        """
        Docker hub deployment helper.

        :param source: Docker files source path
        :param repo: Docker repo name
        :param tag: Docker repo tag
        :param username: Docker username
        """
        self.cmd = DockerCommands(source, repo, tag, username)

    @property
    def available_commands(self):
        """Return a string containing all available Docker commands"""
        return 'AVAILABLE DOCKER COMMANDS:\n' + '\n'.join('{0}'.format(cmd) for cmd in
                                                          (self.cmd.build, self.cmd.run, self.cmd.push)) + '\n'

    def build(self):
        """Build a docker image for distribution to DockerHub."""
        print('Building Docker image')
        os.system(self.cmd.build)
        self.add_task('Built Docker image {0}'.format(self.cmd.docker_image))

    def run(self):
        """Push a docker image to a DockerHub repo."""
        print('Locally running Docker image')
        os.system(self.cmd.run)
        self.add_task('Running Docker image {0} or local machine'.format(self.cmd.docker_image))

    def push(self):
        """Push a docker image to a DockerHub repo."""
        print('Pushing Docker image')
        os.system(self.cmd.push)
        self.add_task('Pushed Docker image {0} to DockerHub repo'.format(self.cmd.docker_image))
