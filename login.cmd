@echo off
chcp 65001 >nul

title xyw


echo ---------Author: Otirik---------
echo 校园网操作:
echo 1.登录
echo 2.注销
echo 任意键退出脚本...
echo --------------------------------


set /p choice=请选择：

if %choice%==1 (
	for /f "tokens=1,2 delims=:" %%i in (config.ini) do python main.py login -u %%i -p %%j
) else if %choice%==2 (
	python main.py logout
) else (echo "退出脚本")

pause