function description_hideshow(id) {

	var span = document.getElementById('dataset_desc_'+id);
	if(span.style.display=='none'){
		span.style.display='block';
	}else{
		span.style.display='none';
	}
}
