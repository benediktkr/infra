pipeline {
    agent any
    options {
        timestamps()
        ansiColor("xterm")
        disableConcurrentBuilds()
    }
    stages {
        stage('lint') {
            steps {
                sh './lint.py'
            }
        }
    }
}
