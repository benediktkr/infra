pipeline {
    agent any
    options {
        timestamps()
        ansiColor("xterm")
        disableConcurrentBuilds()
    }
    stages {
        stage('version') {
            steps {
                script {
                    env.VERSION = sh(script: "date -I", returnStdout: true).trim().replace("-",".")
                    currentBuild.description = env.VERSION
                }
            }
        }
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
