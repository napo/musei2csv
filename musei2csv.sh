steps="1 1002 2003 3004"
echo "denominazione;indirizzo;localita;cap;comune;provincia;regione;latitudine;longitudine;orario;chiusurasettimanale;accessibilita;sitoweb;email;telefono;fax;telefono-biglietteria;fax-biglietteria;email-biglietteria;costo;riduzioni;orario-biglietteria" > musei.csv
for s in $steps; 
do 
wget "http://dbunico20.beniculturali.it/DBUnicoManagerWeb/dbunicomanager/searchPlace?modulo=luoghi&tipologiaLuogo=1&stato=P&quantita=1000&offset=$s" -O out.xml
xsltproc csvmusei.xsl out.xml >> musei.csv
#rm out.xml
done
