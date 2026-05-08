# 🚀 部署指南

本文档介绍如何将 CampusCat Manager 部署到各种环境。

---

## 📋 目录

- [腾讯云轻量服务器部署](#腾讯云轻量服务器部署)
- [GitHub Pages部署](#github-pages部署)
- [本地开发环境](#本地开发环境)

---

## 腾讯云轻量服务器部署

### 前提条件

- 腾讯云轻量服务器（已购买）
- 服务器已安装 Nginx
- 有 root 或 sudo 权限

### 部署步骤

#### 1. 连接服务器

```bash
ssh root@YOUR_SERVER_IP
```

#### 2. 创建部署目录

```bash
mkdir -p /var/www/html/campuscat
```

#### 3. 上传文件

**方式一：使用 SCP**

在本地执行：

```bash
scp -r demo/* root@YOUR_SERVER_IP:/var/www/html/campuscat/
```

**方式二：使用 SFTP 工具**

使用 WinSCP 或 FileZilla 连接服务器，将 `demo/index.html` 上传到 `/var/www/html/campuscat/`。

#### 4. 设置权限

```bash
chmod -R 755 /var/www/html/campuscat/
```

#### 5. 配置 Nginx

编辑 Nginx 配置文件：

```bash
nano /etc/nginx/sites-available/campuscat
```

添加以下内容：

```nginx
server {
    listen 80;
    server_name YOUR_SERVER_IP;
    
    location /campuscat {
        alias /var/www/html/campuscat;
        index index.html;
        try_files $uri $uri/ =404;
    }
}
```

启用配置：

```bash
ln -s /etc/nginx/sites-available/campuscat /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 6. 访问

打开浏览器访问：

```
http://YOUR_SERVER_IP/campuscat/
```

---

## GitHub Pages 部署

> 推荐方式 — 完全免费，每次 push 自动部署

### 方式一：GitHub Actions 自动部署（推荐）

仓库已配置 GitHub Actions 工作流，push 到 main 分支后自动部署到 GitHub Pages。

#### 步骤

1. **首次启用 GitHub Pages**
   - 进入仓库 **Settings → Pages**
   - Source 选择 **GitHub Actions**
   - 保存

2. **推送代码**（工作流文件 `.github/workflows/deploy.yml` 已就绪）
   - 推送后进入仓库 **Actions** 标签页查看部署状态
   - 约 1-3 分钟后完成

3. **访问**
   ```
   https://daka-agent.github.io/CampusCat-/demo/
   ```

> 💡 之后每次 push 到 main 分支都会自动重新部署，无需手动操作。

### 方式二：手动部署（不推荐）

1. **Fork 本仓库** 到您的 GitHub 账号
2. **启用 GitHub Pages**
   - 进入仓库 Settings → Pages
   - Source 选择 "Deploy from a branch"
   - Branch 选择 "main" / "root"
   - 点击 Save
3. **访问**
   ```
   https://YOUR_USERNAME.github.io/CampusCat-/demo/
   ```

---

## 本地开发环境

### 方式一：直接打开

直接用浏览器打开 `demo/index.html` 文件。

### 方式二：Python HTTP服务器

```bash
cd demo

# Python 3
python -m http.server 8080

# Python 2
python -m SimpleHTTPServer 8080
```

访问：http://localhost:8080

### 方式三：Node.js http-server

```bash
# 安装 http-server
npm install -g http-server

# 启动服务器
cd demo
http-server -p 8080
```

访问：http://localhost:8080

### 方式四：VS Code Live Server

1. 安装 VS Code 扩展 "Live Server"
2. 右键点击 `index.html`
3. 选择 "Open with Live Server"

---

## 🔒 HTTPS配置（可选）

### 使用 Certbot 申请免费 SSL 证书

```bash
# 安装 Certbot
apt-get install certbot python3-certbot-nginx

# 申请证书
certbot --nginx -d your-domain.com

# 自动续期测试
certbot renew --dry-run
```

---

## 📝 配置说明

### 环境变量（未来扩展）

创建 `.env` 文件：

```env
# API配置
API_BASE_URL=https://api.example.com
API_KEY=your-api-key

# 腾讯云配置
TENCENT_CLOUD_ID=your-cloud-id
TENCENT_CLOUD_SECRET=your-cloud-secret

# 其他配置
DEFAULT_CAMPUS=default
```

---

## 🔧 故障排查

### 问题1：无法访问页面

**检查清单：**
- [ ] Nginx 是否运行：`systemctl status nginx`
- [ ] 防火墙是否开放80端口：`ufw status`
- [ ] 文件路径是否正确：`ls -la /var/www/html/campuscat/`
- [ ] Nginx 配置是否正确：`nginx -t`

### 问题2：样式加载异常

**解决方案：**
- 检查浏览器控制台是否有报错
- 确认文件权限正确
- 清除浏览器缓存

### 问题3：AI识别功能不可用

**说明：**
Demo 中的 AI 识别是模拟功能，实际部署需要：
1. 申请腾讯云 AI 服务
2. 配置 API 密钥
3. 部署后端服务

详见 [API文档](API.md)

---

## 📞 获取帮助

- 查看 [GitHub Issues](../../issues)
- 提交新的 Issue
- 联系维护者

---

## 🎉 部署完成

恭喜！您已成功部署 CampusCat Manager。

下一步：
- [配置腾讯技术公益工具箱](../README.md#快速开始)
- [查看使用文档](../README.md)
- [参与贡献](../CONTRIBUTING.md)