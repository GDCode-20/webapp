const btnDelete= document.querySelectorAll('.btn-delete');
if(btnDelete) {
  const btnArray = Array.from(btnDelete);
  btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if(!confirm('Estás seguro de que quieres eliminarlo?')){
        e.preventDefault();
      }
    });
  })
}

$(document).ready(function(){
  console.log('funcionando');
  $('#busqueda').focus();
    // FUNCION PARA LA SELECCION COMBOBOX
    $('.sector').change(function (e) { 
      e.preventDefault();
      const sector = $('.sector :selected').val();
      $.ajax({
        type: "GET",
        url: "http://127.0.0.1:3000/getSector/"+sector,
        success: function (response) {
          var result = JSON.parse(response)
            if (sector < 9) {
              $('.supervisor').val(result[4]);
            }
            else if (sector > 17){
              $('.supervisor').val(result[2]);
            }
            else if (sector > 15 && sector < 18){
              $('.supervisor').val(result[0]);
            }
            else if (sector > 12 && sector < 16){
              $('.supervisor').val(result[3]);
            }
            else if (sector > 8 && sector < 13){
              $('.supervisor').val(result[1]);
            }
        }
      });
    });
    
    // METODO BUSCAR POR FILTRO
		$('#busqueda').on('keyup', function(e) {
			if ($('#busqueda').val()) {

				e.preventDefault();
			   	var busqueda = $('#busqueda').val();
			   	//console.log(busqueda);
			   	$.ajax({
			   		url: 'http://127.0.0.1:3000/buscar/',
			   		type: 'POST',
			   		data: {busqueda: busqueda},
			   	})
			   	.done(function(response) {
			   		var result = JSON.parse(response);
                    var temp = "";
                    var i = 0;   
                       //console.log(response);
			   		result.forEach(res => {
               if(res.supervisor == 1){
                res.supervisor = 'Juan Lopez'
               }
               else if(res.supervisor == 2){
                res.supervisor = 'Admin'
               }
               else if(res.supervisor == 3){
                res.supervisor = 'Carlos Herrera'
               }
               else if(res.supervisor == 4){
                res.supervisor = 'Lucas Castro'
               }
               else{
                  res.supervisor = 'Eduardo Ibarra'
               }
			   			temp += 
			   					`
                    <tr> 
                        <td>${res.id}</td>
                        <td>${res.nombre}</td>
                        <td>${res.apellido}</td>
                        <td>${res.sueldo}</td>
                        <td>${res.cargo}</td>
                        <td>${res.departamento}</td>
                        <td>${res.sector}</td>
                        <td>${res.supervisor}</td>
                    </tr>
                    `
                i++;
			   		});
			   		$('#tabla').html(temp);
			   	})
			   	.fail(function() {
			   		console.log('Hubo un error =(');
			   	});
			}else {window.location.href = 'http://127.0.0.1:3000/visualizar-departamentos';}
    });
});