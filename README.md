# TechTrends-Application Deployment to a Kubernetes Cluster
This is my solution for the first project of Udacity's Cloud Native Application Architecture Nanodegree Program. The goal is to enhance an application with endpoints for health & metrics and deploy it using a container orchestration tool - k3s - and open-source continuous integration & continuous deployment solutions (GitHub Actions, ArgoCD).
The following sections wrap up what can be found in this repository and it's changes compared to the initial [fork](https://github.com/udacity/nd064_course_1/tree/main/project).

## Health- & Metrics-Endpoints, Advanced Logging
The initial application does not have endpoints that can serve as liveness probes and metrics revealing load/traffic/consumption of the service. Two endpoints have been added: One endpoint revealing health of the application and one endpoint returning metrics. Relevant metrics are:

* Total amount of posts in the database
* Total amount of connections to the database.

The health-endpoint can be reached at /healthz. In *app.py* the implementation reads like this:

```python
@app.route('/healthz', methods=['GET'])
def get_health():
    response = app.response_class(
            response=json.dumps({"result": "OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    app.logger.debug('Health request successful!')
    return response
```

The metrics-endpoint can be reached at /healthz. In *app.py* the implementation reads like this:

```python
@app.route('/metrics', methods=['GET'])
def get_metrics():
    global post_count
    global db_connection_count
    post_count = get_post_count()
    response = app.response_class(
            response=json.dumps({"db_connection_count": db_connection_count, "post_count": post_count}),
            status=200,
            mimetype='application/json'
    )
    app.logger.debug('Metrics request successful!')
    return response
```

Advanced logging is achieved by using the logging package and the sys package

```python
import logging, sys
```

The following handlers post logging information to STDERR and STDOUT:

```python
stdout_handler = logging.StreamHandler(stream=sys.stdout) # stdout handler `
stderr_handler = logging.StreamHandler(stream=sys.stderr) # stderr handler
```
The following handler post logging information to a file:

```python
file_handler = logging.FileHandler(filename='app.log')
```

One can wrap the handlers in a list and pass it to the logging-configuration like so:

```python
format_output = '%(levelname)s:%(name)s:%(asctime)s, %(message)s'
logging.basicConfig(format=format_output, level=logging.DEBUG, handlers=create_logging_handlers())
```

Here, the log-level is DEBUG. Logging a piece of information is now achieved by e.g.

```python
app.logger.debug('Health request successful!')
```

The application now logs different events to STDERR, STDOUT and the file *app.log*.

## Local Deployment with Docker
The application can be launched and tested locally with [Docker](https://docs.docker.com/get-docker/). Instructions to run the application are kept in the file

docker_commands

Note, that the following command allows to identify running containers

```console
docker ps
```

The container-id used in the file might be different, so this line will not work on another host than mine

```console
docker exec -it c2c2ec878416 /bin/bash
```

The command above allows one to *ssh-into* the container.

## Configuration of a Continuous Integration Pipeline with GitHub Actions
GitHub Actions is used as a tool for continuous integration: Every commit to the master branch of this repository triggers a build of the Docker Container Image and push to my [Dockerhub repository](https://hub.docker.com/repository/docker/stephanstu/techtrends). The workflow configuration can be found in

.github/workflows

The current status of the image is [![Health of the Image](https://github.com/StephanStu/TechTrends-Application-Deployment-to-Kubernetes/actions/workflows/techtrends-dockerhub.yml/badge.svg)](https://github.com/StephanStu/TechTrends-Application-Deployment-to-Kubernetes/actions/workflows/techtrends-dockerhub.yml)

## Boostrapping a Kubernetes Cluster with k3s

## Configuration of a Continuous Deployment Pipeline with ArgoCD

## Resources provided by Udacity:
This project was rated *passed* on 10-December-2022 by Udacity. The following resources have been provided initially:

**Course Homepage**: https://sites.google.com/udacity.com/suse-cloud-native-foundations/home

**Instructor**: https://github.com/kgamanji
