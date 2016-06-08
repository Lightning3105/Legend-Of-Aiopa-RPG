DEL /S /Q build
"C:\Python34\python.exe" setupExe.py build
cd "build"
rmdir /S /Q "Legend of Aiopa"
rmdir /S /Q "Legend of Aiopa"
rename "exe.win-amd64-3.4" "Legend of Aiopa"
"C:\Program Files\7-Zip\7z.exe" a -r -tzip "LOARPG-Alpha-VX.X.X.zip" "Legend of Aiopa/*.*"
pause