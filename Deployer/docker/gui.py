import PySimpleGUI as sg
from Deployer.utils import most_recent_history
from Deployer.aws.config import DOCKER_USER, DOCKER_REPO_TAG


LABEL_COL_WIDTH = 20
INPUT_COL_WIDTH = 50
HEADER_FONT_SIZE = 30
BODY_FONT_SIZE = 20
DEFAULT_FONT = 'Any {0}'.format(HEADER_FONT_SIZE)


def gui(source=None, docker_user=None, docker_repo=None, docker_tag=None):
    """GUI form for choosing packages to upload to DeployPyPi."""
    # Get most recent deployment data
    most_recent = most_recent_history()
    sg.SetOptions(text_justification='left')

    # Set parameter values
    most_recent['source'] = source if source else most_recent.get('source', None)
    most_recent['docker_user'] = docker_user if docker_user else most_recent['docker_user']
    most_recent['docker_repo'] = docker_repo if docker_repo else most_recent['docker_repo']
    most_recent['docker_repo_tag'] = docker_tag if docker_tag else most_recent['docker_repo_tag']

    # Local directory settings
    directory_settings = [
        # Source
        [sg.Text('Source', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent['source'], size=(INPUT_COL_WIDTH, 1), key='source',
               font='Any {0}'.format(16))]
    ]

    # DockerHub settings
    docker_hub_settings = [
        # Username
        [sg.Text('Username', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('docker_user', DOCKER_USER), size=(INPUT_COL_WIDTH, 1), key='docker_user')],

        # Repo
        [sg.Text('Repository', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('docker_repo', most_recent.get('aws_environment-name', '')),
               size=(INPUT_COL_WIDTH, 1), key='docker_repo')],

        # Tag
        [sg.Text('Tag', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('docker_repo_tag', DOCKER_REPO_TAG), size=(INPUT_COL_WIDTH, 1),
               key='docker_repo_tag')]
    ]

    # Deployable project options
    commands = [[sg.Checkbox(cmd.capitalize(), size=(LABEL_COL_WIDTH, 1),
                             default=False if cmd is not 'build' else True, key=cmd)
                 for cmd in ('build', 'push', 'run')]]

    # Create form layout
    layout = [
        [sg.Frame('Directory settings', directory_settings, title_color='green', font=DEFAULT_FONT)],
        [sg.Frame('DockerHub settings', docker_hub_settings, title_color='blue', font=DEFAULT_FONT)],
        [sg.Frame('Docker commands', commands, title_color='blue', font=DEFAULT_FONT)],
        [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('Docker Hub Deployment Control', font=("Helvetica", HEADER_FONT_SIZE))
    window.Layout(layout)

    while True:
        button, values = window.ReadNonBlocking()
        if button is 'Submit':
            return values
        elif button is 'Cancel':
            exit()
