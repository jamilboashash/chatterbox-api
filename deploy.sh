#! /bin/bash

# 1. Your Git repository will be checked out locally.
# 2. AWS credentials will be copied into your repository in the top-level directory, in a file called credentials.
# 3. The script deploy.sh in the top-level of the repository will be run.
# 4. The deploy.sh script must create a file named api.txt which contains the URL where your API is deployed to.
# 5. We will run automated functionality and load-testing on the URL provided in the api.txt file.

touch api.txt
# URL = deploy instance using terraform and return URL
terraform apply -auto-approve
echo "${URL}" > api.txt

