## 有用的 shell 命令

1. 删除指定命名空间下所有含有 `service` 的 pod:
    ```shell
   kubectl get pods -n hx-test | grep service | awk -F ' ' '{print $1}' | xargs kubectl delete pods -n hx-test
    ```
2. 清理镜像：
   ```shell
   docker image list | grep service | grep latest | awk -F ' ' '{print $1}' | xargs docker image rm
   ```
