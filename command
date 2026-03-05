cd /root/projects/portal_homepage

# 1. 生成新 HTML
python3 generate.py

# 2. 部署 + 推送
sudo cp index.html /var/www/portal/ && git add -A && git commit -m "Update projects" && git push origin main