# Setup instruction

## GCP 

### Prerequisites
- GCP account
- installed [docker](https://docs.docker.com/compose/install/)
- installed [SDK](https://cloud.google.com/sdk/docs/install#installation_instructions)
```bash
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-377.0.0-linux-x86_64.tar.gz

```

- installed [terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- installed vscode

### Setup

**1. clone project localy**
```bash
git clone https://github.com/skibooj/de_zoomcamp_project.git`
```
**2. create GCP project**
insert name of project in bellow code and execute
```bash
PROJECT_ID= <insert name of project>
gcloud projects create $PROJECT_ID --set-as-default
gcloud auth application-default login
```
**3. Set the billing account for project**
- Go into the cloud console
- Go into billing -> Account Management
- Select the My Projects tab
- Click on the Actions button for the new project and Change Billing
- Select the proper billing account and save the change



```bash
gcloud services enable compute.googleapis.com`
```

 **4. Create a service account for Terraform and dowlonad creditionals**
 

**5. create env variables** 


**6. setup GCP infrastructure with Terraform**
in /terraform direction execute:
```terraform
terraform init
terraform plan
terraform apply
```

**7. create ssh key to VM**

https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12

https://itnadigital.notion.site/Terraform-GCP-VM-Instance-Brief-51b2019485de49c890dd06094ccc5ed9


**8. clone project on VM**
```bash
ssh de-wse-project
git clone https://github.com/skibooj/de_zoomcamp_project.git
# code to download all necessery library
```

**9. run docker**
```bash
docker-compose up`
```
**10. create port forwarding**
 - Open vscode 
 - 
**11. run airflow dag**