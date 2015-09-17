How to add Helpdesk to Metrocar?

Several ways:
A) Merge branch master and helpdesk on Assembla.

OR

B) Get version from branch master working and use manual in Appendix C in Bachelor's Thesis "Modul pro hlášení a správu závad pro projekt Metrocar".
VERY simplified, what needs to be done:
1) Edit server/setup.py, 
server/requirements.py, 
server/metrocar/settings/base.py, 
server/metrocar/url.py 
accroding to the corresponding files in branch helpdesk.
2) Copy folder server/metrocar/helpdesk from branch helpdesk to server/metrocar folder.
3) Update DB, load email templates etc.:
sudo python manage.py syncdb
sudo python manage.py migrate helpdesk
sudo python manage.py collectstatic
sudo python manage.py loaddata emailtemplate.json

Once again - the whole manual is in above mentioned BT, way more detailed with better explanation.