import shutil
from pathlib import Path

use_k8s = "{{ cookiecutter.use_k8s }}"

if use_k8s.lower() != "yes":
    k8s_path = Path("k8s")
    if k8s_path.exists():
        shutil.rmtree(k8s_path)

use_git = "{{ cookiecutter.use_git }}"

# Paths
gitlab_ci = Path(".gitlab-ci.yml")
github_actions = Path(".github")

if use_git == "gitlab":
    # Keep GitLab CI, remove GitHub Actions
    if github_actions.exists():
        shutil.rmtree(github_actions)
else:
    # Keep GitHub Actions, remove GitLab CI
    if gitlab_ci.exists():
        gitlab_ci.unlink()
