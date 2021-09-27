pipeline {
  agent { docker { image 'python:3.7.6' } }
  stages {
    stage('build') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
    stage('test') {
      steps {
        echo 'test completed'
      }
      post {
        always {
          echo 'postt activites'
        }
      }    
    }
  }
}
