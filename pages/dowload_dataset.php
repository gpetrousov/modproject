<?
if(isset($_REQUEST['dowload_id'])){
	echo "<center><span id='loading_image'><img style='margin-top:25%;' src='../theme/img/stressed_linen/loading.GIF'/></span></center>";
	$dowload_id=mysql_escape_string(filter_var($_REQUEST['dowload_id'], FILTER_SANITIZE_NUMBER_INT));
	exec('chmod -R 777 ../api/public/tmp/');
	exec('chmod -R 777 ../api/public/v1/');
	if($_REQUEST['file_type']=='json_download'){
		exec('python2.7 ../python/download_dataset_json_wrapper.py '.$dowload_id.'',$dataset_url);
		foreach($dataset_url as $ds_url) {
			$url = $ds_url;
		}
		echo "<meta http-equiv='refresh' content='0;url=".$url."' />";
	}elseif($_REQUEST['file_type']=='csv_dowload'){
		exec('python2.7 ../python/download_dataset_wrapper.py '.$dowload_id.'',$dataset_url);
		foreach($dataset_url as $ds_url) {
			$url = $ds_url;
		}	
		echo "<meta charset='utf-8'>";
		exec('chmod -R 777 ../api/public/tmp/');
		exec('chmod -R 777 ../api/public/v1/');

		$f = fopen($url, "r");
		while (($line = fgetcsv($f)) !== false) {
        		foreach ($line as $cell) {
               		echo $cell.",";
       		}
		}
		fclose($f);
	}
	echo "<script type = 'text/javascript'>document.getElementById('loading_image').style.display='none';</script>";
}
?>