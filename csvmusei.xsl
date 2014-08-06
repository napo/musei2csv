<xsl:stylesheet version='1.0'
xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
<xsl:template match='/'>
<xsl:for-each select='mibac-list'>
<xsl:for-each select='mibac'>
<xsl:value-of select='luogodellacultura/denominazione/nomestandard'/>;;<xsl:value-of select='luogodellacultura/indirizzi/indirizzo/via-piazza'/>;;<xsl:value-of select='luogodellacultura/indirizzi/indirizzo/localita'/>;;<xsl:value-of select='luogodellacultura/indirizzi/indirizzo/cap'/>;;<xsl:value-of select='luogodellacultura/indirizzi/indirizzo/comune'/>;;<xsl:value-of select='luogodellacultura/indirizzi/indirizzo/provincia'/>;;<xsl:value-of select='luogodellacultura/indirizzi/indirizzo/regione'/>;;<xsl:value-of select='luogodellacultura/indirizzi/indirizzo/cartografia/punto/latitudineX'/>;;<xsl:value-of select='luogodellacultura/indirizzi/indirizzo/cartografia/punto/longitudineY'/>;;\n
</xsl:for-each>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet> 
