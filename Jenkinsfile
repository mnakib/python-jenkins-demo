pipeline {
    agent any
    environment {
        // The DOCKER_HUB instructuion replaces both DOCKER_HUB_USER and REGISTRY_CREDENTIALS_ID
        DOCKER_HUB = credentials('docker-hub-creds')
        IMAGE_NAME = "python-jenkins-demo"
        // Define the ID here so you can reuse it easily
        REGISTRY_ID = 'docker-hub-creds'
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
                    // Force the full name into a variable to ensure consistency
                    def fullImageName = "${DOCKER_HUB_USR}/${IMAGE_NAME}:${env.BUILD_NUMBER}"

                    // Build the image
                    appImage = docker.build(fullImageName)

                // DEBUG: List images to ensure it actually exists in the local daemon
                sh "docker images | grep ${IMAGE_NAME}"
                }
            }
        }
        stage('Push to Registry') {
            steps {
                script {
                    // Use credentials stored in Jenkins to log in and push
                    docker.withRegistry('', 'docker-hub-creds') {
                        appImage.push()
                        appImage.push('latest')
                    }
                }
            }
        }
    }
    post {
        always {
            // Best practice to remove the build workspace and local docker images to save space
            cleanWs()
            sh "docker rmi ${DOCKER_HUB_USR}/${IMAGE_NAME}:${env.BUILD_NUMBER} || true"
        }
    }
}
