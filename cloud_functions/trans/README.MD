<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html><head><title>Python: module main</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head><body bgcolor="#f0f0f8">

<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="heading">
<tr bgcolor="#7799ee">
<td valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial">&nbsp;<br><big><big><strong>main</strong></big></big></font></td
><td align=right valign=bottom
><font color="#ffffff" face="helvetica, arial"><a href=".">index</a><br><a href="file:x%3A%5Cml-spez%5Ccloud_functions%5Ctrans%5Cmain.py">x:\ml-spez\cloud_functions\trans\main.py</a></font></td></tr></table>
    <p></p>
<p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#aa55cc">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Modules</strong></big></font></td></tr>
    
<tr><td bgcolor="#aa55cc"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><table width="100%" summary="list"><tr><td width="25%" valign=top><a href="google.cloud.aiplatform.html">google.cloud.aiplatform</a><br>
<a href="google.cloud.bigquery.html">google.cloud.bigquery</a><br>
</td><td width="25%" valign=top><a href="functions_framework.html">functions_framework</a><br>
<a href="google.html">google</a><br>
</td><td width="25%" valign=top><a href="os.html">os</a><br>
<a href="requests.html">requests</a><br>
</td><td width="25%" valign=top></td></tr></table></td></tr></table><p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#eeaa77">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Functions</strong></big></font></td></tr>
    
<tr><td bgcolor="#eeaa77"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><dl><dt><a name="-batch_embeddings"><strong>batch_embeddings</strong></a>() -&gt; None</dt><dd><tt>Perform&nbsp;batch&nbsp;embeddings&nbsp;by&nbsp;submitting&nbsp;a&nbsp;batch&nbsp;prediction&nbsp;job&nbsp;to&nbsp;AI&nbsp;Platform&nbsp;Prediction.<br>
&nbsp;<br>
This&nbsp;function&nbsp;sends&nbsp;a&nbsp;POST&nbsp;request&nbsp;to&nbsp;submit&nbsp;a&nbsp;batch&nbsp;prediction&nbsp;job&nbsp;for&nbsp;embedding&nbsp;generation.<br>
The&nbsp;job&nbsp;processes&nbsp;input&nbsp;data&nbsp;from&nbsp;a&nbsp;BigQuery&nbsp;table&nbsp;and&nbsp;stores&nbsp;the&nbsp;embeddings&nbsp;in&nbsp;another&nbsp;BigQuery&nbsp;table.<br>
&nbsp;<br>
Note:&nbsp;The&nbsp;function&nbsp;assumes&nbsp;the&nbsp;existence&nbsp;of&nbsp;the&nbsp;`<a href="#-get_default_token">get_default_token</a>()`&nbsp;function.<br>
&nbsp;<br>
Returns:<br>
&nbsp;&nbsp;&nbsp;&nbsp;None</tt></dd></dl>
 <dl><dt><a name="-create_index"><strong>create_index</strong></a>(project_number: str) -&gt; None</dt><dd><tt>Create&nbsp;an&nbsp;index&nbsp;for&nbsp;job&nbsp;postings.<br>
&nbsp;<br>
Args:<br>
&nbsp;&nbsp;&nbsp;&nbsp;project_number&nbsp;(str):&nbsp;Google&nbsp;Cloud&nbsp;project&nbsp;number.<br>
&nbsp;<br>
Returns:<br>
&nbsp;&nbsp;&nbsp;&nbsp;None</tt></dd></dl>
 <dl><dt><a name="-deploy_index"><strong>deploy_index</strong></a>(project_number: str, index_id: str) -&gt; None</dt><dd><tt>Deploy&nbsp;an&nbsp;index&nbsp;to&nbsp;the&nbsp;Matching&nbsp;Engine&nbsp;Index&nbsp;Endpoint.<br>
&nbsp;<br>
Args:<br>
&nbsp;&nbsp;&nbsp;&nbsp;project_number&nbsp;(str):&nbsp;Google&nbsp;Cloud&nbsp;project&nbsp;number.<br>
&nbsp;&nbsp;&nbsp;&nbsp;index_id&nbsp;(str):&nbsp;ID&nbsp;of&nbsp;the&nbsp;index&nbsp;to&nbsp;deploy.<br>
&nbsp;<br>
Returns:<br>
&nbsp;&nbsp;&nbsp;&nbsp;None</tt></dd></dl>
 <dl><dt><a name="-export_to_gcs"><strong>export_to_gcs</strong></a>() -&gt; None</dt><dd><tt>Export&nbsp;data&nbsp;from&nbsp;BigQuery&nbsp;table&nbsp;to&nbsp;Google&nbsp;Cloud&nbsp;Storage&nbsp;in&nbsp;JSON&nbsp;format.<br>
&nbsp;<br>
This&nbsp;function&nbsp;exports&nbsp;the&nbsp;content&nbsp;of&nbsp;a&nbsp;BigQuery&nbsp;table&nbsp;to&nbsp;a&nbsp;specified&nbsp;Cloud&nbsp;Storage&nbsp;location<br>
in&nbsp;newline-delimited&nbsp;JSON&nbsp;format.<br>
&nbsp;<br>
Returns:<br>
&nbsp;&nbsp;&nbsp;&nbsp;None</tt></dd></dl>
 <dl><dt><a name="-get_default_token"><strong>get_default_token</strong></a>() -&gt; str</dt><dd><tt>Get&nbsp;the&nbsp;default&nbsp;access&nbsp;token&nbsp;using&nbsp;Google&nbsp;Cloud&nbsp;Platform&nbsp;credentials.<br>
&nbsp;<br>
Returns:<br>
&nbsp;&nbsp;&nbsp;&nbsp;str:&nbsp;Access&nbsp;token&nbsp;obtained&nbsp;from&nbsp;credentials.</tt></dd></dl>
 <dl><dt><a name="-get_weighted_embeddings"><strong>get_weighted_embeddings</strong></a>() -&gt; bool</dt><dd><tt>Calculate&nbsp;weighted&nbsp;embeddings&nbsp;for&nbsp;each&nbsp;job&nbsp;and&nbsp;store&nbsp;the&nbsp;results&nbsp;in&nbsp;a&nbsp;BigQuery&nbsp;table.<br>
&nbsp;<br>
This&nbsp;function&nbsp;defines&nbsp;a&nbsp;JavaScript&nbsp;UDF&nbsp;(User-Defined&nbsp;Function)&nbsp;to&nbsp;perform&nbsp;the&nbsp;weighted&nbsp;averaging<br>
of&nbsp;chunk&nbsp;embeddings&nbsp;and&nbsp;then&nbsp;executes&nbsp;a&nbsp;BigQuery&nbsp;query&nbsp;to&nbsp;create&nbsp;a&nbsp;table&nbsp;with&nbsp;the&nbsp;calculated<br>
weighted&nbsp;embeddings.<br>
&nbsp;<br>
Returns:<br>
&nbsp;&nbsp;&nbsp;&nbsp;bool:&nbsp;True&nbsp;if&nbsp;the&nbsp;operation&nbsp;is&nbsp;successful,&nbsp;False&nbsp;otherwise.</tt></dd></dl>
 <dl><dt><a name="-trans"><strong>trans</strong></a>(request: flask.wrappers.Request) -&gt; str</dt><dd><tt>Handle&nbsp;incoming&nbsp;HTTP&nbsp;requests&nbsp;for&nbsp;various&nbsp;processing&nbsp;modes.<br>
&nbsp;<br>
Args:<br>
&nbsp;&nbsp;&nbsp;&nbsp;request&nbsp;(Request):&nbsp;The&nbsp;incoming&nbsp;HTTP&nbsp;request.<br>
&nbsp;<br>
Returns:<br>
&nbsp;&nbsp;&nbsp;&nbsp;str:&nbsp;Response&nbsp;message.</tt></dd></dl>
 <dl><dt><a name="-trans_job_posts"><strong>trans_job_posts</strong></a>() -&gt; bool</dt><dd><tt>Transform&nbsp;job&nbsp;posts&nbsp;by&nbsp;chunking&nbsp;the&nbsp;description&nbsp;text&nbsp;and&nbsp;store&nbsp;the&nbsp;results&nbsp;in&nbsp;a&nbsp;BigQuery&nbsp;table.<br>
&nbsp;<br>
This&nbsp;function&nbsp;defines&nbsp;a&nbsp;JavaScript&nbsp;UDF&nbsp;(User-Defined&nbsp;Function)&nbsp;to&nbsp;split&nbsp;the&nbsp;input&nbsp;description&nbsp;text<br>
into&nbsp;chunks&nbsp;based&nbsp;on&nbsp;the&nbsp;specified&nbsp;maximum&nbsp;chunk&nbsp;size.&nbsp;It&nbsp;then&nbsp;executes&nbsp;a&nbsp;BigQuery&nbsp;query&nbsp;to&nbsp;create<br>
a&nbsp;table&nbsp;with&nbsp;the&nbsp;transformed&nbsp;job&nbsp;posts.<br>
&nbsp;<br>
Returns:<br>
&nbsp;&nbsp;&nbsp;&nbsp;bool:&nbsp;True&nbsp;if&nbsp;the&nbsp;operation&nbsp;is&nbsp;successful,&nbsp;False&nbsp;otherwise.</tt></dd></dl>
</td></tr></table><p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#55aa55">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Data</strong></big></font></td></tr>
    
<tr><td bgcolor="#55aa55"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><strong>Dict</strong> = typing.Dict</td></tr></table>
</body></html>