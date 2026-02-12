pipeline {
    agent any
    agent {
        docker { image 'python:3.10-slim' } 
    }
    stages {
        /*
        stage('Checkout') {
            steps {
                git 'https://github.com/mnakib/python-jenkins-demo.git'
            }
        }
        */
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
