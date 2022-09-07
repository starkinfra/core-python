from ..utils.checks import check_environment


class PublicUser:

    def __init__(self, environment):
        self.environment = check_environment(environment)
