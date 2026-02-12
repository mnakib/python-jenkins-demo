
This guide follows the "Pipeline as Code" philosophy, where your automation steps live inside your GitHub repository in a file called a Jenkinsfile.

## 0. Prepare the Prereq

### 0.1 Create a working directory 
```bash
mkdir jenkins-demo && cd jenkins-demo
```

### 0.2 Prepare and create the Jenkins customized image

Create a custom image Jenkins that includes Python as the default Jenkins image does not include Python by defautl. Python needs to be installed because the Jenkins Pipeline will run a Python application.

```bash
cat > Containerfile
```

```dockerfile
# Start from the standard Jenkins LTS image
FROM jenkins/jenkins:lts

# Switch to root user to install software
USER root

# Install Python 3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv docker.io zip && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the standard jenkins user
USER jenkins
```

```bash
# Create the image
podman build -t python-jenkins .

# Check the image is successfully created
podman images
```



## 1. Create the Python App (GitHub)

Create a new GitHub repo (e.g., `python-jenkins-demo`) and add these two files.

### 1.1 The App: `app.py`

Create the Python application file, named `app.py`, containing a simple calculator script with a built-in test.

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    print("Test Passed!")

if __name__ == "__main__":
    print(f"Result: {add(10, 5)}")
    test_add()
```

### 1.2 The Pipeline: `Jenkinsfile`

Create the Jenkins pipeline file. This file must be called `Jenkinsfile` and it defines the "DevOps steps": pulling code, setting up Python, and running tests.

```groovy
pipeline {
    agent any
    stages {
        }
        stage('Build & Test') {
            steps {
                // We use a shell command to run our python script
                sh 'python3 app.py'
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}
```


## 2. Run Jenkins in Podman

```bash
# Run Jenkins in a Podman container 
podman run -d \
  --name jenkins-server \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

Display the container logs and scroll down to get the Jenkins GUI Web console password

```bash
podman logs jenkins-python
```

```text
*************************************************************
Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

[32-CHARACTER-CODE-HERE]

This may also be found at: /var/jenkins_home/secrets/initialAdminPassword
*************************************************************
```

## 3. Configure the Pipeline

1. **Open Jenkins:** Go to `http://localhost:8080` in your browser.
2. **Unlock:** Paste the password from the logs and select **"Install Suggested Plugins."**
3. **Create Job:** * Click **New Item**.
* Enter name: `Python-App-Pipeline`.
* Select **Pipeline** and click OK.


4. **Connect GitHub:**
* Scroll to the **Pipeline** section.
* Change "Definition" to **Pipeline script from SCM**.
* Select **Git**.
* Paste your **GitHub Repository URL**.
* Ensure the branch is correct (usually `*/main`).
* Click **Save**.


## 4. Run the Pipeline

Click **Build Now** on the left menu. Jenkins will:

1. **Clone** your code from GitHub.
2. **Execute** the `sh 'python3 app.py'` command defined in your `Jenkinsfile`.
3. **Report** success or failure in the **Stage View** dashboard.
























## 2. Run Jenkins in Podman

Create a custom image Jenkins that includes Python and Docker. The reason being that the default jenkins image does not inlude Python not Docker. And because we are building a Python application and pushing it to an image registry, we will need both Python and Docker installed in the image.

cat > Containerfile

```dockerfile
# Start from the standard Jenkins LTS image
FROM jenkins/jenkins:lts

# Switch to root user to install software
USER root

# Install Python 3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv docker.io zip && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the standard jenkins user
USER jenkins
```

Create the image

```bash
podman build -t python-jenkins .
```

Run the container by mounting the Podman socket when you start Jenkins, using the `-v /run/user/$(id -u)/podman/podman.sock:/var/run/docker.sock` parameter

```bash
# This allows the Jenkins container to 'borrow' your computer's Podman engine
podman run -d \
  --name jenkins-python \
  -p 8080:8080 \
  -v /run/user/$(id -u)/podman/podman.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  python-jenkins
```

Display the container logs and scroll down to get the Jenkins GUI Web console password

```bash
podman logs jenkins-python
```

```text
*************************************************************
Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

[32-CHARACTER-CODE-HERE]

This may also be found at: /var/jenkins_home/secrets/initialAdminPassword
*************************************************************
```


### Create Dockerfile.app (In GitHub)

Create "blueprint" for your application artifact.

### Create the Jenkinsfile

```groovy
pipeline {
    agent any
    environment {
        // Replace with your Docker Hub username
        DOCKER_HUB_USER = 'your-username'
        IMAGE_NAME = "python-jenkins-demo"
        REGISTRY_CREDENTIALS_ID = 'docker-hub-login' 
    }
    stages {
        stage('Build & Test') {
            steps {
                sh 'python3 app.py'
            }
        }
        stage('Create Docker Artifact') {
            steps {
                script {
                    // Build the image using the Dockerfile in the repo
                    appImage = docker.build("${DOCKER_HUB_USER}/${IMAGE_NAME}:${env.BUILD_NUMBER}")
                }
            }
        }
        stage('Push to Registry') {
            steps {
                script {
                    // Use credentials stored in Jenkins to log in and push
                    docker.withRegistry('', REGISTRY_CREDENTIALS_ID) {
                        appImage.push()
                        appImage.push('latest')
                    }
                }
            }
        }
    }
}
```
