$(document).ready(function () {

    $('[data-toggle="tooltip"]').tooltip();

    if ($('#tabla-principal').length > 0) {
        var table = new DataTable('#tabla-principal', {
            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
            }
        });
      }
    
    if ($('#limpiar_formulario').length > 0) {
    $('#limpiar_formulario').click(function(event) {
        $("#form").validate().resetForm();
    });
    }

    if ($('#id_imagen').length > 0) {
        $("label[for='id_imagen']").hide();
        $('#id_imagen').insertAfter('#cuadro-imagen');
        $("#id_imagen").css("opacity", "0");
        $("#id_imagen").css("height", "0px");
        $("#id_imagen").css("width", "0px");
        $('#form').removeAttr('style');
    }
    
    if ($('#id_subscrito').length > 0) {
        $('#id_subscrito').wrap('<div class="row"></div>');
        $('#id_subscrito').wrap('<div class="col-sm-1" id="checkbox-subscrito"></div>');
        $('#checkbox-subscrito').after('<div id="help_text_id_subscrito" class="col-sm-11"></div>');
        $('#help_text_id_subscrito').text(`Deseo subscribirme con un aporte
          de $3.000 mensuales a la fundación "Help a Brother" y obtener un 
          5% de descuento en todas mis compras.`);
    }

    if ($('#id_imagen').length > 0) {
        $('#id_imagen').change(function() {
          var input = this;
          if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
              $('#cuadro-imagen').attr('src', e.target.result).show();
            };
            reader.readAsDataURL(input.files[0]);
          }
        });
    }

    $.validator.addMethod("rutChileno", function(value, element) {
        value = value.replace(/[.-]/g, "");

        if (value.length < 8 || value.length > 9) {
            return false;
        }

        var validChars = "0123456789K";
        var lastChar = value.charAt(value.length - 1).toUpperCase();
        if (validChars.indexOf(lastChar) == -1) {
            return false;
        }

        var rut = parseInt(value.slice(0, -1), 10);
        var factor = 2;
        var sum = 0;
        var digit;
        while (rut > 0) {
            digit = rut % 10;
            sum += digit * factor;
            rut = Math.floor(rut / 10);
            factor = factor === 7 ? 2 : factor + 1;
        }
        var dv = 11 - (sum % 11);
        dv = dv === 11 ? "0" : dv === 10 ? "K" : dv.toString();

        return dv === lastChar;
        }, "Por favor ingrese un RUT válido.");

        if(document.getElementById('id_rut')){
            document.getElementById('id_rut').addEventListener('keyup', function(e) {
            e.target.value = e.target.value.toUpperCase();
            for (let i = 0; i < e.target.value.length; i++) {
                const caracter = e.target.value[i];
                if (!"0123456789kK-".includes(caracter)) {
                e.target.value = e.target.value.replace(caracter, "");
                }
            }
        });
    }
    
    $.validator.addMethod("emailCompleto", function (value, element) {
        var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z\-0-9]{2,}))$/;
        return regex.test(value);
    }, 'El formato del correo no es válido');

    $.validator.addMethod("soloLetras", function (value, element) {
        var regex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑçÇ\s]+$/;
        return regex.test(value);
    }, "Sólo se permiten letras y espacios en blanco.");    

    $.validator.addMethod("inList", function(value, element, param) {
        return $.inArray(value, param) !== -1;
      }, "Por favor, selecciona un valor válido.");
});
