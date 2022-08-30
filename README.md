# k8s-flagger

### Configure cluster
#### Install istio
```BASH
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.14.3
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y
```
#### Install prometheus
```BASH
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.10/samples/addons/prometheus.yaml
```
### Install Flagger
```BASH
helm repo add flagger https://flagger.app
kubectl apply -f https://raw.githubusercontent.com/fluxcd/flagger/main/artifacts/flagger/crd.yaml
helm upgrade -i flagger flagger/flagger --namespace=istio-system --set crd.create=false --set meshProvider=istio --set metricsServer=http://prometheus:9090
```
### Install Grafana
```BASH
helm upgrade -i flagger-grafana flagger/grafana --namespace=istio-system --set url=http://prometheus.istio-system:9090 --set user=admin --set password=change-me
kubectl patch svc flagger-grafana -n istio-system -p '{"spec": {"type": "NodePort"}}'
kubectl -n istio-system get svc
```
### Install Kiali
```BASH
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.14/samples/addons/kiali.yaml
kubectl patch svc kiali -n istio-system -p '{"spec": {"type": "NodePort"}}'
```
###Name pod from istio-system namespaces                                    
flagger-5c8658c64-jplrh                 
flagger-grafana-6594969455-lhwbk        
istio-egressgateway-56b4ddcfd6-9n5zb    
istio-ingressgateway-76cd944566-g2d4k   
istiod-56b77cf5d6-b59xs                 
kiali-748d5cdbfc-blcsp                  
prometheus-69f7f4d689-cvrcx             

### Deploy app
Создаем namespace test и тегируем его для inject istio side car
```BASH
kubectl create ns test
kubectl label namespace test istio-injection=enabled
```
Деплоим app в кластер. Целевой namespace test.
```BASH
kubectl apply -f https://raw.githubusercontent.com/geksogen/k8s-flagger/master/k8s_cluster/deployment.yaml
```
Проверяем приложение
```BASH
kubectl -n test run -i -t nginx --rm=true --image=nginx -- bash
```
```BASH
curl -X GET http://appdeploy:5000
curl -X GET http://appdeploy:5000/return_version
```

### Patch istio-ingressgateway to nodeport
```BASH
kubectl patch svc -n istio-system istio-ingressgateway --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'
```