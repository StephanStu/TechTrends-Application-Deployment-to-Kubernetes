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
The following handler posts logging information to a file:

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

## Bootstrapping a Kubernetes Cluster with k3s
In this project, a Kubernetes Cluster is bootstrapped on a [locally](https://www.virtualbox.org/wiki/Downloads) hosted virtual machine. The machine is created using [Vagrant](https://developer.hashicorp.com/vagrant/downloads). Clone this repository, cd into the directory and create the virtual machine by running

```console
vagrant up
```

The Kubernetes Cluster is deployed as part of the machine-bring up. In the Vagrantfile that instructs Vagrant in the machine-creation process, find these lines, that deploy the Kubernetes Cluster

```console
curl -sfL https://get.k3s.io | sh -
```

Once the virtual machine is created *ssh-into* it by

```console
vagrant ssh
```

Then deploy the application by creating the files contained in the folder

kubernetes

Then deploy the application by running

```console
kubectl apply -f namespace.yaml
kubectl apply -f deploy.yaml
kubectl apply -f service.yaml
```

Note: The virtual machine can be terminated and removed from the host by

```console
vagrant destroy
```

This may save some disc space.

## Configuration of a Continuous Deployment Pipeline with ArgoCD
Following the instructions given at [here](https://argo-cd.readthedocs.io/en/stable/getting_started/#1-install-argo-cd), ArgoCD is deployed in the Kubernetes Cluster by running  

```console
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Once the ArgoCD-Containers have reached the running state (in the argocd-namespace!), the password for accessing the Continuous Deployment-UI is catched by

```console
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

Before running this command, a port for accessing ArgoCd has to be exposed - an instance of a NodePort-Service needs to be created. To do so, create a file called 'argocd-server-nodeport.yaml' and fill it with these lines

```yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
  labels:
    app.kubernetes.io/component: server
    app.kubernetes.io/name: argocd-server
    app.kubernetes.io/part-of: argocd
  name: argocd-server-nodeport
  namespace: argocd
spec:
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 8080
    nodePort: 30007
  - name: https
    port: 443
    protocol: TCP
    targetPort: 8080
    nodePort: 30008
  selector:
    app.kubernetes.io/name: argocd-server
  sessionAffinity: None
  type: NodePort
```

Then, in the same directory run

```console
kubectl apply -f argocd-server-nodeport.yaml
```

Now access ArgoCD at http://192.168.50.4:30007 - Ip-Address as defined in the Vagrantfile and port oas defined in the NodePort-Service-Manifest given above.

To deploy an application using ArgoCD, run

```console
kubectl apply -f helm-techtrends-prod.yaml
```

or

```console
kubectl apply -f helm-techtrends-staging.yaml
```

Both custom resource definitions (CRD's) will deploy the applications with a set of replicas and resources in the cluster.

## Resources provided by Udacity:
This project was rated *passed* on 10-December-2022 by Udacity. The following resources have been provided initially:

**Course Homepage**: https://sites.google.com/udacity.com/suse-cloud-native-foundations/home

**Instructor**: https://github.com/kgamanji
