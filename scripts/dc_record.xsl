<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:py="file://processor.py">
  <xsl:template match="/epitafium">
    <record xmlns="http://alma.exlibrisgroup.com/dc/47BIBSYS_UBO"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:dcterms="http://purl.org/dc/terms/">

      <location xml:lang="nob">
        <xsl:value-of select="plassering"/>
      </location>

      <originalLocation xml:lang="nob">
        <xsl:value-of select="opprinnelig_plassering"/>
      </originalLocation>

      <diocese xml:lang="nob">
        <xsl:value-of select="stift"/>
      </diocese>

      <epitaphOn xml:lang="nob">
        <xsl:value-of select="avbildet"/>
      </epitaphOn>

      <dcterms:description xml:lang="nob">
        [forslag til tekst] Dokumentasjon av epitafier i Norge, gjennomført av Teologisk fakultet.
        Nummer i tittel er katalognummeret i prosjektkatalogen utarbeidet ved TF.
        &lt;a href=&quot;https://www.tf.uio.no/forskning/prosjekter/norske-epitafier&quot;&gt;Om samlingen&lt;/a&gt;.
      </dcterms:description>

      <dc:date>
        <xsl:value-of select="datering"/>
      </dc:date>

      <dc:rights xml:lang="nob">
        Lisens knyttet til bruk [...]
      </dc:rights>

      <dc:title xml:lang="nob">
        Norske epitafier : <xsl:value-of select="katalognummer"/> [test versjon 02]
      </dc:title>

      <xsl:if test="mms_id">
        <dc:identifier>alma:47BIBSYS_UBO/bibs/<xsl:value-of select="mms_id"/></dc:identifier>
      </xsl:if>

      <xsl:for-each select="fil">
        <dc:identifier>file://<xsl:value-of select="filnavn"/></dc:identifier>
      </xsl:for-each>

      <inscriptions xml:lang="nob">
        <xsl:for-each select="innskrift">
          <p>
            <b><xsl:value-of select="plassering"/>:</b>
            <xsl:text> </xsl:text><!-- explicit space -->
            <xsl:value-of select="py:tohtml(original)"/>

            <xsl:if test="oversettelse">
              <b>Oversettelse: </b>
              <xsl:value-of select="py:tohtml(oversettelse)"/>
            </xsl:if>
          </p>
        </xsl:for-each>
      </inscriptions>

      <xsl:for-each select="referanse">
        <dcterms:bibliographicCitation xml:lang="nob">
          <xsl:value-of select="py:tohtml(.)"/>
        </dcterms:bibliographicCitation>
      </xsl:for-each>

    </record>
  </xsl:template>
</xsl:stylesheet>