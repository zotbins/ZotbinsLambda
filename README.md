# ZotbinsLambda

The ZotbinsLambda project organizes the Lambda functions used for manipulating the bin metric data from the deployed smart bins.

## Installation

First clone this project:
```bash
git clone "link"
```
In order to run this project, we'll need:
- The Serverless Framework
- Serverless Offline
- Serverless Python Requirements

To install Serverless Framework, run:
```bash
npm install serverless -g
```
This command installs serverless globally, so you won't need a separate serverless package for other npm projects.

To install Serverless Offline, run:
```bash
npm install serverless-offline --save-dev
```

To install Serverless Python Requirements:
```bash
sls plugin install -n serverless-python-requirements
```

To install the necessary python modules, run: 
```bash
pip install -r requirements.txt
```

## TimescaleDB Docker

Docker is used to be create a TimescaleDB database to test our data locally. To install, run:
```bash
docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg12
```
This creates a Docker named TimescaleDB that will run on port 5432. TimescaleDB utilizes PostgresSQL, so the password to access
the underlying PostgresSQL database remotely is just "password" since this docker database is just for local testing.

We can also directly access the PostgresSQL database by running:
```bash
docker exec -it timescaledb psql -U postgres
```

But it would be more convenient to create the tables by running the create_tables.py script. Just make sure that the docker container
has started by running:
```bash
docker start timescaledb
python create_tables.py
```

## Running the Lambda Locally

To run the project locally, use
```bash
sls offline
```

The project should be hot reloadable, so you should see changes after you save a file.

And we can then manipulate the data inside there.

# Helpful Links
- https://www.serverless.com/plugins/serverless-python-requirements
- https://www.serverless.com/blog/serverless-python-packaging
- https://stackoverflow.com/questions/6506578/how-to-create-a-new-database-using-sqlalchemy 