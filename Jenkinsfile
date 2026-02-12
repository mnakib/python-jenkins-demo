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
