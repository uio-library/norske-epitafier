<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:py="file://processor.py">
  <xsl:template match="/epitafium">
    <record xmlns="http://alma.exlibrisgroup.com/dc/47BIBSYS_UBO"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:dcterms="http://purl.org/dc/terms/">

      <xsl:if test="mms_id">
        <dc:identifier>alma:47BIBSYS_UBO/bibs/<xsl:value-of select="mms_id"/></dc:identifier>
      </xsl:if>

      <catalogCode><xsl:value-of select="katalognummer"/></catalogCode>

      <epitaphOn xml:lang="nob"><xsl:value-of select="avbildet"/></epitaphOn>

      <diocese xml:lang="nob"><xsl:value-of select="stift"/></diocese>

      <originalLocation xml:lang="nob"><xsl:value-of select="opprinnelig_plassering/navn"/></originalLocation>

      <location xml:lang="nob"><xsl:value-of select="plassering/navn"/></location>

      <artist xml:lang="nob"><xsl:value-of select="skaper"/></artist>

      <dc:date><xsl:value-of select="datering"/></dc:date>

      <dc:title xml:lang="nob">Norske epitafier 1550–1700: <xsl:value-of select="avbildet"/> 
      (<xsl:value-of select="opprinnelig_plassering/navn"/>)
      [TEST @ 2020-05-05]</dc:title>

      <dcterms:description xml:lang="nob"><xsl:value-of select="py:tohtml(beskrivelse)"/></dcterms:description>

      <notes><xsl:value-of select="merknader"/></notes>

      <inscriptions xml:lang="nob">
        <xsl:if test="count(innskrift) = 0">
          &lt;i&gt;Ingen&lt;/i&gt;
        </xsl:if>
        <xsl:for-each select="innskrift">&lt;b&gt;<xsl:value-of select="plassering"/>:&lt;/b&gt;&lt;br /&gt;<xsl:value-of select="py:tohtml(original)"/><xsl:if test="py:trim(oversettelse) != ''">&lt;br&gt;&lt;i&gt;Oversettelse: &lt;/i&gt;&lt;br /&gt;<xsl:value-of select="py:tohtml(oversettelse)"/></xsl:if>&lt;br&gt;&lt;br&gt;</xsl:for-each>
      </inscriptions>

      <xsl:for-each select="referanse">
        <dcterms:bibliographicCitation xml:lang="nob">
          <xsl:value-of select="py:tohtml(.)"/>
        </dcterms:bibliographicCitation>
      </xsl:for-each>

      <!-- Ansvarshavende
      <dc:creator>???</dc:creator>
      -->

      <dc:source xml:lang="nob">[forslag til tekst] Dokumentasjon av epitafier i Norge, gjennomført av Teologisk fakultet.
        Nummer i tittel er katalognummeret i prosjektkatalogen utarbeidet ved TF.
        &lt;a href=&quot;https://www.tf.uio.no/forskning/prosjekter/norske-epitafier&quot;&gt;Om samlingen&lt;/a&gt;.</dc:source>

      <dc:rights xml:lang="nob">&lt;p&gt;[Generell tekst].&lt;/p&gt;
        &lt;p&gt;Kreditering for bilder:
        <xsl:for-each select="fil">
          <xsl:value-of select="filnavn"/>: <xsl:value-of select="kreditering"/>
          &lt;br&gt;
        </xsl:for-each>
        &lt;/p&gt;
      </dc:rights>

      <xsl:for-each select="fil">
        <dc:identifier>file://<xsl:value-of select="filnavn"/></dc:identifier>
      </xsl:for-each>

      <dc:identifier><xsl:value-of select="katalognummer"/></dc:identifier>

    </record>
  </xsl:template>
</xsl:stylesheet>