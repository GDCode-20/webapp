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
    
});