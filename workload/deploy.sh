git clone https://ghproxy.com/https://github.com/microservices-demo/microservices-demo
cd microservices-demo

# application
kubectl create -f deploy/kubernetes/manifests
# opentracing
# kubectl apply -f deploy/kubernetes/manifests-zipkin/zipkin-ns.yaml -f deploy/kubernetes/manifests-zipkin

kubectl get pods --namespace="sock-shop"
