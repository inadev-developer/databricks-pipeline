def DBTOKEN         = ""
def DBURL           = "https://dbc-3f01e141-ef44.cloud.databricks.com"
// def SCRIPTPATH      = "${GITREPO}/Automation/Deployments"
def GITREPOREMOTE   = "https://github.com/suprobhat/databricks-notebook"
def GITHUBCREDID    = "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"
def CURRENTRELEASE  = "main"
//def NOTEBOOKPATH    = "https://dbc-6a384387-6e96.cloud.databricks.com/#workspace/Users/anindya.das@inadev.com/Terraform/notebook-getting-started-etl-quick-start.py"
def NOTEBOOKPATH	  = "/Users/satya.saini@inadev.com/example"
def NOTEBOOKNAME	  = "Notebooktest"
// def LIBRARYPATH     = "${GITREPO}/Libraries"
def BUILDPATH       = "https://dbc-6a384387-6e96.cloud.databricks.com/#job/1090278327353974"
// def OUTFILEPATH     = "${BUILDPATH}/Validation/Output"
// def TESTRESULTPATH  = "${BUILDPATH}/Validation/reports/junit"
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
  nodeSelector:
    nodename: ops-node
  tolerations:
  - effect: NoSchedule
    key: nodetaints
    operator: Equal
    value: ops-nodegroup
  containers:
  - name: docker
    image: 618187721717.dkr.ecr.us-east-1.amazonaws.com/baseline-repository:docker-latest
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true 
    volumeMounts:  
    - mountPath: /var/run/docker.sock
      name: docker-sock          
  - name: ceebasictools
    image: 618187721717.dkr.ecr.us-east-1.amazonaws.com/baseline-repository:linux-basic-tools-latest
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true
  - name: gitcli
    image: 618187721717.dkr.ecr.us-east-1.amazonaws.com/baseline-repository:alpine-git
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true   
  - name: python
    image: python:3.9.16
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true    
  - name: kube
    image: 618187721717.dkr.ecr.us-east-1.amazonaws.com/baseline-repository:k8s-kubectl-latest
    command:
    - cat
    tty: true 
    imagePullPolicy: IfNotPresent
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
        stage ('Source Code Checkout') {
            steps {
                script {
                    checkout scm: [$class: 'GitSCM', userRemoteConfigs: [[url: "https://github.com/inadev-developer/databricks-pipeline.git", credentialsId: "inadev-github"]], 
                    extensions: [[$class: 'CloneOption', shallow: true, depth: 1], [$class: 'CheckoutOption', timeout: 30 ]], 
                    branches: [[name: "master"]]], poll: false                       
                }                          
            }
        }
        
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
                def data = "{\"name\": \"Testrun\", \"existing_cluster_id\": \"$CLUSTERID\", \"timeout_seconds\": 3600, \"max_retries\": 1, \"notebook_task\": {\"notebook_path\": \"$NOTEBOOKPATH\", \"base_parameters\": {} } }"
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
      				        echo "${DBURL}
      				        $TOKEN" | databricks configure --token

     					     # Configure Databricks Connect for testing
      			    	    echo "${DBURL}
      			    	    $TOKEN
      			    	    $CLUSTERID
      			    	    0
      			    	    15001" | databricks-connect configure
      			    	    databricks jobs configure --version=2.1
      			    	    cat ~/.databrickscfg
      			    	    databricks jobs list --output JSON
      			    	    databricks fs ls 
      			    	    databricks fs ls dbfs:/mnt/
      			    	    databricks clusters list
      			    	    #databricks workspace mkdirs "/src"
      			    	    databricks workspace import --language PYTHON --overwrite Notebooktest.py $NOTEBOOKPATH
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
