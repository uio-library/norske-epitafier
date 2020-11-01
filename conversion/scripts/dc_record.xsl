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

      <catalogCode><xsl:value-of select="py:singleline(katalognummer)"/></catalogCode>

      <epitaphOn xml:lang="nob"><xsl:value-of select="py:singleline(avbildet)"/></epitaphOn>

      <diocese xml:lang="nob"><xsl:value-of select="py:singleline(stift)"/></diocese>

      <originalLocation xml:lang="nob"><xsl:value-of select="py:singleline(opprinnelig_plassering/navn)"/><xsl:if test="opprinnelig_plassering/wikidata_id != ''"> (&lt;a href=&quot;https://ub-media.uio.no/norske-epitafier-1537-1700/#/kart?id=<xsl:value-of select="py:singleline(opprinnelig_plassering/wikidata_id)"/>&quot;&gt;Vis på kart&lt;/a&gt;)</xsl:if></originalLocation>

      <location xml:lang="nob"><xsl:value-of select="py:singleline(plassering/navn)"/><xsl:if test="plassering/wikidata_id != ''"> (&lt;a href=&quot;https://ub-media.uio.no/norske-epitafier-1537-1700/#/kart?id=<xsl:value-of select="py:singleline(plassering/wikidata_id)"/>&quot;&gt;Vis på kart&lt;/a&gt;)</xsl:if></location>

      <artist xml:lang="nob"><xsl:value-of select="py:singleline(skaper)"/></artist>

      <dc:date><xsl:value-of select="py:singleline(datering)"/></dc:date>

      <dc:title xml:lang="nob"><xsl:value-of select="py:singleline(avbildet)"/> (<xsl:value-of select="opprinnelig_plassering/navn"/>)</dc:title>

      <dcterms:isPartOf xml:lang="nob">Norske epitafier 1537–1700</dcterms:isPartOf>

      <dcterms:description xml:lang="nob"><xsl:value-of select="py:tohtml(beskrivelse)"/></dcterms:description>

      <notes><xsl:value-of select="py:tohtml(merknader)"/></notes>

      <biography><xsl:value-of select="py:tohtml(biografi)"/></biography>

      <inscriptions xml:lang="nob">
        <xsl:if test="count(innskrift) = 0">&lt;i&gt;Ingen&lt;/i&gt;</xsl:if>
        <xsl:for-each select="innskrift">&lt;b&gt;<xsl:value-of select="plassering"/>:&lt;/b&gt;&lt;br /&gt;<xsl:value-of select="py:tohtml(original)"/><xsl:if test="py:trim(oversettelse) != ''">&lt;br&gt;&lt;i&gt;Oversettelse: &lt;/i&gt;&lt;br /&gt;<xsl:value-of select="py:tohtml(oversettelse)"/></xsl:if>&lt;br&gt;&lt;br&gt;</xsl:for-each>
      </inscriptions>

      <xsl:for-each select="referanse">
        <dcterms:bibliographicCitation xml:lang="nob">
          <xsl:value-of select="py:tohtml(.)"/>
        </dcterms:bibliographicCitation>
      </xsl:for-each>

      <dc:source xml:lang="nob">&lt;a href=&quot;https://tf.uio.no/forskning/forskergrupper/protestantisme/norske-epitafier-1537-1700/&quot;&gt;Norske epitafier 1537–1700&lt;/a&gt;. Dokumentasjon av epitafier i Norge, gjennomført som del av to forskningsprosjekter ved Det teologiske fakultet, UiO.</dc:source>

      <dc:rights xml:lang="nob">&lt;p&gt;Se initialer bak hver tekst. Kreditering for bilder:
        <xsl:for-each select="fil">
          <xsl:if test="not(contains(filnavn, '.pdf'))">
            <xsl:value-of select="filnavn"/>: <xsl:value-of select="kreditering"/> (<xsl:value-of select="lisens"/>)&lt;br&gt;
          </xsl:if>
        </xsl:for-each>
        &lt;/p&gt;
      </dc:rights>

      <xsl:for-each select="fil">
        <xsl:if test="filnavn != '' and not(contains(filnavn, '.pdf'))">
          <dc:identifier>file://<xsl:value-of select="filnavn"/></dc:identifier>
        </xsl:if>
      </xsl:for-each>

      <dc:identifier><xsl:value-of select="katalognummer"/></dc:identifier>

    </record>
  </xsl:template>
</xsl:stylesheet>