pipeline {
    agent any
    environment {
        // Replace with your Docker Hub username
        DOCKER_HUB_USER = 'mouradn81'
        IMAGE_NAME = "python-jenkins-demo"
        REGISTRY_CREDENTIALS_ID = 'docker-hub-creds' 
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
