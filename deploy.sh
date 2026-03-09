#!/bin/bash
echo "[AWS DEPLOY] Starting Auto-Pull & Build..."

# 1. 최신 코드 가져오기
git pull origin main

# 2. 대시보드 빌드
cd maro-dashboard
npm install
npm run build

# 3. API 서버 및 위챗 에이전트 재시작 (예시)
# pm2 restart dashboard_api
# pm2 restart wechat_agent

echo "[AWS DEPLOY] Success."
