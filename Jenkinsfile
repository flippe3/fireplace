pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'pip install flask'
                sh 'pip install mysql-connector-python'
            }
        }
        stage('test') {
            steps {
                sh 'python3 test.py'
            }
        }
        
    }
    post {
        success {
            sh 'sudo systemctl restart app.service'
        }
    }   
}