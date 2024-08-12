

from Git import GitPy

username = "harry1180"
gitpy = GitPy(username)
gitpy.scrape_repo_list_from_user()
print(gitpy.repo_list)
gitpy.clone_all_repos()