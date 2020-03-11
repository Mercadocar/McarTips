Task List to Finish POC deploy into k8s.

1 - Develop a way to create exchanges and queues when
helm install from scratch. Check bruno's python code.

2 - Each gRPC client on BFF is creating a channel on every
service endpoint call. Check ClienteService and adapt the
other services to maintain a single long-live channel.

3 - Find a better way to getting service´s host and IP
from pod's enviroment variables. Like in Pessoa's persistence
layer, we are getting the same host and IP in every Repo.
What about Helm Chart Templates? What if the service name
changes?

4 - We are pulling images from a public registry (dockerhub).
Our Apps are private. What should we do? Pay private on
dockerhub or go using Azure Image Registry. I vote on the second.
And whatever the choice, we need to configure helm to use it.