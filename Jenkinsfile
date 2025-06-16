pipeline {
  agent {
    docker {
      image 'python:3.12'
      args '-u root:root'
    }
  }

  environment {
    VENV_PATH = '.venv'
    POETRY_HOME = '/usr/local/bin/poetry'
  }

  stages {
    stage('Install Python') {
      steps {
        sh '''
          apt-get update
          apt-get install -y python3
        '''
      }
    }
    stage('Install Poetry') {
      steps {
        sh 'pip install poetry'
      }
    }
    stage('Install dependencies') {
      steps {
        sh 'poetry install'
      }
    }
    stage('Run Tests') {
      steps {
        sh 'poetry run pytest'
      }
    }
  }

  post {
    failure {
      echo 'Pipeline falhou! Corrija os testes.'
    }
    success {
      echo 'Pipeline passou! Tudo certo.'
    }
  }
}
