<?
function return_available_dataset(){
	exec('python2.7 ../python/available_datasets_wrapper.py',$available_dataset);
	$flag_des=9;
	foreach($available_dataset as $dataset) {
		if(ctype_digit($dataset)){
			if($flag_des == 0){
				echo "</span><br/>";
			}
			$flag_des=1;
			$id=$dataset;
		}elseif($flag_des==1){
			echo "<span onclick=\"description_hideshow('".$id."')\">".$dataset."</span>";
			echo "<form action='dowload_dataset.php' method='get' target='_blank'><input type='hidden' name='dowload_id' value='".$id."' />";
			echo "<button type='submit' name='file_type' value='csv_dowload' >Μεταφόρτωση CSV</button>";
			echo "<button type='submit' name='file_type' value='json_download'>Μεταφόρτωση JSON</button></form>";
			$flag_des=2;
			echo "<span id='dataset_desc_".$id."' style='display:none;'> ";
		}else{
			echo $dataset;
			$flag_des=0;
		}
	}
}
 ?>

<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Διαθέσιμα σύνολα δεδομένων
</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">
            <link rel="stylesheet" href="../theme/css/normalize.css">
        <link href='//fonts.googleapis.com/css?family=Raleway' rel='stylesheet' type='text/css'>
        <link href='//fonts.googleapis.com/css?family=Oswald' rel='stylesheet' type='text/css'>
        <link href='http://fonts.googleapis.com/css?family=PT+Mono' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="../theme/css/font-awesome.min.css">
        <link rel="stylesheet" href="../theme/css/main.css">

    <link rel="stylesheet" href="../theme/css/blog.css">
    <link rel="stylesheet" href="../theme/css/github.css">
        <script src="../theme/js/vendor/modernizr-2.6.2.min.js"></script>
		<script src="../theme/js/custom_functions.js"></script>
    </head>
    <body>
        <!--[if lt IE 7]>
            <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
        <![endif]-->

        <div id="wrapper">
<header id="sidebar" class="side-shadow">
    <hgroup id="site-header">
        <a id="site-title" href=".."><h1><i class="icon-coffee"></i> modproject</h1></a>
        <p id="site-desc"></p>
    </hgroup>
    <nav>
        <ul id="nav-links">
                <li><a href="../pages/about.html">Περί</a></li>
				<li><a href="../pages/available-dataset.php">Διαθέσιμα σύνολα δεδομένων</a></li>
				<li><a href="../pages/manualapi.html">Ανοιχτό API</a></li>
        </ul>
    </nav>
<footer id="site-info">
    <p>
        Proudly powered by <a href="http://getpelican.com/">Pelican</a> and <a href="http://python.org/">Python</a>. Theme by<a href="https://github.com/hdra/pelican-cait">hndr</a>.
    </p>
    <p>
        Textures by <a href="http://subtlepatterns.com/">Subtle Pattern</a>. Font Awesome by <a href="http://fortawesome.github.io/Font-Awesome/">Dave Grandy</a>.
    </p>
</footer></header>
<div id="post-container">
    <ol id="post-list">
        <li>
            <article class="post-entry">
                <header class="entry-header">
                    <a href="../pages/available-dataset.php" rel="bookmark"><h1>Διαθέσιμα σύνολα δεδομένων</h1></a>
                </header>
                <section class="post-content">
                    <p>Μπορείτε να δείτε την περιγραφή κάθε συνόλου δεδομένων κάνοντας click στον τίτλο του.
					<br/>Η μεταφόρτωση CSV μπορεί να διαρκέσει λίγη ώρα καθώς γίνεται η μετατροπή δεδομένων.</p>
					<? return_available_dataset(); ?>
                </section>
                <hr/>
            </article>
        </li>
    </ol>
</div>
        </div>

        <script src="../theme/js/main.js"></script>
    </body>
</html>