def DBTOKEN         = ""
def DBURL           = "https://dbc-3f01e141-ef44.cloud.databricks.com"
def GITREPOREMOTE   = "https://github.com/suprobhat/databricks-notebook"
def GITHUBCREDID    = "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"
def CURRENTRELEASE  = "main"
def NOTEBOOKPATH    = "/Users/joy.chattopadhyay@inadev.com/example"
def NOTEBOOKNAME    = "Notebooktest"
def BUILDPATH       = "https://dbc-6a384387-6e96.cloud.databricks.com/#job/1090278327353974"
def WORKSPACEPATH   = "https://dbc-3f01e141-ef44.cloud.databricks.com"
def DBFSPATH        = "databricks-testing-2oxiui-mountbucket"
def CLUSTERID       = "0105-073813-ry62hsnp"
def CONDAPATH       = "/opt/conda/bin/conda"
def CONDAENV        = "jenkins"

pipeline {
    agent {
        kubernetes {
            defaultContainer 'jnlp'
            yaml """
apiVersion: v1
kind: Pod
metadata:
labels:
  component: ci
spec:
  containers:
  - name: python
    image: python:3.9.16
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true
    volumeMounts:
    - name: docker-sock
      mountPath: /var/run/docker.sock    
  volumes:
    - name: docker-sock
      hostPath:
        path: /var/run/docker.sock
"""
        }
    }
    stages {
        // stage ('Source Code Checkout') {
        //     steps {
        //         script {
        //             checkout scm: [$class: 'GitSCM', userRemoteConfigs: [[url: "https://github.com/inadev-developer/databricks-pipeline.git", credentialsId: "inadev-github"]], 
        //             extensions: [[$class: 'CloneOption', shallow: true, depth: 1], [$class: 'CheckoutOption', timeout: 30 ]], 
        //             branches: [[name: "master"]]], poll: false                       
        //         }                          
        //     }
        // }
        
        stage ('Notebook create') {
            steps {
                script {
                    sh """
                        ls -la
                    """
                }                          
            }
        }
        
        stage("Job JSON File") {
          steps {
            container('python') {
              script {
                def data = "{\"name\": \"Testrun\", \"existing_cluster_id\": \"${env.DATABRICKS_CLUSTER_ID}\", \"timeout_seconds\": 3600, \"max_retries\": 1, \"notebook_task\": {\"notebook_path\": \"${env.DATABRICKS_NOTEBOOK_PATH}\", \"base_parameters\": {} } }"
                writeFile(file: 'job.json', text: data)
                sh """
                  cat job.json
                """
              }
            }
          }
        }
        stage ('Setup') {
            steps {
                container('python') {
                    script {
                        withCredentials([string(credentialsId: 'DBTOKEN', variable: 'TOKEN')]) {
                            sh """
                              apt update
                              apt install jq -y
                              #!/bin/bash
                              # Configure Conda environment for deployment & testing
                              #export PATH="/home/username/miniconda/bin:$PATH"
                              #conda -V
                              python -V
                              #which conda
                              #conda env list
                              #activate base
                              pip3 install requests
                              pip3 install databricks-connect
                              pip3 install databricks-cli
                              pip3 install pytest
                              
                              # Configure Databricks CLI for deployment
                              echo "${env.DATABRICKS_WORKSPACE_URL}
                              $TOKEN" | databricks configure --token
                              # Configure Databricks Connect for testing
                              echo "${env.DATABRICKS_WORKSPACE_URL}
                              $TOKEN
                              ${env.DATABRICKS_CLUSTER_ID}
                              0
                              15001" | databricks-connect configure
                              databricks jobs configure --version=2.1
                              cat ~/.databrickscfg
                              databricks jobs list --output JSON
                              databricks fs ls 
                              databricks fs ls dbfs:/mnt/
                              databricks clusters list
                              #databricks workspace mkdirs "/src"
                              databricks workspace import --language PYTHON --overwrite Notebooktest.py ${env.DATABRICKS_NOTEBOOK_PATH}
                              #databricks fs cp dbfs:/mnt/ dbfs:/tmp/demo/ --recursive --overwrite
                              #databricks fs ls dbfs:/tmp/demo/experiments
                              JOB_ID=\$(databricks jobs create --json-file job.json | jq -r '.job_id' )
                              databricks jobs run-now --job-id \$JOB_ID
                          """
                        }
                    }
                }
            }
        }
    }
}
