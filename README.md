# Send-to-IBM-Alert-Notification-Service

If you are using the DASH/Jazz for Service Management web server that comes with WebSphere Application Server you can add HTML files to the "myBox" directory.  Here is a quick lesson:

Become the user that owns the Jazz files (netcool in my case)

su - netcool

CD into the myBox dir

cd ... wherever.../JazzSM/ui/myBox/

Edit your html files in myBox/web_files/

Deploy your files
Note: enclose the smadmin password in doublequotes and escape those special chars

./deployMyBox.sh -username smadmin -password "C\$tfood"

This is then the URL:
https://169.54.176.175:16311/myBox/yourfile.html

For example, my filename is initiateSWAT.html, so:
https://169.54.176.175:16311/myBox/initiateSWAT.html
