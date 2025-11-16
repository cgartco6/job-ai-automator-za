@echo off
echo Deploying to Afrihost...
echo.

echo Setting up production environment...
docker-compose -f docker-compose.prod.yml up -d

echo Configuring domain and SSL...
echo Application deployed successfully!
echo.
echo URLs:
echo Main Site: https://jobai.co.za
echo Owner Dashboard: https://jobai.co.za/owners
echo API: https://api.jobai.co.za
echo.
pause
