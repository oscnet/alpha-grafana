# 中性量化管理面板的 Docker 镜像

## 布署和运行

1. 编辑 .env 文件
2. 将 grafana 的面板 json 文件放入 grafana/dashboards 目录下，缺省已经放了一些。
3. docker-compose up -d 
4. 稍等几分钟，等容器运行准备完成后，打开浏览器，输入网址 http://localhost:8899 , 设置 admin 密码后登录，选择实时持仓面板，就可以看到当前仓位了。

所有配置都在 .env 文件中。配置示例：
```
# 配置帐户，使用 account_帐户名 进行多帐户配置，以下除 mysql_port,mysql_host,mysql_user 外都可以自由更改
account_psy1_cash=100
account_psy1_apiKey=RxVJmqDUlItpQci
account_psy1_secret=dGeo65p2t1bl

account_psy2_cash=100
account_psy2_apiKey=RxVJmqDUlItpQci
account_psy2_secret=dGeo65p2t1bl

# 配置钉钉提醒，如果有公众号的可以配置，没有的也可不管它
wechat_secret=FoJsxkyVOs
wechat_agentid=100
wechat_corpid=ww73

# mysql 数据库配置，看需要修改
mysql_database=ns_data
mysql_password=3ctMcfmlKKPwwNaI
mysql_user=root
mysql_host=db
mysql_port=3306
```

## 已知问题

~~~1. macOs M1 mysql 镜像问题。~~~

   ~~~在 `docker-compose.yml` 中加入  `platform: linux/amd64`~~~
   已修复

2. grafana 运行时插件 `grafana-piechart-panel` 下载失败。
   
    网络问题，需要在 fq 环境。

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