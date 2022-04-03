# Setup instruction

Below you will find instructions on how to set up your project. The whole instruction is shown on linux but for other operating systems the process will be very similar.

### **Prerequisites**
- GCP account 
- installed [docker](https://docs.docker.com/compose/install/)
- installed [SDK](https://cloud.google.com/sdk/docs/install#installation_instructions)
```bash
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-377.0.0-linux-x86_64.tar.gz

```

- installed [terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- installed vscode

### **Setup**

**1. clone project localy**
```bash
git clone https://github.com/skibooj/de_zoomcamp_project.git
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

**4. Create service account and create**
- Go to IAM and admin 
- Select Create service account 
- In first step insert sercive acoount name
- In second add bellow roles:
`viewer` `BigQuery Admin` `Storage Admin` `Storage Object Admin`
- You can skip third step by clicking button `done`

**5. dowload GCP key**
- At Service accounts tab click on the three dots next to service account you just created and choose `Manage keys`
- Click `add key` and `Create new key`
- choose JSON key type and dowload 

**6. move GCP key to `/.google/credentials/google_credentials.json`**

At the location where the key was downloaded, follow the steps below:

```bash
mkdir ~/.google/credentials/
mv your-key.json ~/.google/credentials/google_credentials.json
```
**7. Set environment variable to point to your downloaded GCP keys:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/.google/credentials/google_credentials.json"
gcloud auth application-default login
```

**8. Enable these APIs:**
- https://console.cloud.google.com/apis/library/iam.googleapis.com
- https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
- https://console.cloud.google.com/apis/library/compute.googleapis.com
```bash
gcloud services enable compute.googleapis.com`
```

**9. setup GCP infrastructure with Terraform**
in de_zoomcamp_project/terraform direction execute:

```python
terraform init
terraform plan
#here terraform should you ask for GCP project id and path to credentials
terraform apply
```

now you should have:
- one bucket
- one dataset in BQ
- one instance of VM

10. create ssh connection to VM

- execute bellow code
```bash
mkdir ~/.ssh
cd ~/.ssh
ssh-keygen -t rsa -f gpc -C <yourname> -b 2048
```
- In GCP select Compute Engine > Metadata > SSH KEYS > ADD SSK KEY
- open publick key in /.ssh directory
` cat gcp.pub` 
- copy entire content of gcp.pub file to opened tab in GCP in SSH KEY 1 field and next click SAVE on the bottom 

11. create VM instance 
- Go to Compute Engine > VM instances and click create instance
- select name
- select the same region as in previous configurations
- series: E2
- Machine type: e2-medium
- In Boot disk section click change and select:
- Operating system: Ubuntu
- Version: 20.04 LTS
and now click CREATE

12. config SSH

```bash
cd ~/.ssh
touch config
nano config
```
complete the file as below

```bash
Host wse-vm #vm name selected in the previous step
	Hostname 104.122.49.123 # External IP from GCP VM instances tab
    User <your name>
    IdentityFile ~/.ssh/gcp
```

now you can connect to connect to vm instace typing in shell, remember to update hostname every time when you stop and run instance of VM

```
ssh wse-vm
```

13. setup VM 

in this step we will be configure VM to handle with pipline 
**Anaconda**
```bash
ssh wse-vm

wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
bash Anaconda3-2021.11-Linux-x86_64.sh 
# log out and log in 
rm Anaconda3-2021.11-Linux-x86_64.sh
```
**docker**
```
sudo apt-get update
sudo apt-get install docker.io
```
[guides/docker-without-sudo.md at main · sindresorhus/guides (github.com)](https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md)

`docker run hello-world`

**install docker-compose**

```
mkdir bin
cd bin
wget https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -O docker-compose
chmod +x docker-compose
cd 
nano ~/.bashrc
```
add these line 

```
export PATH="${HOME}/bin:${PATH}"
```

**add credentials on VM**
back to locall machine
```
 cd ~/.google/credentials/
 sftp wse-vm
 mkdir .google/credentials/
 cd .google/credentials/
 put google_credentials.json
```
logout from stfp `ctrl + D`

```
ssh wse-vm
export GOOGLE_APPLICATION_CREDENTIALS=~/.google/credentials/google_credentials.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```


Follow the guide. Logout and login > close connection with ctrl d.
14. setup VScode to work with remote machine
- install `Remote - SSH` extention
- `Ctrl + Shift + P` and type `Connect to 
**5. create env variables** 


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