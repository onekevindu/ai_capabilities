# 🐳 本容器构建方法

## ✅ 一、安装 Docker 并配置代理

### 1. 安装 Docker

请前往 [Docker 官网](https://docs.docker.com/get-docker/) 选择对应系统安装。

### 2. 设置代理环境变量（推荐设置为全局）

```shell
export http_proxy=http://192.168.31.92:7890
export https_proxy=http://192.168.31.92:7890
```

### 3. 添加 NVIDIA Container Toolkit 仓库

```shell
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
&& curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add - \
&& curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### 4. 修改 Docker 的配置文件（配置代理）

```ini
[Service]
Environment="HTTP_PROXY=http://192.168.31.92:7890"
Environment="HTTPS_PROXY=http://192.168.31.92:7890"
Environment="NO_PROXY=localhost,127.0.0.1,.example.com"
```

> 配置文件一般为 `/etc/systemd/system/docker.service.d/http-proxy.conf`，重启 Docker 生效：
> `sudo systemctl daemon-reexec && sudo systemctl restart docker`

---

## 🧊 二、拉取基础镜像

> 本项目使用基础镜像：`pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel`

```shell
docker pull pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel
```

---

## 🚀 三、启动容器

```shell
docker run -d \
  --gpus all \
  -v /data:/root/.cache/huggingface \
  --network=host \
  --name pytorch2.5.1_cuda12.4 \
  pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel \
  tail -f /dev/null
```

进入容器：

```shell
docker exec -it pytorch2.5.1_cuda12.4 bash
```

---

## 🛠️ 四、配置 SSH（用于远程开发）

### 安装 SSH 服务：

```shell
apt update
apt install -y vim openssh-server
vim /etc/ssh/sshd_config
```

### 修改配置：

```yaml
Port 8022                   # 修改端口为 8022
PermitRootLogin yes         # 允许 root 登录
PasswordAuthentication yes  # 启用密码认证
```

### 设置密码并启动 SSH：

```shell
passwd root
service ssh restart
```

---

## 🧬 五、设置默认 Conda

```shell
echo 'export PATH=/opt/conda/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```# ai_capabilities
