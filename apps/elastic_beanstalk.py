from Deployer.aws.eb import ElasticBeanstalk, gui


def main():
    params = gui()
    eb = ElasticBeanstalk(source=params['source'],
                          aws_application_name=params['aws_application-name'],
                          aws_environment_name=params['aws_environment-name'],
                          aws_instance_key=params['aws_instance-key'],
                          aws_version=params['aws_version'],
                          docker_user=params['docker_user'],
                          docker_repo=params['docker_repo'],
                          docker_repo_tag=params['docker_repo_tag'])
    # Ensure directory has been initialized as an Elastic Beanstalk app and that config is correct
    eb.initialize()

    # Build and push Docker image to DockerHub
    eb.Docker.build()
    eb.Docker.push()

    # Deploy application by creating or updating an environment
    eb.deploy()

    eb.show_tasks()


if __name__ == '__main__':
    main()
