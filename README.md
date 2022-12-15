# TechTrends-Application Deployment to a Kubernetes Cluster
This is my solution for the first project of Udacity's Cloud Native Application Architecture Nanodegree Program. The goal is to enhance an application with endpoints for health & metrics and deploy it using a container orchestration tool, k3s, and open-source continuous integration & continuous deployment solutions (GitHub Actions, ArgoCD).

## Health- & Metrics-Endpoints

## Local Deployment with Docker

## Configuration of a Continuous Integration Pipeline with GitHub Actions
GitHub Actions is used as a tool for continuous integration: Every commit to the master branch of this repository triggers a build of the Docker Container Image and push to my [Dockerhub repository](https://hub.docker.com/repository/docker/stephanstu/techtrends). The workflow configuration can be found in

.github/workflows

The current status of the image is [![Health of the Image](https://github.com/StephanStu/TechTrends-Application-Deployment-to-Kubernetes/actions/workflows/techtrends-dockerhub.yml/badge.svg)](https://github.com/StephanStu/TechTrends-Application-Deployment-to-Kubernetes/actions/workflows/techtrends-dockerhub.yml)

## Boostrapping a Kubernetes Cluster with k3s

## Configuration of a Continuous Deployment Pipeline with ArgoCD

## Resources provided by Udacity:
**Course Homepage**: https://sites.google.com/udacity.com/suse-cloud-native-foundations/home

**Instructor**: https://github.com/kgamanji
