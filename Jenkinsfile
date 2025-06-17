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
    DJANGO_SETTINGS_MODULE = "web.config.settings.${env.BRANCH_NAME == 'main' ? 'prod' : env.BRANCH_NAME}"
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
    stage('Lint & Format') {
      steps {
        sh 'poetry run ruff check --fix .'
        sh 'poetry run ruff format .'
      }
    }
    stage('Run Tests') {
      steps {
        sh 'poetry run pytest --junitxml=reports/pytest.xml'
        junit 'reports/pytest.xml'
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
