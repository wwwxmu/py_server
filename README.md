supervisord -c supervisor.conf 通过配置文件启动supervisor
supervisorctl -c supervisor.conf status 察看supervisor的状态
supervisorctl -c supervisor.conf reload 重新载入 配置文件
supervisorctl -c supervisor.conf start py_server 启动指定/所有 supervisor管理的程序进程
supervisorctl -c supervisor.conf stop py_server 关闭指定/所有 supervisor管理的程序进程

### 设置supervisor开机自动启动
在/etc/systemd/system/supervisord.service文件中配置：
```
[Unit]
Description=Process Monitoring and Control Daemon
After=rc-local.service nss-user-lookup.target
[Service]
User=root
Type=forking
ExecStart=/home/py_server/venv/bin/supervisord -c /home/py_server/supervisor.conf
ExecStop=/home/py_server/venv/bin/supervisord  shutdown
ExecReload=/home/py_server/venv/bin/supervisord -c /home/py_server/supervisor.conf  reload
Restart=on-failure
RestartSec=42s
[Install]
WantedBy=multi-user.target
```
重载service
sudo systemctl daemon-reload
设置开机启动
systemctl enable supervisord
验证是否开机启动
systemctl is-enabled supervisord

nginx 配置图片目录
location /images{
      #处理静态文件夹中的静态文件
      expires      30d;
      alias /www/wwwroot/imgs.diystock.ai/images/;
}
