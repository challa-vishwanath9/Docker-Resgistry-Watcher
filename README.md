# Docker-Resgistry-Watcher
This Git repo has code for docker registry watcher which automates updates in kubenertes based on image tags in Docker Hub.

# Steps
1) Install Minikube and Docker Desktop
2) Start the minikibe
   ```minikube start```
3)  Create and push a image to Docker Hub with name <your_username>/docker-watcher:latest (also change your username in docker_watcher.py script)
   ```
docker login

# Build the image
docker build -t <your-dockerhub-username>/docker-watcher:latest .

# Push it to Docker Hub
docker push <your-dockerhub-username>/docker-watcher:latest
```
5)  Apply the relevant yaml files
  ```
kubectl apply -f deployment-manager-role.yaml
kubectl apply -f deployment-manager-rolebinding.yaml
kubectl apply -f nginx-deployment.yaml
kubectl apply -f docker-watcher-cronjob.yaml
```
6)  Now check the logs of deployment and cron jobs
```
kubectl describe deployment nginx-deployment
kubectl get pods
kubectl logs jobs/<latest_cronjobid>
```
This completes the basic setting of automatic watcher

# To test the watcher
1) change the tag of image and push it to the docker
  ```
docker images
docker tag <image_id> <your_username>/docker-watcher:newtag
docker push <your_username>/docker-watcher:newtag
```

3) wait until new cronjob has been executed

4) Check logs of latest cronjob
   ```
   kubectl get pods
   kubectl logs jobs/<latest_cronjobid>
   ```

6) Check the Description of Deployment and verify image used is changed to newtag or not
   ```
   kubectl describe deployment nginx-deployment
   ```

   
