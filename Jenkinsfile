pipeline {
    agent any
    stages {
        /*
        stage('Checkout') {
            steps {
                git 'https://github.com/mnakib/python-jenkins-demo.git'
            }
        }
        */
        stage('Install Dependencies') {
            steps {
                script {
                    // Create and use a virtual environment
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate'
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Activate venv and run tests (e.g., using pytest)
                    sh '. venv/bin/activate'
                    sh 'pytest' 
                }
            }
        }
        stage('Run') {
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
