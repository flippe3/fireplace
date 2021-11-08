pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'pip install flask'
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
            sh 'python3 app.py'
        }
    }   
}