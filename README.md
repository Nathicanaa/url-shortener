# url-shortener

A simple API for getting short url.

## Run Locally:
1. Clone this repo.
2. Create .env file with required credentials or set just set them into your environment. As an example you can use .env.sample
3. Run `docker-compose up --build`.


## Deploy to Cloud Run
1. Create Postgres instance in GCP, you can use terraform scripts in `terraform` folder.
To use terraform:

   1.1 Create `.tfvars` file with values for variables declared in [variable.tf](terraform%2Fvariable.tf).

   1.2 Run `terraform init` & `terraform apply`
3. Fill GitHub secrets with values declared in [cloud_run_deploy.yaml](.github%2Fworkflows%2Fcloud_run_deploy.yaml).
4. On every push to `master` branch that CI/CD will be triggered.
