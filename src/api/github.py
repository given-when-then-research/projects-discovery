from github import Github

class ApiGithub:
    def __init__(self,github_token:str):
        self.api = Github(github_token)