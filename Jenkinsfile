pipeline {
    agent any
    stages {
        /*
        stage('Checkout') {
            steps {
                git 'https://github.com/YOUR_USERNAME/python-jenkins-demo.git'
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
