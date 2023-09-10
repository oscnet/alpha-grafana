# 中性量化管理面板的 Docker 镜像

## 布署和运行

1. 编辑 .env 文件
2. 将 grafana 的面板 json 文件放入 grafana/dashboards 目录下，缺省已经放了一些。
3. docker-compose up -d 
4. 稍等几分钟，等容器运行准备完成后，打开浏览器，输入网址 http://localhost:8899 , 初始用户名密码为：admin, admin,然后再设置 admin 密码后登录，选择实时持仓面板，就可以看到当前仓位了，其它数据一般要运行1个多小时后才能显示。

所有配置都在 .env 文件中。配置示例：
```
# 配置信息

# 1、帐户配置
# 使用不同的帐户名，可以配置多个帐户。 
# account_帐户名_cash 配置初始金额
# account_帐户名_apiKey 配置币安帐户 api 的 apiKey
# account 帐户名_secret 配置币安帐户 api 的 secret
# 例如我取一个帐户名为 yxd01, 则配置如下：

account_yxd01_cash=1000
account_yxd01_apiKey=ReUQ5erxopO3W0gS1Ll3leCn8112Osi9cTrFMz9lhqvJWEWBUoxVJmqDUlItpQci
account_yxd01_secret=dxDuKtA7W58zSak6rZdLXvivSkJicvu5jWgxY2VHrNPV5655mfj5Geo65xp2t1bl

# 2、配置钉钉提醒，如果有公众号的可以配置，没有的也可不管它
wechat_secret=FoJsxkyVOs
wechat_agentid=100
wechat_corpid=ww73

# 3、mysql 数据库配置，看需要修改
mysql_database=ns_data
mysql_password=3ctMcfmlKKPwwNaI

# 以下三个 mysql 配置一般不更改，如确实需要，需相应更改  docker-compose.yml 文件
mysql_user=root  
mysql_host=db    
mysql_port=3306
```

## 问题调试

### 重建 

docker rmi alpha-grafana-spider 
docker-compose up


## 更新

### 2023.9.10 更新 

* [unicorn-binance-websocket-api](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api) 到 1.46.1

* 更新 python-binance 到 1.0.19

## 已知问题

1. macOs M1 mysql 镜像问题。

   ~~~在 `docker-compose.yml` 中加入  `platform: linux/amd64`~~~
   已修复

2. grafana 运行时插件 `grafana-piechart-panel` 下载失败。
   
    网络问题，需要 fq 环境。

## 其它参考

### docker 使用 secret
* https://yeasy.gitbook.io/docker_practice/swarm_mode/secret
* https://developer.aliyun.com/article/91396
```bash
echo "Password4DB" | docker secret create db_password -
```

### grafana 配置

* [grafana config](https://github.com/cirocosta/sample-grafana)

* https://grafana.com/docs/grafana/latest/administration/configure-docker/

* https://riamf.github.io/posts/dockerized_grafana_setup/

* [compose 示例](https://github.com/docker/awesome-compose)

### 常用命令

Stop the container(s) using the following command:

`docker-compose down`

Delete all containers using the following command:

`docker rm -f $(docker ps -a -q)`

 Delete all volumes using the following command:

`docker volume rm $(docker volume ls -q)`

 Restart the containers using the following command:

`docker-compose up -d`