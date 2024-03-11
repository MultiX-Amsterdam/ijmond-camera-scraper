# ijmond-camera-scraper

This repository hosts the code for scraping camera images from an URL and then storing the images in the structure that enables us to [create zoomable timelapses](https://github.com/CMU-CREATE-Lab/timemachine-creator).

### Table of Content
- [Coding standards](#coding-standards)

# <a name="coding-standards"></a>Coding standards
When contributing code to this repository, please follow the guidelines below:

### Language
- The primary language for this repository is set to English. Please use English when writing comments and docstrings in the code. Please also use English when writing git issues, pull requests, wiki pages, commit messages, and the README file.

### Git workflow
- Follow the [Git Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow). The master branch preserves the development history with no broken code. When working on a system feature, create a separate feature branch.
- Always create a pull request before merging the feature branch into the main branch. Doing so helps keep track of the project history and manage git issues.
- NEVER perform git rebasing on public branches, which means that you should not run "git rebase [FEATURE-BRANCH]" while you are on a public branch (e.g., the main branch). Doing so will badly confuse other developers since rebasing rewrites the git history, and other people's works may be based on the public branch. Check [this tutorial](https://www.atlassian.com/git/tutorials/merging-vs-rebasing#the-golden-rule-of-rebasing) for details.
- NEVER push credentials to the repository, for example, database passwords or private keys for signing digital signatures (e.g., the user tokens).
- Request a code review when you are not sure if the feature branch can be safely merged into the main branch.

### Python package installation
- Make sure you are in the correct conda environment before installing packages. Otherwise, the packages will be installed to the server's general python environment, which can be problematic.
- Make sure the packages are in the [install_packages.sh](back-end/install_packages.sh) script with version numbers, which makes it easy for others to install packages.
- Use the pip command first. Only use the conda command to install packages when the pip command does not work.

### Coding style
- Use the functional programming style (check [this Python document](https://docs.python.org/3/howto/functional.html) for the concept). It means that each function is self-contained and does NOT depend on a state that may change outside the function (e.g., global variables). Avoid using the object-oriented programming style unless necessary. In this way, we can accelerate the development progress while maintaining code reusability.
- Minimize the usage of global variables, unless necessary, such as system configuration variables. For each function, avoid modifying its input parameters. In this way, each function can be independent, which is good for debugging code and assigning coding tasks to a specific collaborator.
- Use a consistent coding style.
  - For Python, follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/), for example, putting two blank lines between functions, using the lower_snake_case naming convention for variable and function names. Please use double quote (not single quote) for strings.
  - For JavaScript, follow the [Idiomatic JavaScript style guide](https://github.com/rwaldron/idiomatic.js), for example, using lowerCamelCase naming convention for variable and function names. Please use double quote (not single quote) for strings.
- Document functions and script files using docstrings.
  - For Python, follow the [numpydoc style guide](https://numpydoc.readthedocs.io/en/latest/format.html). Here is an [example](https://numpydoc.readthedocs.io/en/latest/example.html#example). More detailed numpydoc style can be found on [LSST's docstrings guide](https://developer.lsst.io/python/numpydoc.html).
  - For JavaScript, follow the [JSDoc style guide](https://jsdoc.app/index.html)
- For naming files, never use white spaces.
  - For Python script files (and shell script files), use the lower_snake_case naming convention. Avoid using uppercase.
  - For JavaScript files, use the lower_snake_case naming convention. Avoid using uppercases.
- Always comment the code, which helps others read the code and reduce our pain in the future when debugging or adding new features.
- Write testing cases to make sure that functions work as expected.

# <a name="install-conda"></a>Dockerize the code 

### Setup the Docker engine (administrator only)
> WARNING: this section is only for system administrators, not developers.

This assumes that Ubuntu is installed.
A detailed documentation is [here](https://docs.docker.com/engine/install/ubuntu/).
Before you install Docker Engine for the first time on a new host machine, you need to set up the Docker repository. Afterward, you can install and update Docker from the repository.
1. Set up Docker's apt repository:
```sh
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
2. Install the Docker packages:
```sh
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
3. Verify that the Docker Engine installation is successful by running the hello-world image. This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.
```sh
sudo docker run hello-world
```

### Create Docker image and run it
1. Create the Dockerfile, where you need to specify the working directory, the python version and install the required libraries:
```sh
FROM python:alpine3.17
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "scraper.py"]
```

2. This is the Docker command used to build the Docker image. It reads the instructions from a Dockerfile and generates a Docker image based on those instructions. Tha name of the image is scraper.
```sh
sudo docker build -t scraper:0.0.0 .
```

3. Run the Docker image by specifying the camera_name and the url of the camera. The -d options means that the container runs in the background and doesn't keep the terminal tied up. The --restart unless-stopped option specifies the container's restart policy. In this case, it instructs Docker to restart the container automatically unless it is explicitly stopped by the user. This ensures that the container is always running, even if it crashes or the Docker daemon restarts.
```sh
sudo docker run -d --restart unless-stopped -v "$(pwd)/camera_name:/app/camera_name" scraper:0.0.0 'http://username:password@root:port/image.jpg' camera_name
```

4. If the user wants to stop the container:
```sh
sudo docker stop CONTAINERID
sudo docker rm CONTAINERID
```
