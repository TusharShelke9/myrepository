Jenkins pipeline

@Library("share")
def issueLinks
def testResult
def branchName
def buildVersion
def commitData
def commitHash

// Change this email address field to specify where success and failure notifications are sent
// Use a comma (',') to separate email addresses (eg. 'ianc@xyz.com , bob@yyz.org')

emailTo = 'pankajrawat@hkjc.org.hk'

// Change the Jenkins slave node according to the availability
buildnode = 'DEVBUILD53'

node(buildnode){
    try{
        properties([
          buildDiscarder(
                logRotator(artifactDaysToKeepStr: '10', artifactNumToKeepStr: '10', daysToKeepStr: '10', numToKeepStr: '20')),
            parameters([
            gitParameter(branch:'',
                        branchFilter:'origin/(.*)', 
                        defaultValue:'test', 
                        description:'', 
                        name:'BRANCH_NAME', 
                        quickFilterEnabled: true, 
                        selectedValue:'DEFAULT', 
                        sortMode:'ASCENDING_SMART', 
                        tagFilter:'*', 
                        listSize: '10',
                        type:'PT_BRANCH_TAG',
                    useRepository:'ssh://git@devgit01.corpdev.hkjc.com:7999/ites/ai.msp.git'),
            choice(choices: 'SNAPSHOT\nRELEASE', description:'SNAPSHOT OR RELEASE', name: 'snapshotorrelease'),
            booleanParam(defaultValue: true, description: '', name: 'enableSonarQube'),
            booleanParam(defaultValue: true, description: 'enableAquaScan or not', name: 'enableAquaScan'),
            booleanParam(defaultValue: true, description: 'enableBlackDuckScan or not', name: 'enableBlackDuckScan'),
            booleanParam(defaultValue: true, description: 'enableFortifyScan or not', name: 'enableFortifyScan'),
          ]),
        ])
  env.DOCKER_REPO="deopcard.corp.hkjc.com/ai-msp-docker-release-local/serving"
  stage ('Clone') {
            //clean workspace if needed
            //cleanWs() 
            //deleteDir() 
            checkout([$class: 'GitSCM', 
                            branches: [[name: "$BRANCH_NAME"]], 
                            userRemoteConfigs: [[url: 'ssh://git@devgit01.corpdev.hkjc.com:7999/ites/ai.msp.git']]]
                          )
                
            logOutput = sh returnStdout: true, script: 'git log -n 1'

                  // pass this for print content to jenkins console log
                  // this has print/println/printf methods
                  sCommit.processOut(this, logOutput)
            
            commitData = sCommit.getAll()
            commitHash = commitData.CommitId
            issueLinks = sCommit.getIssueLinks()      
            //branchName = sCommit.getBranchName(this)
            branchName = "${params.BRANCH_NAME}"
      }
      
  stage ('Docker Pytest Image Build - SNAPSHOT') {
        if ("${params.snapshotorrelease}" == 'SNAPSHOT')                                 
     	{      
          sh '''
              #!/bin/bash
              pwd
              #find / -type f -name "Dockerfile.testing"
              ls
              hostname -i
              docker build -t deopcard.corp.hkjc.com/ai-msp-docker-release-local/pytest-sampleapp:${BUILD_NUMBER} -f Dockerfile.testing .
              docker push deopcard.corp.hkjc.com/ai-msp-docker-release-local/pytest-sampleapp:${BUILD_NUMBER}
             '''
       }
  }
  stage ('Create Pytest Container and validate testcases - SNAPSHOT') {
        if ("${params.snapshotorrelease}" == 'SNAPSHOT')                                 
     	{      
          sh '''
              #!/bin/bash
              docker rm --force pytestapp
              docker pull deopcard.corp.hkjc.com/ai-msp-docker-release-local/pytest-sampleapp:${BUILD_NUMBER}
              docker run -itd  --name pytestapp deopcard.corp.hkjc.com/ai-msp-docker-release-local/pytest-sampleapp:${BUILD_NUMBER}
              sleep 10
              docker logs -f pytestapp 
              docker cp pytestapp:/tests/coverage.xml .
              pwd
             '''
       }
  }
  stage ('SonarQube analysis') {
    if (params.enableSonarQube){
        withSonarQubeEnv('SonarQube') {
          SONAR_PROJECT = "${env.JOB_NAME.replace('ITES/AI.MSP/','')}"
                  SONAR_VERSION = "${env.BUILD_NUMBER}-${BRANCH_NAME}"
          logOutput = sh ''' /opt/sonar-scanner-3.3.0.1492-linux/bin/sonar-scanner \
          -Dsonar.projectKey=ITES_AI.MSP_ \
          -Dsonar.sources=. \
          -Dsonar.python.coverage.reportPaths=/jenkins-slave/workspace/ES/AI.MSP/ITES_AI.MSP_Build/coverage.xml
        '''
        }
     }
   }
