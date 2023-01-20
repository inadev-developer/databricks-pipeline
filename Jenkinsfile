def NOTEBOOKNAME    = "Notebooktest"
def FILENAME = "Notebooktest.py"

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
  - name: aws-cli
    image: amazon/aws-cli
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true
    volumeMounts:
    - name: docker-sock
      mountPath: /var/run/docker.sock
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
        stage ('CSV upload') {
          steps {
            container('aws-cli') {
              script {
                sh """
                  aws s3 cp allergies.csv s3://${env.DATABRICKS_MOUNT_BUCKET}/
                """
              }                          
            }
          }  
        }           
        stage ('Update Mount path in code') {
            steps {
                script {
                    sh """
                        sed -i 's#update_mount_path#${env.DATABRICKS_MOUNT_PATH}#g' ${FILENAME}
                    """
                }                          
            }
        }
        
        stage("Job JSON File") {
          steps {
            container('python') {
              script {
                def data = "{\"name\": \"Testrun\", \"existing_cluster_id\": \"${env.DATABRICKS_CLUSTER_ID}\", \"timeout_seconds\": 3600, \"max_retries\": 1, \"notebook_task\": {\"notebook_path\": \"${env.DATABRICKS_NOTEBOOK_PATH}/$NOTEBOOKNAME\", \"base_parameters\": {} } }"
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
                              databricks workspace import --language PYTHON --overwrite ${FILENAME} ${env.DATABRICKS_NOTEBOOK_PATH}/$NOTEBOOKNAME
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
