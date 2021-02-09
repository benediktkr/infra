pipeline {
    agent any
    options {
        timestamps()
        ansiColor("xterm")
        disableConcurrentBuilds()
    }

    stages {
        stage('build') {
            steps {
                sh 'docker build -t infra:lint .'
            }
        }

        stage('lint') {
            steps {
                sh 'docker run --rm infra:lint'
            }
        }
    }
    post {
        cleanup {
            cleanWs(deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true)
        }
    }
}
