pipeline {
    agent any
    environment {
        // The DOCKER_HUB instructuion replaces both DOCKER_HUB_USER and REGISTRY_CREDENTIALS_ID
        DOCKER_HUB = credentials('docker-hub-creds')
        IMAGE_NAME = "python-jenkins-demo"
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
                    appImage = docker.build("${DOCKER_HUB_USR}/${IMAGE_NAME}:${env.BUILD_NUMBER}")
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
    post {
        always {
            cleanWs()
        }
    }
}
