pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'pip install flask'
                sh 'pip install mysql-connector-python'
                sh 'pip install flask_login'
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
            sh 'sudo systemctl restart api.service'
            sh 'sudo systemctl restart simulator.service'
        }
    }   
}