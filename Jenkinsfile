pipeline {
    agent any
    stages {
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
