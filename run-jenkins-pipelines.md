To showcase the progression of a DevOps pipeline, we will move from simply "testing" the code to "packaging" it and finally "deploying" it.

---

### Step 1: Adding the "Artifact Creation" Stage

In DevOps, an **Artifact** is the finished "product" of your build (like a `.zip`, `.exe`, or `.jar`). We want to bundle our `app.py` so it can be saved by Jenkins and downloaded later.

**Updated `Jenkinsfile` (Version A):**

```groovy
pipeline {
    agent any
    stages {
        stage('Build & Test') {
            steps {
                sh 'python3 app.py'
            }
        }
        stage('Archive Artifact') {
            steps {
                // 1. Create a zip file containing our app
                sh 'zip my-python-app.zip app.py'
                
                // 2. Tell Jenkins to store this file in its 'Archive'
                archiveArtifacts artifacts: 'my-python-app.zip', fingerprint: true
            }
        }
    }
}

```

> **Note:** Since you are using a custom Jenkins image, you may need to run `apt-get install -y zip` inside your container (or add it to your Dockerfile) for the `zip` command to work.

**What this shows a beginner:** After the tests pass, Jenkins "saves" a specific version of the code that is ready to be moved elsewhere. You will see a "Last Successful Artifacts" link on the Jenkins project home page.

---

### Step 2: Adding the "Deployment" Stage

In a beginner demo, "Deployment" usually means moving that artifact to a "Production" environment. Since we are running in a container, we will simulate a deployment by "shipping" the file to a specific folder on the server.

**Complete `Jenkinsfile` (Version B):**

```groovy
pipeline {
    agent any
    
    // We define a variable for where 'Production' is
    environment {
        DEPLOY_PATH = '/var/jenkins_home/production_env'
    }

    stages {
        stage('Build & Test') {
            steps {
                sh 'python3 app.py'
            }
        }
        stage('Archive Artifact') {
            steps {
                sh 'zip my-python-app.zip app.py'
                archiveArtifacts 'my-python-app.zip'
            }
        }
        stage('Deploy to Production') {
            steps {
                // 1. Create the production folder if it doesn't exist
                sh "mkdir -p ${DEPLOY_PATH}"
                
                // 2. Unzip the artifact into the production folder
                sh "unzip -o my-python-app.zip -d ${DEPLOY_PATH}"
                
                echo "App successfully deployed to ${DEPLOY_PATH}"
            }
        }
    }
}
```

---

### Understanding the Flow

1. **Build & Test:** Proves the code works.
2. **Archive:** Creates the "package" (The Artifact).
3. **Deploy:** Puts the package where the users (or other servers) can access it.

### How to see the results:

* **Artifacts:** Go to your Jenkins Job dashboard. You will see a new section called **"Build Artifacts"** with your `.zip` file ready for download.
* **Deployment:** You can verify the "deployment" by looking inside your Podman container:
```bash
podman exec jenkins-python ls /var/jenkins_home/production_env

```



**Would you like me to show you how to add a "Post-Deployment" test to verify the app is actually running in that production folder?**
