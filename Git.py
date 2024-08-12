from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
from git import Repo
from os import makedirs
from os.path import dirname, join as joinpath

working_dir = dirname(__file__)

class RepoInfo:
    def __init__(self, repo_name: str, repo_type: str, repo_href: str, programming_language: str, updated_time: str) -> None:
        self.repo_name = repo_name
        self.repo_type = repo_type
        self.repo_href = repo_href
        self.programming_language = programming_language
        self.updated_time = updated_time

class GitPy:
    def __init__(self, username: str) -> None:
        self.username = username
        self.repo_list = []
        self.user_repo_folder = joinpath(working_dir, username)
        makedirs(self.user_repo_folder, exist_ok=True)
    
    def add(self) -> None:
        self.repo.git.add(".")
    
    def commit(self, message: str) -> None:
        self.repo.git.commit(m=message)
    
    def push(self) -> None:
        self.repo.git.push()
    
    def pull(self) -> None:
        self.repo.git.pull()
    
    def clone(self, repo_name: str, repo_href: str) -> None:
        Repo.clone_from(repo_href, joinpath(self.user_repo_folder, repo_name))
    
    def clone_all_repos(self):
        for repo in self.repo_list:
            self.clone(repo.repo_name,repo.repo_href)
    
    def scrape_repo_list_from_user(self):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        github_url = "https://github.com"
        url = f"{github_url}/{self.username}"
        repo_url = f"{url}?tab=repositories"
        driver.get(repo_url)

        DELAY = 10
        try:
            repo_list_element = WebDriverWait(driver, DELAY).until(
                EC.presence_of_element_located(
                    (By.ID, "user-repositories-list")
                )
            )
            
            repo_list_html = repo_list_element.get_attribute("outerHTML")
            soup = BeautifulSoup(repo_list_html, "html.parser")
            
            lines = ["Repo Name, Repo Type, Repo Href, Programming Language, Updated Time"]
            for soup in soup.find_all("li"):
                programming_language = soup.find("span", {"itemprop":"programmingLanguage"})
                if programming_language:
                    programming_language = programming_language.text.strip()
                else:
                    programming_language = " "    
                repo_element = soup.find("a", {"itemprop":"name codeRepository"})
                repo_name = repo_element.text.strip()
                repo_href = f"{repo_url}{repo_element['href']}.git"
                repo_type = soup.find("span", {"class":"Label Label--secondary v-align-middle ml-1 mb-1"}).text.strip()
                updated_time = soup.find("relative-time").text.strip().replace(",", "")
                self.repo_list.append(RepoInfo(repo_name, repo_type, repo_href, programming_language, updated_time))
                lines.append(f"{repo_name}, {repo_type}, {repo_href}, {programming_language}, {updated_time}")
            
            with open("output.csv", "w") as f:
                f.writelines("\n".join(lines))
            

        except TimeoutException as e:
            pass