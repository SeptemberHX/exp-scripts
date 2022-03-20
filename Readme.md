## 有用的 shell 命令

1. 删除指定命名空间下所有含有 `service` 的 pod:
    ```shell
   kubectl get pods -n hx-test | grep service | awk -F ' ' '{print $1}' | xargs kubectl delete pods -n hx-test
    ```
2. 清理镜像：
   ```shell
   docker image list | grep service | grep latest | awk -F ' ' '{print $1}' | xargs docker image rm
   ```

## 脚本

1. `k8s.py`: 参数给定部署方案的 json 格式文件，并部署到特定命名空间中。注意方案的键值对均是下标，需要从下标还原回节点、服务名称
2. `users.py`: 使用 `threading` 模拟用户请求，并使用日志输出记录请求发起时间、响应耗时等。