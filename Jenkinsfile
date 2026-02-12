pipeline {
    agent any
    stages {
        // This stage is commented as the repo cloning is done by Jenkins before running the pipeline
        /*
        stage('Checkout') {
            steps {
                git 'https://github.com/YOUR_USERNAME/python-jenkins-demo.git'
            }
        }
        */
        // Check the version of Python
        stage('Environment Check') {
            steps {
                sh 'python3 --version'
            }
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
