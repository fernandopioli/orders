pipeline {
agent any

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
        sh '''
          if ! command -v poetry > /dev/null; then
            curl -sSL https://install.python-poetry.org | python3 -
            export PATH="$HOME/.local/bin:$PATH"
          fi
        '''
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
